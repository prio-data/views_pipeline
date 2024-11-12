import sys
from abc import abstractmethod
from common_utils.model_path import ModelPath
from common_utils.ensemble_path import EnsemblePath
from wandb_utils import WandbUtils
from typing import Union, Optional, List, Dict
from views_pipeline.data.dataloaders import ViewsDataLoader
import logging
import importlib
import wandb
import time
import pickle
import pandas as pd
from pathlib import Path


logger = logging.getLogger(__name__)




# ============================================================ Model Manager ============================================================


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
        self._data_loader = ViewsDataLoader(model_path=self._model_path)
        # self.__state = {"training_complete": False, "evaluation_complete": False, "forecasting_complete": False, "calibration_complete": False}

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

        self._execute_model_tasks(config=self.config, train=args.train, eval=args.evaluate, forecast=args.forecast, artifact_name=args.artifact_name)

            
    def execute_sweep_run(self, args):

        self.config = self._update_sweep_config(args)

        self._project = f"{self.config['name']}_sweep" 

        with wandb.init(project=f'{self._project}_fetch', entity=self._entity):

            self._data_loader.get_data(use_saved=args.saved, validate=True, self_test=args.drift_self_test, partition=args.run_type)

        wandb.finish()

        sweep_id = wandb.sweep(self.config, project=self._project, entity=self._entity)

        wandb.agent(sweep_id, self._execute_model_tasks, entity=self._entity)
            

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
        with wandb.init(project=self._project, entity=self._entity,
                        config=config):  # project and config ignored when running a sweep

            # add the monthly metrics to WandB
            WandbUtils.add_wandb_monthly_metrics()

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

    def _get_artifact_files(self, path_artifact, run_type):
        """
        Retrieve artifact files from a directory that match the given run type and common extensions.

        Args:
            path (str): The directory path where model files are stored.
            run_type (str): The type of run (e.g., calibration, testing).

        Returns:
            list: List of matching model file paths.
        """
        common_extensions = ['.pt', '.pth', '.h5', '.hdf5', '.pkl', '.json', '.bst', '.txt', '.bin', '.cbm', '.onnx']

        # Retrieve files that start with run_type and end with any of the common extensions
        # artifact_files = [f for f in os.listdir(PATH) if f.startswith(f"{run_type}_model_") and any(f.endswith(ext) for ext in common_extensions)]
        
        artifact_files = [f for f in path_artifact.iterdir() if f.is_file() and f.stem.startswith(f"{run_type}_model_") and f.suffix in common_extensions]

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
            raise FileNotFoundError(f"No model artifacts found for run type '{run_type}' in path '{path_artifact}'")
        
        # Sort the files based on the timestamp embedded in the filename. With format %Y%m%d_%H%M%S For example, '20210831_123456.pt'
        model_files.sort(reverse=True)

        #print statements for debugging
        logger.info(f"artifact used: {model_files[0]}")

        PATH_MODEL_ARTIFACT = path_artifact / model_files[0]

        return PATH_MODEL_ARTIFACT
    
    def _save_model_outputs(self, df_evaluation: pd.DataFrame, df_output: pd.DataFrame, path_generated: str | Path):
        '''
        Save the model outputs and evaluation metrics to the specified path
        '''

        Path(path_generated).mkdir(parents=True, exist_ok=True)

        # Save the DataFrame of model outputs
        outputs_path = f'{path_generated}/output_{self.config["steps"][-1]}_{self.config["run_type"]}_{self.config["timestamp"]}.pkl'
        with open(outputs_path, "wb") as file:
            pickle.dump(df_output, file)
        logger.info(f"Model outputs saved at: {outputs_path}")

        # Save the DataFrame of evaluation metrics
        evaluation_path = f'{path_generated}/evaluation_{self.config["steps"][-1]}_{self.config["run_type"]}_{self.config["timestamp"]}.pkl'
        with open(evaluation_path, "wb") as file:
            pickle.dump(df_evaluation, file)
        logger.info(f"Evaluation metrics saved at: {evaluation_path}")


    def _save_predictions(self, df_predictions: pd.DataFrame, path_generated: str | Path):
        '''
        Save the model predictions to the specified path
        '''
        
        Path(path_generated).mkdir(parents=True, exist_ok=True)

        predictions_path = f'{path_generated}/predictions_{self.config["steps"][-1]}_{self.config["run_type"]}_{self.config["timestamp"]}.pkl'
        with open(predictions_path, "wb") as file:
            pickle.dump(df_predictions, file)
        logger.info(f"Predictions saved at: {predictions_path}")







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