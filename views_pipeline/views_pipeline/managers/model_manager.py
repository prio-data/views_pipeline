import sys
from abc import abstractmethod
from views_pipeline.managers.path_manager import ModelPath
from views_pipeline.wandb.utils import add_wandb_monthly_metrics, generate_wandb_log_dict, log_wandb_log_dict
from typing import Union, Optional, List, Dict
from views_pipeline.data.dataloaders import ViewsDataLoader
import logging
import importlib
import wandb
import time
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)




# ============================================================ Model Manager ============================================================


class ModelManager:
    """
    Manages the lifecycle of a machine learning model, including configuration loading,
    training, evaluation, and forecasting.

    Attributes:
        _entity (str): The WandB entity name.
        _model_path (ModelPath): The path manager for the model.
        _script_paths (dict): Dictionary of script paths.
        _config_deployment (dict): Deployment configuration.
        _config_hyperparameters (dict): Hyperparameters configuration.
        _config_meta (dict): Metadata configuration.
        _config_sweep (dict): Sweep configuration (if applicable).
        _data_loader (ViewsDataLoader): Data loader for fetching and preprocessing data.
    """

    def __init__(self, model_path: ModelPath) -> None:
        """
        Initializes the ModelManager with the given model path.

        Args:
            model_path (ModelPath): The path manager for the model.
        """
        self._entity = "views_pipeline"
        self._model_path = model_path
        self._script_paths = self._model_path.get_scripts()
        self._config_deployment = self.__load_config(
            "config_deployment.py", "get_deployment_config"
        )
        self._config_hyperparameters = self.__load_config(
            "config_hyperparameters.py", "get_hp_config"
        )
        self._config_meta = self.__load_config("config_meta.py", "get_meta_config")
        if self._model_path.target == "model":
            self._config_sweep = self.__load_config(
                "config_sweep.py", "get_sweep_config"
            )
        self._data_loader = ViewsDataLoader(model_path=self._model_path)

    def __load_config(self, script_name: str, config_method: str) -> Union[Dict, None]:
        """
        Loads and executes a configuration method from a specified script.

        Args:
            script_name (str): The name of the script to load.
            config_method (str): The name of the configuration method to execute.

        Returns:
            dict: The result of the configuration method if the script and method are found, otherwise None.

        Raises:
            AttributeError: If the specified configuration method does not exist in the script.
            ImportError: If there is an error importing the script.
        """
        script_path = self._script_paths.get(script_name)
        if script_path:
            try:
                spec = importlib.util.spec_from_file_location(script_name, script_path)
                config_module = importlib.util.module_from_spec(spec)
                sys.modules[script_name] = config_module
                spec.loader.exec_module(config_module)
                if hasattr(config_module, config_method):
                    return getattr(config_module, config_method)()
            except (AttributeError, ImportError) as e:
                logger.error(f"Error loading config from {script_name}: {e}")
        return None

    def _update_single_config(self, args) -> Dict:
        """
        Updates the configuration object with hyperparameters, metadata, deployment settings, and command line arguments.

        Args:
            args: Command line arguments.

        Returns:
            dict: The updated configuration object.
        """
        config = {
            **self._config_hyperparameters,
            **self._config_meta,
            **self._config_deployment,
        }
        config["run_type"] = args.run_type
        config["sweep"] = False
        return config

    def _update_sweep_config(self, args) -> Dict:
        """
        Updates the configuration object for a sweep run with hyperparameters, metadata, and command line arguments.

        Args:
            args: Command line arguments.

        Returns:
            dict: The updated configuration object.
        """
        config = self._config_sweep
        config["parameters"]["run_type"] = {"value": args.run_type}
        config["parameters"]["sweep"] = {"value": True}
        config["parameters"]["name"] = {"value": self._config_meta["name"]}
        config["parameters"]["depvar"] = {"value": self._config_meta["depvar"]}
        config["parameters"]["algorithm"] = {"value": self._config_meta["algorithm"]}
        return config

    def execute_single_run(self, args) -> None:
        """
        Executes a single run of the model, including data fetching, training, evaluation, and forecasting.

        Args:
            args: Command line arguments.
        """
        self.config = self._update_single_config(args)
        self._project = f"{self.config['name']}_{args.run_type}"

        try:
            with wandb.init(project=f"{self._project}_fetch", entity=self._entity):
                self._data_loader.get_data(
                    use_saved=args.saved,
                    validate=True,
                    self_test=args.drift_self_test,
                    partition=args.run_type,
                )
            wandb.finish()

            self._execute_model_tasks(
                config=self.config,
                train=args.train,
                eval=args.evaluate,
                forecast=args.forecast,
                artifact_name=args.artifact_name,
            )
        except Exception as e:
            logger.error(f"Error during single run execution: {e}")

    def execute_sweep_run(self, args) -> None:
        """
        Executes a sweep run of the model, including data fetching and hyperparameter optimization.

        Args:
            args: Command line arguments.
        """
        self.config = self._update_sweep_config(args)
        self._project = f"{self.config['name']}_sweep"

        try:
            with wandb.init(project=f"{self._project}_fetch", entity=self._entity):
                self._data_loader.get_data(
                    use_saved=args.saved,
                    validate=True,
                    self_test=args.drift_self_test,
                    partition=args.run_type,
                )
            wandb.finish()

            sweep_id = wandb.sweep(
                self.config, project=self._project, entity=self._entity
            )
            wandb.agent(sweep_id, self._execute_model_tasks, entity=self._entity)
        except Exception as e:
            logger.error(f"Error during sweep run execution: {e}")

    def _execute_model_tasks(
        self,
        config: Optional[Dict] = None,
        train: Optional[bool] = None,
        eval: Optional[bool] = None,
        forecast: Optional[bool] = None,
        artifact_name: Optional[str] = None,
    ) -> None:
        """
        Executes various model-related tasks including training, evaluation, and forecasting.

        Args:
            config (dict, optional): Configuration object containing parameters and settings.
            train (bool, optional): Flag to indicate if the model should be trained.
            eval (bool, optional): Flag to indicate if the model should be evaluated.
            forecast (bool, optional): Flag to indicate if forecasting should be performed.
            artifact_name (str, optional): Specific name of the model artifact to load for evaluation or forecasting.
        """
        start_t = time.time()
        try:
            with wandb.init(project=self._project, entity=self._entity, config=config):
                add_wandb_monthly_metrics()
                self.config = wandb.config

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

    @abstractmethod
    def _train_model_artifact(self):
        """
        Abstract method to train the model artifact. Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def _evaluate_model_artifact(self, artifact_name: str):
        """
        Abstract method to evaluate the model artifact. Must be implemented by subclasses.

        Args:
            artifact_name (str): The name of the model artifact to evaluate.
        """
        pass

    @abstractmethod
    def _forecast_model_artifact(self, artifact_name: str):
        """
        Abstract method to forecast using the model artifact. Must be implemented by subclasses.

        Args:
            artifact_name (str): The name of the model artifact to use for forecasting.
        """
        pass

    @abstractmethod
    def _evaluate_sweep(self, model):
        """
        Abstract method to evaluate the model during a sweep. Must be implemented by subclasses.

        Args:
            model: The model to evaluate.
        """
        pass

    def _get_artifact_files(self, path_artifact: Path, run_type: str) -> List[Path]:
        """
        Retrieve artifact files from a directory that match the given run type and common extensions.

        Args:
            path_artifact (Path): The directory path where model files are stored.
            run_type (str): The type of run (e.g., calibration, testing).

        Returns:
            List[Path]: List of matching model file paths.
        """
        common_extensions = [
            ".pt",
            ".pth",
            ".h5",
            ".hdf5",
            ".pkl",
            ".json",
            ".bst",
            ".txt",
            ".bin",
            ".cbm",
            ".onnx",
        ]
        artifact_files = [
            f
            for f in path_artifact.iterdir()
            if f.is_file()
            and f.stem.startswith(f"{run_type}_model_")
            and f.suffix in common_extensions
        ]
        return artifact_files

    def _get_latest_model_artifact(self, path_artifact, run_type):
        """
        Retrieve the path (pathlib path object) latest model artifact for a given run type based on the modification time.

        Args:
            path_artifact (Path): The model specifc directory path where artifacts are stored.
            run_type (str): The type of run (e.g., calibration, testing, forecasting).

        Returns:
            The path (pathlib path objsect) to the latest model artifact given the run type.

        Raises:
            FileNotFoundError: If no model artifacts are found for the given run type.
        """

        # List all model files for the given specific run_type with the expected filename pattern
        model_files = self._get_artifact_files(path_artifact, run_type)

        if not model_files:
            raise FileNotFoundError(
                f"No model artifacts found for run type '{run_type}' in path '{path_artifact}'"
            )

        # Sort the files based on the timestamp embedded in the filename. With format %Y%m%d_%H%M%S For example, '20210831_123456.pt'
        model_files.sort(reverse=True)

        # print statements for debugging
        logger.info(f"artifact used: {model_files[0]}")

        return path_artifact / model_files[0]

    def _save_model_outputs(
        self,
        df_evaluation: pd.DataFrame,
        df_output: pd.DataFrame,
        path_generated: Union[str, Path],
    ) -> None:
        """
        Save the model outputs and evaluation metrics to the specified path.

        Args:
            df_evaluation (pd.DataFrame): DataFrame containing evaluation metrics.
            df_output (pd.DataFrame): DataFrame containing model outputs.
            path_generated (str or Path): The path where the outputs should be saved.
        """
        try:
            Path(path_generated).mkdir(parents=True, exist_ok=True)

            outputs_path = ModelManager._generate_output_file_name(path_generated,
                                                                   "output",
                                                                   self.config["steps"][-1],
                                                                   self.config["run_type"],
                                                                   self.config["timestamp"])
            evaluation_path = ModelManager._generate_output_file_name(path_generated,
                                                                      "evaluation",
                                                                      self.config["steps"][-1],
                                                                      self.config["run_type"],
                                                                      self.config["timestamp"])

            df_output.to_pickle(outputs_path)
            df_evaluation.to_pickle(evaluation_path)
        except Exception as e:
            logger.error(f"Error saving model outputs: {e}")

    def _save_predictions(
        self, df_predictions: pd.DataFrame, path_generated: Union[str, Path]
    ) -> None:
        """
        Save the model predictions to the specified path.

        Args:
            df_predictions (pd.DataFrame): DataFrame containing model predictions.
            path_generated (str or Path): The path where the predictions should be saved.
        """
        try:
            Path(path_generated).mkdir(parents=True, exist_ok=True)

            predictions_path = ModelManager._generate_output_file_name(path_generated,
                                                                       "predictions",
                                                                       self.config["steps"][-1],
                                                                       self.config["run_type"],
                                                                       self.config["timestamp"])
            df_predictions.to_pickle(predictions_path)
        except Exception as e:
            logger.error(f"Error saving predictions: {e}")

    @staticmethod
    def _generate_model_file_name(run_type: str, timestamp: str) -> str:
        """
        Generates a model file name based on the run type, and timestamp.

        Args:
            run_type (str): The type of run (e.g., calibration, testing).
            timestamp (str): The timestamp of the model file.

        Returns:
            str: The generated model file name.
        """

        return f"{run_type}_model_{timestamp}.pkl"

    @staticmethod
    def _generate_output_file_name(
            path_generated: Union[str, Path], generated_file_type, steps: int, run_type: str, timestamp: str) -> str:
        """
        Generates a prediction file name based on the run type, generated file type, steps, and timestamp.

        Args:
            path_generated (str or Path): The path where the predictions should be saved.
            generated_file_type (str): The type of generated file (e.g., predictions, output, evaluation).
            steps (int): The number of steps ahead for the forecast.
            run_type (str): The type of run (e.g., calibration, testing).

        Returns:
            str: The generated prediction file name.
        """

        path_generated = Path(path_generated)

        return f'{path_generated}/{generated_file_type}_{steps}_{run_type}_{timestamp}.pkl'



if __name__ == "__main__":
    model_path = ModelPath("lavender_haze")
    model_manager = ModelManager(model_path)
    print(model_manager._config_deployment)
    print(model_manager._config_hyperparameters)
    print(model_manager._config_meta)
    print(model_manager._config_sweep)
    # model_manager.execute_single_run("args")
    # ensemble_path = EnsemblePath("white_mustang")
    # ensemble_manager = ModelManager(ensemble_path)
    # print(ensemble_manager._config_deployment)
    # print(ensemble_manager._config_hyperparameters)
    # print(ensemble_manager._config_meta)
    # print(ensemble_manager._config_sweep)
