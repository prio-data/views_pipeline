import sys
from common_utils.model_path import ModelPath
from common_utils.global_cache import GlobalCache
from common_utils.ensemble_path import EnsemblePath
from typing import Union, Optional, List, Dict
from views_dataloader import ViewsDataLoader
import logging
import importlib
from pathlib import Path
import wandb
import pandas as pd
from views_forecasts.extensions import *
from views_partitioning.data_partitioner import DataPartitioner
from stepshift.views import StepshiftedModels
from common_utils.views_stepshift.run import ViewsRun
from common_utils.utils_wandb import add_wandb_monthly_metrics
from common_utils.utils_log_files import create_log_file, read_log_file

logger = logging.getLogger(__name__)
import time

# Temp
# from execute_model_tasks import execute_model_tasks
from evaluate_sweep import evaluate_sweep

class ModelManager:

    def __init__(
        self, model_path: Union[ModelPath, EnsemblePath], cli_args, **kwargs
    ) -> None:
        self._entity = "views_pipeline"
        self._model_path = model_path
        self._script_paths = self._model_path.get_scripts()
        # print(self._script_paths)
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
        self.data_loader = ViewsDataLoader(model_path=self._model_path)
        self.__state = {
            "training_complete": False,
            "evaluation_complete": False,
            "forecasting_complete": False,
            "calibration_complete": False,
        }
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.__args = cli_args
        self._aggregated_config = None
        self._wandb_config = None
        self._wandb_sweep_id = None
        self._data = None

    def __load_config(self, script_name, config_method) -> Union[Dict, None]:
        """
        Loads and executes a configuration method from a specified script.

        args:
            script_name (str): The name of the script to load.
            config_method (str): The name of the configuration method to execute.

        Returns:
            The result of the configuration method if the script and method are found, otherwise None.

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
                else:
                    logger.error(f"Method {config_method} not found in {script_name}")
                    return None
            except (ImportError, AttributeError) as e:
                logger.error(f"Error loading config from {script_name}: {e}")
                return None
        else:
            logger.error(f"Script path for {script_name} not found")
            return None

    # def execute_sweep_run(self, __args):
    #     sweep_config = get_sweep_config()
    #     meta_config = get_meta_config()
    #     update_sweep_config(sweep_config, __args, meta_config)

    #     project = f"{self._config_sweep['name']}_sweep"  # we can name the sweep in the config file

    #     sweep_id = wandb.sweep(self._config_sweep, project=project, entity=self._entity)

    #     with wandb.init(project=f'{project}_fetch', entity=self._entity):

    #         data_loader = DataLoader(model_path=ModelPath(Path(__file__)))
    #         data_loader.get_data(use_saved=__args.saved, validate=True, self_test=__args.drift_self_test, partition=__args.run_type)

    #     wandb.finish()

    #     wandb.agent(sweep_id, execute_model_tasks, entity='views_pipeline')

    def _aggregate_configs(self) -> Dict:
        """
        Aggregates configuration settings from various sources into a single dictionary.

        Returns:
            Dict: A dictionary containing the aggregated configuration settings.
        """
        if self.__args.sweep:
            self._config_sweep["parameters"]["run_type"] = {"value": self.__args.run_type}
            self._config_sweep["parameters"]["sweep"] = {"value": True}
            self._config_sweep["parameters"]["name"] = {"value": self._config_meta["name"]}
            self._config_sweep["parameters"]["depvar"] = {"value": self._config_meta["depvar"]}
            self._config_sweep["parameters"]["algorithm"] = {"value": self._config_meta["algorithm"]}
            if self._config_meta["algorithm"] == "HurdleRegression":
                self._config_sweep["parameters"]["model_clf"] = {"value": self._config_meta["model_clf"]}
                self._config_sweep["parameters"]["model_reg"] = {"value": self._config_meta["model_reg"]}
            # return self._config_sweep
        
        _config = self._config_hyperparameters.copy()
        if self.__args is not None:
            _config["run_type"] = self.__args.run_type
            _config["sweep"] = self.__args.sweep
        _config["name"] = self._config_meta["name"]
        _config["depvar"] = self._config_meta["depvar"]
        _config["algorithm"] = self._config_meta["algorithm"]
        if self._config_meta["algorithm"] == "HurdleRegression":
             _config["model_clf"] = self._config_meta["model_clf"]
             _config["model_reg"] = self._config_meta["model_reg"]
        _config["deployment_status"] = self._config_deployment["deployment_status"]
        return _config

    @staticmethod
    def wandb_session(stage):
        """
        A static method decorator to initialize and finalize a Weights and Biases (wandb) session for a given stage.

        __args:
            stage (str): The stage of the project (e.g., 'train', 'test', 'validate') to be appended to the project name.

        Returns:
            function: A decorator function that wraps the given function with wandb session initialization and finalization.

        The decorator function:
            - Aggregates configuration settings.
            - Sets the project name using the configuration name and run type.
            - Initializes a wandb session with the project name and entity.
            - Executes the wrapped function.
            - Finalizes the wandb session.
        """

        def decorator(func):
            def wrapper(self):
                # if self._aggregated_config is None:
                self._aggregated_config = self._aggregate_configs()
                self._project = (
                    f"{self._aggregated_config['name']}_{self.__args.run_type}"
                )
                start_t = time.time()

                with wandb.init(
                    project=f"{self._project}_{stage}",
                    entity=self._entity,
                    config=self._aggregated_config,
                ):
                    print(self._aggregated_config)
                    result = func(self)
                wandb.finish()
                if self.__args.sweep:
                    # if self._wandb_sweep_id is None:
                    self._wandb_sweep_id = wandb.sweep(
                        self._config_sweep, project=self._project, entity=self._entity
                    )
                    # self._wandb_sweep_id = wandb.sweep(sweep_config, project=project, entity="views_pipeline")
                    wandb.agent(self._wandb_sweep_id, self.train(), entity=self._entity)

                end_t = time.time()
                minutes = (end_t - start_t) / 60
                logger.info(f"Done. Runtime: {minutes:.3f} minutes.\n")
                return result

            return wrapper

        return decorator

    #################################
    # STAGE 1: Fetch Data           #
    #################################

    @wandb_session(stage="fetch")
    def get_data(self):  # Overridable
        self.data_loader.get_data(
            use_saved=self.__args.saved,
            validate=True,
            self_test=self.__args.drift_self_test,
            partition=self.__args.run_type,
        )
        self._data = pd.read_pickle(
            self._model_path.data_raw / f"{self.__args.run_type}_viewser_df.pkl"
        )

    #################################
    # STAGE 2: Preprocess Data      #
    #################################

    @wandb_session(stage="preprocessing")
    def preprocess(self):  # Overridable
        pass

    # def __get_parameters(self):
    #     """
    #     Get the parameters from the config file.
    #     If not sweep, then get directly from the config file, otherwise have to remove some parameters.
    #     """

    #     if self._aggregated_config["sweep"]:
    #         keys_to_remove = [
    #             "algorithm",
    #             "depvar",
    #             "steps",
    #             "sweep",
    #             "run_type",
    #             "model_cls",
    #             "model_reg",
    #         ]
    #         parameters = {
    #             k: v
    #             for k, v in self._aggregated_config.items()
    #             if k not in keys_to_remove
    #         }
    #     else:
    #         parameters = self._aggregated_config["parameters"]
    #     return parameters

    #################################
    # STAGE 3: Get Model            #
    #################################

    def get_model(self):
        """
        Get the model based on the algorithm specified in the config.
        """

        if self._aggregated_config["algorithm"] == "HurdleRegression":
            from common_utils.views_stepshifter_darts.hurdle_model import HurdleModel
            return HurdleModel(
                self._aggregated_config, self.data_loader.partition_dict
            )
        else:
            self._aggregated_config["model_reg"] = self._aggregated_config["algorithm"]
            from common_utils.views_stepshifter_darts.stepshifter import (
                StepshifterModel,
            )
            return StepshifterModel(
                self._aggregated_config, self.data_loader.partition_dict
            )


    def _split_hurdle_parameters(self, parameters_dict):
        """
        Split the parameters dictionary into two separate dictionaries, one for the
        classification model and one for the regression model.
        """

        cls_dict = {}
        reg_dict = {}

        for key, value in parameters_dict.items():
            if key.startswith("cls_"):
                cls_key = key.replace("cls_", "")
                cls_dict[cls_key] = value
            elif key.startswith("reg_"):
                reg_key = key.replace("reg_", "")
                reg_dict[reg_key] = value

        return cls_dict, reg_dict

    #################################
    # STAGE 4: Train Model          #
    #################################    

    def stepshift_training(self):
        stepshift_model = self.get_model()
        stepshift_model.fit(self._data)
        if not self._wandb_config["sweep"]:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_filename = f"{self.__args.run_type}_model_{timestamp}.pkl"
            stepshift_model.save(self._model_path.artifacts / model_filename)
            date_fetch_timestamp = read_log_file(self._model_path.data_raw / f"{self.__args.run_type}_data_fetch_log.txt").get("Data Fetch Timestamp", None)
            create_log_file(self._model_path.data_generated, self._aggregated_config, timestamp, None, date_fetch_timestamp)
        return stepshift_model

    @wandb_session(stage="train")
    def train(self):
        # from utils_run import get_model, split_hurdle_parameters
        # start_t = time.time()
        from train_model import train_model_artifact
        
        self._wandb_config = wandb.config
        print(self._wandb_config)
        if (
            self._wandb_config["sweep"]
            and self._wandb_config["algorithm"] == "HurdleRegression"
        ):
            self._wandb_config["parameters"] = {}
            (
                self._wandb_config["parameters"]["clf"],
                self._wandb_config["parameters"]["reg"],
            ) = self._split_hurdle_parameters(self._wandb_config)

        if self._wandb_config["sweep"]:
            logger.info(f"Sweeping model {self._wandb_config['name']}...")
            stepshift_model = self.stepshift_training()
            logger.info(f"Evaluating model {self._wandb_config['name']}...")
            evaluate_sweep(self._wandb_config, stepshift_model)

        # Handle the single model runs: train and save the model as an artifact
        if self.__args.train:
            logger.info(f"Training model {self._wandb_config['name']}...")
            train_model_artifact(self._wandb_config)
            ## Actual training
            # stepshift_model = self.stepshift_training()
            
        # end_t = time.time()
        # minutes = (end_t - start_t) / 60
        # logger.info(f"Done. Runtime: {minutes:.3f} minutes.\n")

        self.evaluate()
        self.forecast()
        

    @wandb_session(stage="testing")
    def evaluate(self):
        from evaluate_model import evaluate_model_artifact
        # Handle the single model runs: evaluate a trained model (artifact)
        if self.__args.evaluate:
            logger.info(f"Evaluating model {self._wandb_config['name']}...")
            evaluate_model_artifact(self._wandb_config, self.__args.artifact_name)

    # @wandb_session(stage="testing")
    # def evaluate_sweep(self):
    #     from evaluate_sweep import evaluate_sweep
    #     evaluate_sweep(self._wandb_config, self.stepshift_model)
    
    @wandb_session(stage="forecasting")
    def forecast(self):
        from generate_forecast import forecast_model_artifact
        if self.__args.forecast:
            logger.info(f"Forecasting model {self._wandb_config['name']}...")
            forecast_model_artifact(self._wandb_config, self.__args.artifact_name)

    def start(self):  # To be deleted. This is just for testing.
        self.get_data()
        self.preprocess()
        self.train()
        self.evaluate()
        self.forecast()
