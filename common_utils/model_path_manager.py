import yaml
import logging
import pickle  # Use pickle instead of json
import os
from pathlib import Path
from string import Template
from typing import Any, Dict

logger = logging.getLogger(__name__)

class ModelPathManager:

    current_path = Path(__file__).resolve()
    pipeline_root = Path(*current_path.parts[:current_path.parts.index("views_pipeline") + 1])
    _cache_dir = pipeline_root / "common_cache"  # Directory to store cache files

    def __init__(self, model_name: str, config_file: str = 'model_dir_structure.yaml'):
        self.model_name = model_name
        self.config_file = config_file
        self._initialized = False
        self.paths = {}

        # Try to load from the pickle cache file
        if not self._load_from_cache():
            # If not in cache, initialize normally
            self._discover_pipeline_root()
            self._load_config(config_file)
            self._build_paths()
            self._initialized = True
            # Save to cache
            self._save_to_cache()

    def _discover_pipeline_root(self):
        """
        Discover the root directory of the pipeline by finding the 'views_pipeline' directory
        in the current file path.
        """
        current_path = Path(__file__).resolve()
        if "views_pipeline" in current_path.parts:
            self.pipeline_root = Path(*current_path.parts[:current_path.parts.index("views_pipeline") + 1])
            logger.debug(f"Discovered pipeline root: {self.pipeline_root}")
        else:
            raise ValueError("The 'views_pipeline' directory was not found in the provided path.")

    def _load_config(self, config_file: str):
        """
        Load the YAML configuration file containing the directory structure.
        """
        config_file_path = self.pipeline_root / "meta_tools/templates" / config_file  # Adjust the path as needed

        try:
            with open(config_file_path, 'r') as f:
                self.config_data = yaml.safe_load(f)
                self.path_templates = self.config_data.get('paths', {})
                logger.debug(f"Loaded configuration from {config_file_path}")
        except Exception as e:
            logger.error(f"Failed to load configuration file '{config_file_path}': {e}")
            raise

    def _build_paths(self):
        """
        Build the paths by replacing placeholders in the configuration with actual values
        and set them as attributes of the class, handling nested dictionaries.
        """
        # Initialize placeholders
        self.variables = {
            'pipeline_root': str(self.pipeline_root),
            'model_name': self.model_name,
            'models': str(self.pipeline_root / "models"),
        }
        self.paths = {}
        self._assign_paths(self.path_templates)

    def _assign_paths(self, path_templates: Dict[str, Any], parent_key: str = ''):
        """
        Recursively replace placeholders and set paths as attributes.
        """
        for key, template in path_templates.items():
            attr_name = f"{parent_key}_{key}" if parent_key else key

            if isinstance(template, dict):
                # Recursively handle nested dictionaries
                self._assign_paths(template, attr_name)
            elif template is None:
                setattr(self, attr_name, None)
                self.paths[attr_name] = None
                logger.debug(f"Set attribute '{attr_name}' to None")
            elif isinstance(template, str):
                try:
                    # Substitute placeholders
                    substituted_path_str = self._substitute_placeholders(template)
                    path_obj = Path(substituted_path_str)

                    # Resolve relative paths
                    if not path_obj.is_absolute():
                        absolute_path = (self.model_dir / path_obj).resolve()
                    else:
                        absolute_path = path_obj.resolve()

                    # Assign the attribute
                    setattr(self, attr_name, absolute_path)
                    self.paths[attr_name] = absolute_path
                    logger.debug(f"Set attribute '{attr_name}' to {absolute_path}")

                    # Update variables for future substitutions
                    self.variables[attr_name] = str(absolute_path)

                except KeyError as e:
                    logger.error(f"Missing placeholder for '{attr_name}': {e}")
                    raise
                except Exception as e:
                    logger.error(f"Error assigning path for '{attr_name}': {e}")
                    raise
            else:
                logger.warning(f"Unsupported template type for '{attr_name}': {type(template)}")

    def _substitute_placeholders(self, template_str: str) -> str:
        """
        Substitute placeholders in a template string using current variables.

        Args:
            template_str (str): The template string with placeholders.

        Returns:
            str: The string with placeholders substituted.

        Raises:
            KeyError: If a placeholder is missing in variables.
        """
        template = Template(template_str)
        substituted_str = template.safe_substitute(self.variables)
        return substituted_str

    def _save_to_cache(self):
        """
        Serialize the instance data and save it to a pickle file.
        """
        try:
            os.makedirs(self._cache_dir, exist_ok=True)
            cache_file = os.path.join(self._cache_dir, f"{self.model_name}.pkl")

            with open(cache_file, 'wb') as f:
                pickle.dump(self, f)
            logger.info(f"Saved instance to cache file: {cache_file}")
        except Exception as e:
            logger.error(f"Failed to save instance to cache file: {e}")
            # Optionally, handle or re-raise the exception

    def _load_from_cache(self) -> bool:
        """
        Attempt to load the instance data from a pickle cache file.

        Returns:
            bool: True if the instance was successfully loaded from cache, False otherwise.
        """
        try:
            cache_file = os.path.join(self._cache_dir, f"{self.model_name}.pkl")
            if os.path.exists(cache_file):
                with open(cache_file, 'rb') as f:
                    cached_instance = pickle.load(f)

                # Update the current instance's __dict__ with the cached instance's __dict__
                self.__dict__.update(cached_instance.__dict__)

                logger.info(f"Loaded instance from cache file: {cache_file}")
                return True
            else:
                logger.info(f"No cache file found for model_name: {self.model_name}")
                return False
        except Exception as e:
            logger.error(f"Failed to load instance from cache file: {e}")
            return False

    def validate_paths(self):
        """
        Validate that all paths set as attributes exist on the filesystem.
        """
        missing_paths = []
        for attr, path in self.paths.items():
            if isinstance(path, Path) and not path.exists():
                missing_paths.append((attr, path))
        if missing_paths:
            logger.warning("The following paths do not exist:")
            for attr, path in missing_paths:
                logger.warning(f"- {attr}: {path}")
        else:
            logger.info("All paths exist.")

    def create_paths(self):
        """
        Create directories for all paths that do not exist.
        """
        for attr, path in self.paths.items():
            if isinstance(path, Path) and not path.exists():
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    logger.info(f"Created directory: {path}")
                except Exception as e:
                    logger.error(f"Failed to create directory '{path}': {e}")

    def get_model_specific_queryset(self) -> Path:
        """
        Get the path to the model-specific queryset file from the common_querysets directory.

        Returns:
            Path: The path to the model-specific queryset file.

        Raises:
            FileNotFoundError: If the queryset file does not exist.
        """
        queryset_filename = f"queryset_{self.model_name}.py"  # Assuming the queryset files are .py files
        queryset_path = self.common_querysets / queryset_filename

        if not queryset_path.exists():
            logger.error(f"Queryset file not found: {queryset_path}")
            raise FileNotFoundError(f"Queryset file not found: {queryset_path}")

        logger.debug(f"Model-specific queryset path: {queryset_path}")
        return queryset_path

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    try:
        # First instantiation
        model_paths1 = ModelPathManager(model_name="purple_alien")
        print(f"First instance model_dir: {model_paths1.model_dir}")

        # Second instantiation (should load from cache)
        model_paths2 = ModelPathManager(model_name="purple_alien")
        print(f"Second instance model_dir: {model_paths2.model_dir}")

        # Check if both instances have the same data
        print(f"Paths are equal: {model_paths1.paths == model_paths2.paths}")

        # Third instantiation with a different model_name
        model_paths3 = ModelPathManager(model_name="orange_pasta")
        print(f"Third instance model_dir: {model_paths3.model_dir}")

       # Access attributes
        print(f"Pipeline root: {model_paths1.pipeline_root}")
        print(f"Model directory: {model_paths1.model_dir}")
        print(f"Architectures directory: {model_paths1.architectures}")
        print(f"Common querysets directory: {model_paths1.common_querysets}")
        print(f"Common cache directory: {model_paths1.common_cache}")
        # Get model-specific queryset
        queryset_path = model_paths1.get_model_specific_queryset()
        print(f"Model-specific queryset path: {queryset_path}")
        # Validate paths
        model_paths1.validate_paths()
        # Optionally create missing directories
        # model_paths.create_paths()

    except Exception as e:
        logger.error(f"Failed to initialize ModelPathManager: {e}")