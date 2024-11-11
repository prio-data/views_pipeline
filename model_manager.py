import sys
from abc import abstractmethod
from common_utils.model_path import ModelPath
from common_utils.global_cache import GlobalCache
from common_utils.ensemble_path import EnsemblePath
from common_utils.utils_wandb import add_wandb_monthly_metrics
from typing import Union, Optional, List, Dict
from dataloaders import DataLoader
import logging
import importlib
import wandb
import time

logger = logging.getLogger(__name__)


# Temp
# from execute_model_tasks import execute_model_tasks

class ModelManager:

    def __init__(self, model_path: Union[ModelPath, EnsemblePath]) -> None:
        self._entity = "views_pipeline"
        self._model_path = model_path
        self._script_paths = self._model_path.get_scripts()
        self._config_deployment = self.__load_config("config_deployment.py", "get_deployment_config")
        self._config_hyperparameters = self.__load_config("config_hyperparameters.py", "get_hp_config")
        self._config_meta = self.__load_config("config_meta.py", "get_meta_config")
        if self._model_path.target == "model":
            self._config_sweep = self.__load_config("config_sweep.py", "get_sweep_config")
        self._data_loader = DataLoader(model_path=self._model_path)
        self.__state = {"training_complete": False, "evaluation_complete": False, "forecasting_complete": False, "calibration_complete": False}

    def __load_config(self, script_name, config_method) -> Union[Dict, None]:
        """
        Loads and executes a configuration method from a specified script.

        Args:
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
    
    def _update_single_config(self, args):
        '''
        Updates the configuration object with config_hyperparameters, config_meta, config_deployment, and the command line arguments.
        
        Args:
            args: Command line arguments.

        Returns:
            The updated configuration object.
        '''
        config = {**self._config_hyperparameters, **self._config_meta, **self._config_deployment}
        config["run_type"] = args.run_type
        config["sweep"] = False

        return config
    
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
    
        return config

    def execute_single_run(self, args):

        self.config = self._update_single_config(args)
        
        self._project = f"{self.config['name']}_{args.run_type}"

        with wandb.init(project=f'{self._project}_fetch', entity=self._entity):

            self._data_loader.get_data(use_saved=args.saved, validate=True, self_test=args.drift_self_test, partition=args.run_type)

        wandb.finish()

        self._execute_model_tasks(train=args.train, eval=args.evaluate, forecast=args.forecast, artifact_name=args.artifact_name)

            
    def execute_sweep_run(self, args):
        self.config = self._update_sweep_config(args)

        self._project = f"{self.config['name']}_sweep" 

        sweep_id = wandb.sweep(self.config, project=self._project, entity=self._entity)

        with wandb.init(project=f'{self._project}_fetch', entity=self._entity):

            self._data_loader.get_data(use_saved=args.saved, validate=True, self_test=args.drift_self_test, partition=args.run_type)

        wandb.finish()

        wandb.agent(sweep_id, self._execute_model_tasks, entity=self._entity)
            

    def _execute_model_tasks(self, train=None, eval=None, forecast=None, artifact_name=None):
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
        with wandb.init(project=self._project, entity=self._entity,
                        config=self.config):  # project and config ignored when running a sweep

            # add the monthly metrics to WandB
            add_wandb_monthly_metrics()

            # Update config from WandB initialization above
            self.config = wandb.config

            if self.config["sweep"]:
                logger.info(f"Sweeping model {self.config['name']}...")
                model = self._train_model_artifact()
                logger.info(f"Evaluating model {self.config['name']}...")
                self._evaluate_sweep(model)

            if train:
                logger.info(f"Training model {self.config['name']}...")
                self._train_model_artifact(self)

            if eval:
                logger.info(f"Evaluating model {self.config['name']}...")
                self._evaluate_model_artifact(artifact_name)

            if forecast:
                logger.info(f"Forecasting model {self.config['name']}...")
                self._forecast_model_artifact(artifact_name)

            end_t = time.time()
            minutes = (end_t - start_t) / 60
            logger.info(f"Done. Runtime: {minutes:.3f} minutes.\n")

    @abstractmethod
    def _train_model_artifact(self):
        pass
    
    @abstractmethod
    def _evaluate_model_artifact(self, artifact_name):
        pass

    @abstractmethod
    def _forecast_model_artifact(self, artifact_name):
        pass

    @abstractmethod
    def _evaluate_sweep(self, model):
        pass



if "main" in __name__:
    model_path = ModelPath("lavender_haze")
    model_manager = ModelManager(model_path)
    print(model_manager.config_deployment)
    print(model_manager.config_hyperparameters)
    print(model_manager.config_meta)
    print(model_manager.config_sweep)
    # model_manager.execute_single_run("args")
    # ensemble_path = EnsemblePath("white_mustang")
    # ensemble_manager = ModelManager(ensemble_path)
    # print(ensemble_manager.config_deployment)
    # print(ensemble_manager.config_hyperparameters)
    # print(ensemble_manager.config_meta)
    # print(ensemble_manager.config_sweep)