import sys
print(sys.path)
from common_utils.model_path import ModelPath
from common_utils.global_cache import GlobalCache
from common_utils.ensemble_path import EnsemblePath
from typing import Union, Optional, List, Dict
from dataloaders import DataLoaders
import logging
import importlib

logger = logging.getLogger(__name__)


class ModelManager:

    def __init__(self, model_path: Union[ModelPath, EnsemblePath]) -> None:
        self.model_path = model_path
        self._script_paths = model_path.get_scripts()
        self.config_deployment = self.__load_config("config_deployment.py", "get_deployment_config")
        self.config_hyperparameters = self.__load_config("config_hyperparameters.py", "get_hp_config")
        self.config_meta = self.__load_config("config_meta.py", "get_meta_config")
        if self.model_path.target == "model":
            self.config_sweep = self.__load_config("config_sweep.py", "get_sweep_config")
        else:
            self.config_sweep = None
        # self._data_loader = DataLoaders(model_path=self.model_path, partition=)

    def __load_config(self, script_name, config_method) -> Optional[Dict]:
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
        
    # STAGE 1: Data Fetching

        
if "main" in __name__:
    model_path = ModelPath("orange_pasta")
    model_manager = ModelManager(model_path)
    print(model_manager.config_deployment)
    print(model_manager.config_hyperparameters)
    print(model_manager.config_meta)
    print(model_manager.config_sweep)
    ensemble_path = EnsemblePath("white_mustang")
    ensemble_manager = ModelManager(ensemble_path)
    print(ensemble_manager.config_deployment)
    print(ensemble_manager.config_hyperparameters)
    print(ensemble_manager.config_meta)
    print(ensemble_manager.config_sweep)