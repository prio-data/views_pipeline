from views_pipeline.managers.model_manager import ModelManager
from views_pipeline.managers.path_manager import ModelPath
# from views_pipeline.views_pipeline.managers.path_manager import EnsemblePath
from views_stepshifter.models import StepshifterModel
from views_stepshifter.models.hurdle_model import HurdleModel
from views_pipeline.evaluation.metrics import generate_metric_dict
from views_pipeline.models.outputs import generate_output_dict
from views_pipeline.wandb.utils import add_wandb_monthly_metrics, generate_wandb_log_dict, log_wandb_log_dict
from views_pipeline.files.utils import FileUtils
from views_forecasts.extensions import *
import logging
import pandas as pd
import numpy as np
import time
import wandb
from datetime import datetime
from sklearn.metrics import mean_squared_error

logger = logging.getLogger(__name__)


class StepshifterManager(ModelManager):

    def __init__(self, model_path: ModelPath) -> None:
        super().__init__(model_path)
        self._is_hurdle = self._config_meta["algorithm"] == "HurdleModel"

    def _update_sweep_config(self, args):
        '''
        Updates the configuration object with config_hyperparameters, config_meta, config_deployment, and the command line arguments.

        Args:
            args: Command line arguments

        Returns:
            The updated configuration object.
        '''

        config = self._config_sweep
        config["parameters"]["run_type"] = {"value": args.run_type}
        config["parameters"]["sweep"] = {"value": True}
        config["parameters"]["name"] = {"value": self._config_meta["name"]}
        config["parameters"]["depvar"] = {"value": self._config_meta["depvar"]}
        config["parameters"]["algorithm"] = {"value": self._config_meta["algorithm"]}

        if self._is_hurdle:
            config["parameters"]["model_clf"] = {"value": self._config_meta["model_clf"]}
            config["parameters"]["model_reg"] = {"value": self._config_meta["model_reg"]}
    
        return config
    
    def _split_hurdle_parameters(self):
        """
        Split the parameters dictionary into two separate dictionaries, one for the
        classification model and one for the regression model.

        Returns:
            A dictionary containing original config, the split classification and regression parameters.
        """

        cls_dict = {}
        reg_dict = {}
        config = self.config

        for key, value in config.items():
            if key.startswith("cls_"):
                cls_key = key.replace("cls_", "")
                cls_dict[cls_key] = value
            elif key.startswith("reg_"):
                reg_key = key.replace("reg_", "")
                reg_dict[reg_key] = value

        config["parameters"]["clf"] = cls_dict
        config["parameters"]["reg"] = reg_dict

        return config

    def _execute_model_tasks(self, config=None, train=None, eval=None, forecast=None, artifact_name=None):
        """
        Executes various model-related tasks including training, evaluation, and forecasting.

        This function manages the execution of different tasks such as training the model,
        evaluating an existing model, or performing forecasting.
        It also initializes the WandB project.

        Args:
            config: Configuration object containing parameters and settings.
            project: The WandB project name.
            train: Flag to indicate if the model should be trained.
            eval: Flag to indicate if the model should be evaluated.
            forecast: Flag to indicate if forecasting should be performed.
            artifact_name (optional): Specific name of the model artifact to load for evaluation or forecasting.
        """
        start_t = time.time()

        # Initialize WandB
        try:
            with wandb.init(project=self._project, entity=self._entity, config=config):  # project and config ignored when running a sweep

                # add the monthly metrics to WandB
                add_wandb_monthly_metrics()

                # Update config from WandB initialization above
                self.config = wandb.config

                # W&B does not directly support nested dictionaries for hyperparameters
                if self.config["sweep"] and self._is_hurdle:
                    self.config["parameters"] = self._split_hurdle_parameters(self.config)

                if self.config["sweep"]:
                    logger.info(f"Sweeping model {self.config['name']}...")
                    model = self._train_model_artifact()
                    logger.info(f"Evaluating model {self.config['name']}...")
                    self._evaluate_sweep(model)

                if train:
                    logger.info(f"Training model {self.config['name']}...")
                    self._train_model_artifact()

                if eval:
                    logger.info(f"Evaluating model {self.config['name']}...")
                    self._evaluate_model_artifact(artifact_name)

                if forecast:
                    logger.info(f"Forecasting model {self.config['name']}...")
                    self._forecast_model_artifact(artifact_name)
            wandb.finish()
        except Exception as e:
            logger.error(f"Error during model tasks execution: {e}")
        end_t = time.time()
        minutes = (end_t - start_t) / 60
        logger.info(f"Done. Runtime: {minutes:.3f} minutes.\n")

    def _get_model(self, partitioner_dict: dict):
        """
        Get the model based on the algorithm specified in the config

        Args:
            partitioner_dict: The dictionary of partitioners.

        Returns:
            The model object based on the algorithm specified in the config
        """

        if self._is_hurdle:
            model = HurdleModel(self.config, partitioner_dict)
        else:
            self.config["model_reg"] = self.config["algorithm"]
            model = StepshifterModel(self.config, partitioner_dict)

        return model
    
    def _get_standardized_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize the DataFrame based on the run type

        Args:
            df: The DataFrame to standardize

        Returns:
            The standardized DataFrame
        """

        run_type = self.config["run_type"]
        steps = self.config["steps"]
        depvar = self.config["depvar"]

        # choose the columns to keep based on the run type and replace negative values with 0
        if run_type in ["calibration", "testing"]:
            cols = [depvar] + df.forecasts.prediction_columns
        elif run_type == "forecasting":
            cols = [f"step_pred_{i}" for i in steps]
        df = df.replace([np.inf, -np.inf], 0)[cols]
        df = df.mask(df < 0, 0)
        return df
    
    def _train_model_artifact(self):
        # print(config)
        path_raw  = self._model_path.data_raw
        path_generated = self._model_path.data_generated
        path_artifacts = self._model_path.artifacts
        run_type = self.config["run_type"]
        df_viewser = pd.read_pickle(path_raw / f"{run_type}_viewser_df.pkl")

        partitioner_dict = self._data_loader.partition_dict
        stepshift_model = self._get_model(partitioner_dict)
        stepshift_model.fit(df_viewser)

        if not self.config["sweep"]:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_filename = f"{run_type}_model_{timestamp}.pkl"
            stepshift_model.save(path_artifacts / model_filename)
            data_fetch_timestamp = FileUtils.read_log_file(path_raw / f"{run_type}_data_fetch_log.txt").get("Data Fetch Timestamp", None)
            FileUtils.create_log_file(path_generated, self.config, timestamp, None, data_fetch_timestamp)
        return stepshift_model

    def _evaluate_model_artifact(self, artifact_name):
        path_raw = self._model_path.data_raw
        path_generated = self._model_path.data_generated
        path_artifacts = self._model_path.artifacts
        run_type = self.config["run_type"]

        # if an artifact name is provided through the CLI, use it.
        # Otherwise, get the latest model artifact based on the run type
        if artifact_name:
            logger.info(f"Using (non-default) artifact: {artifact_name}")

            if not artifact_name.endswith(".pkl"):
                artifact_name += ".pkl"
            path_artifact = path_artifacts / artifact_name
        else:
            # use the latest model artifact based on the run type
            logger.info(f"Using latest (default) run type ({run_type}) specific artifact")
            path_artifact = self._get_latest_model_artifact(path_artifacts, run_type)

        self.config["timestamp"] = path_artifact.stem[-15:]
        df_viewser = pd.read_pickle(path_raw / f"{run_type}_viewser_df.pkl")

        try:
            stepshift_model = pd.read_pickle(path_artifact)
        except FileNotFoundError:
            logger.exception(f"Model artifact not found at {path_artifact}")

        df = stepshift_model.predict(run_type, df_viewser)
        df = self._get_standardized_df(df)
        data_generation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data_fetch_timestamp = FileUtils.read_log_file(path_raw / f"{run_type}_data_fetch_log.txt").get("Data Fetch Timestamp", None)

        _, df_output = generate_output_dict(df, self.config)
        evaluation, df_evaluation = generate_metric_dict(df, self.config)
        log_wandb_log_dict(self.config, evaluation)

        self._save_model_outputs(df_evaluation, df_output, path_generated)
        self._save_predictions(df, path_generated)
        FileUtils.create_log_file(path_generated, self.config, self.config["timestamp"], data_generation_timestamp, data_fetch_timestamp)
    
    def _forecast_model_artifact(self, artifact_name):
        path_raw = self._model_path.data_raw
        path_generated = self._model_path.data_generated
        path_artifacts = self._model_path.artifacts
        run_type = self.config["run_type"]

        # if an artifact name is provided through the CLI, use it.
        # Otherwise, get the latest model artifact based on the run type
        if artifact_name:
            logger.info(f"Using (non-default) artifact: {artifact_name}")

            if not artifact_name.endswith(".pkl"):
                artifact_name += ".pkl"
            path_artifact = path_artifacts / artifact_name
        else:
            # use the latest model artifact based on the run type
            logger.info(f"Using latest (default) run type ({run_type}) specific artifact")
            path_artifact = self._get_latest_model_artifact(path_artifacts, run_type)

        self.config["timestamp"] = path_artifact.stem[-15:]
        df_viewser = pd.read_pickle(path_raw / f"{run_type}_viewser_df.pkl")

        try:
            stepshift_model = pd.read_pickle(path_artifact)
        except FileNotFoundError:
            logger.exception(f"Model artifact not found at {path_artifact}")

        df_predictions = stepshift_model.predict(run_type, df_viewser)
        df_predictions = self._get_standardized_df(df_predictions)
        data_generation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data_fetch_timestamp = FileUtils.read_log_file(path_raw / f"{run_type}_data_fetch_log.txt").get("Data Fetch Timestamp", None)

        self._save_predictions(df_predictions, path_generated)
        FileUtils.create_log_file(path_generated, self.config, self.config["timestamp"], data_generation_timestamp, data_fetch_timestamp)

    def _evaluate_sweep(self, model):
        path_raw = self._model_path.data_raw
        run_type = self.config["run_type"]
        steps = self.config["steps"]

        df_viewser = pd.read_pickle(path_raw / f"{run_type}_viewser_df.pkl")
        df = model.predict(run_type, df_viewser)
        df = self._get_standardized_df(df)

        # Temporarily keep this because the metric to minimize is MSE
        pred_cols = [f"step_pred_{str(i)}" for i in steps]
        df["mse"] = df.apply(lambda row: mean_squared_error([row[self.config["depvar"]]] * len(steps),
                                                            [row[col] for col in pred_cols]), axis=1)

        wandb.log({"MSE": df["mse"].mean()})

        evaluation, _ = generate_metric_dict(df, self.config)
        log_wandb_log_dict(self.config, evaluation)
