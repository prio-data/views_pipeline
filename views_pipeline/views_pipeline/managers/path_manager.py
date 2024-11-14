from pathlib import Path
import sys
import logging
import importlib
import hashlib
from typing import Union, Optional, List, Dict
import re

logger = logging.getLogger(__name__)

# ============================================================ ModelPath ============================================================

class ModelPath:
    """
    A class to manage model paths and directories within the ViEWS Pipeline.

    Attributes:
        __instances__ (int): A class-level counter to track the number of ModelPath instances.
        model_name (str): The name of the model.
        _validate (bool): A flag to indicate whether to validate paths and names.
        target (str): The target type (e.g., 'model').
        _force_cache_overwrite (bool): A flag to indicate whether to force overwrite the cache.
        root (Path): The root directory of the project.
        models (Path): The directory for models.
        common_utils (Path): The directory for common utilities.
        common_configs (Path): The directory for common configurations.
        model_dir (Path): The directory for the specific model.
        architectures (Path): The directory for model architectures.
        artifacts (Path): The directory for model artifacts.
        configs (Path): The directory for model configurations.
        data (Path): The directory for model data.
        data_generated (Path): The directory for generated data.
        data_processed (Path): The directory for processed data.
        data_raw (Path): The directory for raw data.
        dataloaders (Path): The directory for data loaders.
        forecasting (Path): The directory for forecasting scripts.
        management (Path): The directory for management scripts.
        notebooks (Path): The directory for notebooks.
        offline_evaluation (Path): The directory for offline evaluation scripts.
        online_evaluation (Path): The directory for online evaluation scripts.
        reports (Path): The directory for reports.
        src (Path): The source directory.
        _templates (Path): The directory for templates.
        training (Path): The directory for training scripts.
        utils (Path): The directory for utility scripts.
        visualization (Path): The directory for visualization scripts.
        _sys_paths (list): A list of system paths.
        common_querysets (Path): The directory for common querysets.
        queryset_path (Path): The path to the queryset script.
        _queryset (module): The imported queryset module.
        scripts (list): A list of script paths.
        _ignore_attributes (list): A list of paths to ignore.
    """

    _target = "model"
    _use_global_cache = True
    __instances__ = 0
    # Class variables for paths
    _root = None
    # _common_utils = None
    # _common_configs = None
    # _common_querysets = None
    # _meta_tools = None

    @classmethod
    def _initialize_class_paths(cls):
        """Initialize class-level paths."""
        cls._root = cls.find_project_root()
        # cls._models = cls._root / Path(cls._target + "s")
        # cls._common_utils = cls._root / "common_utils"
        # cls._common_configs = cls._root / "common_configs"
        # cls._common_querysets = cls._root / "common_querysets"
        # cls._meta_tools = cls._root / "meta_tools"
        # cls._common_logs = cls._root / "common_logs"

    @classmethod
    def get_root(cls) -> Path:
        """Get the root path."""
        if cls._root is None:
            cls._initialize_class_paths()
        return cls._root

    @classmethod
    def get_models(cls) -> Path:
        """Get the models path."""
        if cls._root is None:
            cls._initialize_class_paths()
        return cls._root / Path(cls._target + "s")

    # @classmethod
    # def get_common_utils(cls) -> Path:
    #     """Get the common utils path."""
    #     if cls._common_utils is None:
    #         cls._initialize_class_paths()
    #     return cls._common_utils

    # @classmethod
    # def get_common_configs(cls) -> Path:
    #     """Get the common configs path."""
    #     if cls._common_configs is None:
    #         cls._initialize_class_paths()
    #     return cls._common_configs

    # @classmethod
    # def get_common_querysets(cls) -> Path:
    #     """Get the common querysets path."""
    #     if cls._common_querysets is None:
    #         cls._initialize_class_paths()
    #     return cls._common_querysets

    # @classmethod
    # def get_meta_tools(cls) -> Path:
    #     """Get the meta tools path."""
    #     if cls._meta_tools is None:
    #         cls._initialize_class_paths()
    #     return cls._meta_tools

    # @classmethod
    # def get_common_logs(cls) -> Path:
    #     """Get the common logs path."""
    #     if cls._common_logs is None:
    #         cls._initialize_class_paths()
    #     return cls._common_logs

    @classmethod
    def check_if_model_dir_exists(cls, model_name: str) -> bool:
        """
        Check if the model directory exists.

        Args:
            cls (type): The class calling this method.
            model_name (str): The name of the model.

        Returns:
            bool: True if the model directory exists, False otherwise.
        """
        model_dir = cls.get_models() / model_name
        return model_dir.exists()

    @staticmethod
    def generate_hash(model_name: str, validate: bool, target: str) -> str:
        """
        Generates a unique hash for the ModelPath instance.

        Args:
            model_name_or_path (str or Path): The model name or path.
            validate (bool): Whether to validate paths and names.
            target (str): The target type (e.g., 'model').

        Returns:
            str: The SHA-256 hash of the model name, validation flag, and target.
        """
        return hashlib.sha256(str((model_name, validate, target)).encode()).hexdigest()

    @staticmethod
    def get_model_name_from_path(path: Union[Path, str]) -> str:
        """
        Returns the model name based on the provided path.

        Args:
            PATH (Path): The base path, typically the path of the script invoking this function (e.g., `Path(__file__)`).

        Returns:
            str: The model name extracted from the provided path.

        Raises:
            ValueError: If the model name is not found in the provided path.
        """
        path = Path(path)
        logger.debug(f"Extracting model name from Path: {path}")
        if "models" in path.parts and "ensembles" not in path.parts:
            model_idx = path.parts.index("models")
            model_name = path.parts[model_idx + 1]
            if ModelPath.validate_model_name(model_name):
                logger.debug(f"Valid model name {model_name} found in path {path}")
                return str(model_name)
            else:
                logger.debug(f"No valid model name found in path {path}")
                return None
        if "ensembles" in path.parts and "models" not in path.parts:
            model_idx = path.parts.index("ensembles")
            model_name = path.parts[model_idx + 1]
            if ModelPath.validate_model_name(model_name):
                logger.debug(f"Valid ensemble name {model_name} found in path {path}")
                return str(model_name)
            else:
                logger.debug(f"No valid ensemble name found in path {path}")
                return None
        return None
    
    @staticmethod
    def validate_model_name(name: str) -> bool:
        """
        Validates the model name to ensure it follows the lowercase "adjective_noun" format.

        Parameters:
            name (str): The model name to validate.

        Returns:
            bool: True if the name is valid, False otherwise.
        """
        # Define a basic regex pattern for a noun_adjective format
        pattern = r"^[a-z]+_[a-z]+$"
        # Check if the name matches the pattern
        if re.match(pattern, name):
            # You might want to add further checks for actual noun and adjective validation
            # For now, this regex checks for two words separated by an underscore
            return True
        return False
    
    @staticmethod
    def find_project_root(marker="LICENSE.md") -> Path:
        """
        Finds the base directory of the project by searching for a specific marker file or directory.
        Args:
            marker (str): The name of the marker file or directory that indicates the project root.
                        Defaults to 'LICENSE.md'.
        Returns:
            Path: The path of the project root directory.
        Raises:
            FileNotFoundError: If the marker file/directory is not found up to the root directory.
        """
        # Start from the current directory and move up the hierarchy
        current_path = Path(__file__).resolve().parent
        while current_path != current_path.parent:  # Loop until we reach the root directory
            if (current_path / marker).exists():
                return current_path
            current_path = current_path.parent
        raise FileNotFoundError(
            f"{marker} not found in the directory hierarchy. Unable to find project root."
        )

    def __init__(
        self, model_name_or_path: Union[str, Path], validate: bool = True
    ) -> None:
        """
        Initializes a ModelPath instance.

        Args:
            model_name_or_path (str or Path): The model name or path.
            validate (bool, optional): Whether to validate paths and names. Defaults to True.
            target (str, optional): The target type (e.g., 'model'). Defaults to 'model'.
        """

        # Configs
        self.__class__.__instances__ += 1

        self._validate = validate
        self.target = self.__class__._target

        # DO NOT USE GLOBAL CACHE FOR NOW
        self.use_global_cache = self.__class__._use_global_cache
        self._force_cache_overwrite = False

        # Common paths
        self.root = self.__class__.get_root()
        self.models = self.__class__.get_models()
        # self.common_utils = self.__class__.get_common_utils()
        # self.common_configs = self.__class__.get_common_configs()
        # self.common_querysets = self.__class__.get_common_querysets()
        # self.meta_tools = self.__class__.get_meta_tools()
        # Ignore attributes while processing
        self._ignore_attributes = [
            "model_name",
            "model_dir",
            "scripts",
            "_validate",
            "models",
            "_sys_paths",
            "queryset_path",
            "_queryset",
            "_ignore_attributes",
            "target",
            "_force_cache_overwrite",
            "_instance_hash",
            "use_global_cache",
        ]

        self.model_name = self._process_model_name(model_name_or_path)
        self._instance_hash = self.generate_hash(
            self.model_name, self._validate, self.target
        )

        if self.use_global_cache:
            self._handle_global_cache()

        self._initialize_directories()
        self._initialize_scripts()
        logger.debug(
            f"ModelPath instance {ModelPath.__instances__} initialized for {self.model_name}."
        )

        if self.use_global_cache:
            self._write_to_global_cache()

    def _process_model_name(self, model_name_or_path: Union[str, Path]) -> str:
        """
        Processes the input model name or path and returns a valid model name.

        If the input is a path, it extracts the model name from the path.
        If the input is a model name, it validates the name format.

        Args:
            model_name_or_path (Union[str, Path]): The model name or path to process.

        Returns:
            str: The processed model name.

        Raises:
            ValueError: If the model name is invalid.

        Example:
            >>> self._process_model_name("models/my_model")
            'my_model'
        """
        # Should fail as violently as possible if the model name is invalid.
        if self._is_path(model_name_or_path):
            logger.debug(f"Path input detected: {model_name_or_path}")
            try:
                result = ModelPath.get_model_name_from_path(model_name_or_path)
                if result:
                    logger.debug(f"Model name extracted from path: {result}")
                    return result
                else:
                    raise ValueError(
                        f"Invalid {self.target} name. Please provide a valid {self.target} name that follows the lowercase 'adjective_noun' format."
                    )
            except Exception as e:
                logger.error(f"Error extracting model name from path: {e}")
        else:
            if not self.validate_model_name(model_name_or_path):
                raise ValueError(
                    f"Invalid {self.target} name. Please provide a valid {self.target} name that follows the lowercase 'adjective_noun' format."
                )
            logger.debug(f"{self.target.title()} name detected: {model_name_or_path}")
            return model_name_or_path

    def _handle_global_cache(self) -> None:
        """
        Handles the global cache for the model instance.

        Attempts to retrieve the model instance from the global cache.
        If the instance is not found or cache overwrite is forced, initializes a new instance.

        Raises:
            Exception: If there is an error accessing the global cache.
        """
        try:
            from views_pipeline.cache.global_cache import GlobalCache

            cached_instance = GlobalCache[self._instance_hash]
            if cached_instance and not self._force_cache_overwrite:
                logger.debug(
                    f"ModelPath instance {self.model_name} found in GlobalCache. Using cached instance."
                )
                return cached_instance
        except Exception as e:
            logger.error(
                f"Error adding model {self.model_name} to cache: {e}. Initializing new ModelPath instance."
            )

    def _write_to_global_cache(self) -> None:
        """
        Writes the current model instance to the global cache if it doesn't exist.

        Adds the model instance to the global cache using the instance hash as the key.
        """
        from views_pipeline.cache.global_cache import GlobalCache

        if GlobalCache[self._instance_hash] is None:
            logger.debug(
                f"Writing {self.target.title}Path object to cache for model {self.model_name}."
            )
            GlobalCache[self._instance_hash] = self
        else:
            if self._force_cache_overwrite:
                logger.debug(
                    f"Overwriting {self.target.title}Path object in cache for model {self.model_name}. (_force_cache_overwrite is set to True)"
                )
                GlobalCache[self._instance_hash] = self

    def _initialize_directories(self) -> None:
        """
        Initializes the necessary directories for the model.

        Creates and sets up various directories required for the model, such as architectures, artifacts, configs, data, etc.
        """
        self.model_dir = self._get_model_dir()
        self.logging = self.model_dir / "logs"
        self.artifacts = self._build_absolute_directory(Path("artifacts"))
        self.configs = self._build_absolute_directory(Path("configs"))
        self.data = self._build_absolute_directory(Path("data"))
        self.data_generated = self._build_absolute_directory(Path("data/generated"))
        self.data_processed = self._build_absolute_directory(Path("data/processed"))
        self.data_raw = self._build_absolute_directory(Path("data/raw"))
        self.src = self._build_absolute_directory(Path("src")) 
        self.architectures = self._build_absolute_directory(Path("src/architectures"))
        self.dataloaders = self._build_absolute_directory(Path("src/dataloaders"))
        self.forecasting = self._build_absolute_directory(Path("src/forecasting"))
        self.management = self._build_absolute_directory(Path("src/management"))
        self.offline_evaluation = self._build_absolute_directory(
            Path("src/offline_evaluation")
        )
        self.reports = self._build_absolute_directory(Path("reports"))
        # self._templates = self.meta_tools / "templates"
        self.training = self._build_absolute_directory(Path("src/training"))
        self.utils = self._build_absolute_directory(Path("src/utils"))
        self.visualization = self._build_absolute_directory(Path("src/visualization"))
        self._sys_paths = None
        # if self.common_querysets not in sys.path:
        #     sys.path.insert(0, str(self.common_querysets))
        self.queryset_path = self._build_absolute_directory(Path(f"queryset_{self.model_name}.py"))
        self._queryset = None

        # Initialize model-specific directories only if the class is ModelPath
        if self.__class__.__name__ == "ModelPath":
            self._initialize_model_specific_directories()

    def _initialize_model_specific_directories(self) -> None:
        self.architectures = self._build_absolute_directory(Path("src/architectures"))
        self.data_raw = self._build_absolute_directory(Path("data/raw"))
        self.notebooks = self._build_absolute_directory(Path("notebooks"))
        self.online_evaluation = self._build_absolute_directory(
            Path("src/online_evaluation")
        )

    def _initialize_scripts(self) -> None:
        """
        Initializes the necessary scripts for the model.

        Creates and sets up various scripts required for the model, such as configuration scripts, main script, and other utility scripts.
        """
        self.scripts = [
            self._build_absolute_directory(Path("configs/config_deployment.py")),
            self._build_absolute_directory(Path("configs/config_hyperparameters.py")),
            self._build_absolute_directory(Path("configs/config_meta.py")),
            self._build_absolute_directory(Path("main.py")),
            self._build_absolute_directory(Path("README.md")),
            # self._build_absolute_directory(
            #     Path("src/forecasting/generate_forecast.py")
            # ),
            # self._build_absolute_directory(
            #     Path("src/management/execute_model_runs.py")
            # ),
            # self._build_absolute_directory(
            #     Path("src/management/execute_model_tasks.py")
            # ),
        ]
        # Initialize model-specific directories only if the class is ModelPath
        if self.__class__.__name__ == "ModelPath":
            self._initialize_model_specific_scripts()

    def _initialize_model_specific_scripts(self) -> None:
        """
        Initializes and appends model-specific script paths to the `scripts` attribute.

        The paths are built using the `_build_absolute_directory` method.
        Returns:
            None
        """
        self.scripts += [
            # self._build_absolute_directory(Path("configs/config_sweep.py")),
            # self._build_absolute_directory(Path("src/dataloaders/get_data.py")),
            # self._build_absolute_directory(
            #     Path("src/offline_evaluation/evaluate_model.py")
            # ),
            # self._build_absolute_directory(
            #     Path(f"src/training/train_{self.target}.py")
            # ),
            self.queryset_path
        ]

    def _is_path(self, path_input: Union[str, Path]) -> bool:
        """
        Determines if the given input is a valid path.

        This method checks if the input is a string or a Path object and verifies if it points to an existing file or directory.

        Args:
            path_input (Union[str, Path]): The input to check.

        Returns:
            bool: True if the input is a valid path, False otherwise.
        """
        try:
            path_input = Path(path_input) if isinstance(path_input, str) else path_input
            return path_input.exists() and len(path_input.parts) > 1
        except Exception as e:
            logger.error(f"Error checking if input is a path: {e}")
            return False

    def get_queryset(self) -> Optional[Dict[str, str]]:
        """
        Returns the queryset for the model if it exists.

        This method checks if the queryset directory exists and attempts to import the queryset module.
        If the queryset module is successfully imported, it calls the `generate` method of the queryset module.

        Returns:
            module or None: The queryset module if it exists, or None otherwise.

        Raises:
            FileNotFoundError: If the common queryset directory does not exist and validation is enabled.
        """
        # if self._validate and not self._check_if_dir_exists(self.queryset_path):
        #     error = f"Common queryset directory {self.common_querysets} does not exist. Please create it first using `make_new_scripts.py` or set validate to `False`."
        #     logger.error(error)
        #     raise FileNotFoundError(error)
        if self._validate and self._check_if_dir_exists(self.queryset_path):
            try:
                self._queryset = importlib.import_module(self.queryset_path.stem)
            except Exception as e:
                logger.error(f"Error importing queryset: {e}")
                self._queryset = None
            else:
                logger.debug(f"Queryset {self.queryset_path} imported successfully.")
                return self._queryset.generate() if self._queryset else None
        else:
            logger.warning(
                f"Queryset {self.queryset_path} does not exist. Continuing..."
            )
        return None

    def _get_model_dir(self) -> Path:
        """
        Determines the model directory based on validation.

        This method constructs the model directory path and checks if it exists.
        If the directory does not exist and validation is enabled, it raises a FileNotFoundError.

        Returns:
            Path: The model directory path.

        Raises:
            FileNotFoundError: If the model directory does not exist and validation is enabled.
        """
        model_dir = self.models / self.model_name
        if not self._check_if_dir_exists(model_dir) and self._validate:
            error = f"{self.target.title()} directory {model_dir} does not exist. Please create it first using `make_new_model.py` or set validate to `False`."
            logger.error(error)
            raise FileNotFoundError(error)
        return model_dir

    def _check_if_dir_exists(self, directory: Path) -> bool:
        """
        Checks if the directory already exists.
        Args:
            directory (Path): The directory path to check.
        Returns:
            bool: True if the directory exists, False otherwise.
        """
        return directory.exists()

    def _build_absolute_directory(self, directory: Path) -> Path:
        """
        Build an absolute directory path based on the model directory.
        """
        directory = self.model_dir / directory
        if self._validate:
            if not self._check_if_dir_exists(directory=directory):
                logger.warning(f"Directory {directory} does not exist. Continuing...")
                if directory.name.endswith(".py"):
                    return directory.name
                return None
        return directory

    @DeprecationWarning
    def add_paths_to_sys(self) -> List[str]:
        """
        (Will be deprecated soon) Adds the necessary paths for the current model to the system path (sys.path).

        This method checks if paths for another model are already added to sys.path. If so, it logs an error and exits.
        If no paths are added yet, it initializes the _sys_paths attribute and adds the relevant paths to sys.path.

        Steps:
        1. Iterate through the current sys.path to detect if paths for another model are already added.
        2. If paths for another model are found, log an error and return.
        3. If _sys_paths is None, initialize it as an empty list.
        4. Iterate through the instance's attributes and add paths that are:
        - Path objects
        - Absolute paths
        - Existing directories
        5. Extend sys.path with the collected paths.
        6. Handle potential AttributeError if sys.path is not found.

        Returns:
            list: The list of paths added to sys.path.

        Raises:
            AttributeError: If sys.path is not found.
        """
        for path in sys.path:
            path = Path(path)
            if str(self.target + "s") in path.parts:
                try:
                    model_name = ModelPath.get_model_name_from_path(path)
                except:
                    continue
                if model_name != self.model_name:
                    logger.error(
                        f"Paths for another {self.target} ('{model_name}') are already added to sys.path. Please remove them first by calling remove_paths_from_sys()."
                    )
                    return
                if model_name == self.model_name:
                    logger.debug(
                        f"Path {str(path)} for '{model_name}' is already added to sys.path. Skipping..."
                    )
        if self._sys_paths is None:
            self._sys_paths = []
        for attr, value in self.__dict__.items():
            # value = getattr(self, attr)
            if str(attr) not in self._ignore_attributes:
                if (
                    isinstance(value, Path)
                    and value.is_absolute()
                    and self._check_if_dir_exists(value)
                    and str(value) not in sys.path
                ):
                    sys.path.insert(0, str(value))
                    if str(value) in sys.path:
                        self._sys_paths.append(str(value))
                        logger.debug(f"Added path to sys.path: {str(value)}")
                    else:
                        logger.warning(f"Unable to add path to sys.path: {str(value)}")
                else:
                    logger.warning(
                        f"Skipping path: {value}. Does not exist or already in sys.path."
                    )
        return self._sys_paths

    @DeprecationWarning
    def remove_paths_from_sys(self) -> bool:
        """
        Removes the paths added by the current model from the system path (sys.path).

        This method checks if _sys_paths is not None and attempts to remove each path from sys.path.
        If a path is not found in sys.path, it logs a warning and skips it.
        Finally, it sets _sys_paths to None.

        Steps:
        1. Check if _sys_paths is not None.
        2. Iterate through _sys_paths and remove each path from sys.path.
        3. Log the removal of each path.
        4. Handle ValueError if a path is not found in sys.path.
        5. Set _sys_paths to None.

        Raises:
            ValueError: If a path is not found in sys.path.
        """
        if self._sys_paths is not None:
            for path in self._sys_paths:
                try:
                    sys.path.remove(path)
                    if path not in sys.path:
                        logger.debug(f"Removed path from sys.path: {path}")
                    else:
                        logger.warning(f"Unable to remove path '{path}'. Continuing...")
                except ValueError:
                    logger.warning(f"Path '{path}' not found in sys.path. Skipping...")
            self._sys_paths = None
            return True
        else:
            logger.error(
                f"{self.model_name} paths not found in sys.path. Add paths by calling add_paths_to_sys()."
            )
            return False

    def view_directories(self) -> None:
        """
        Prints a formatted list of the directories and their absolute paths.

        This method iterates through the instance's attributes and prints the name and path of each directory.
        It ignores certain attributes specified in the _ignore_attributes list.
        """
        print("\n{:<20}\t{:<50}".format("Name", "Path"))
        print("=" * 72)
        for attr, value in self.__dict__.items():
            # value = getattr(self, attr)
            if attr not in self._ignore_attributes and isinstance(value, Path):
                print("{:<20}\t{:<50}".format(str(attr), str(value)))

    def view_scripts(self) -> None:
        """
        Prints a formatted list of the scripts and their absolute paths.

        This method iterates through the scripts attribute and prints the name and path of each script.
        If a script path is None, it prints "None" instead of the path.
        """
        print("\n{:<20}\t{:<50}".format("Script", "Path"))
        print("=" * 72)
        for path in self.scripts:
            if isinstance(path, Path):
                print("{:<20}\t{:<50}".format(str(path.name), str(path)))
            else:
                print("{:<20}\t{:<50}".format(str(path), "None"))

    def get_directories(self) -> Dict[str, Optional[str]]:
        """
        Retrieve a dictionary of directory names and their paths.

        Returns:
            dict: A dictionary where keys are directory names and values are their paths.
        """
        # Not in use yet.
        # self._ignore_attributes = [
        #     "model_name",
        #     "model_dir",
        #     "scripts",
        #     "_validate",
        #     "models",
        #     "_sys_paths",
        #     "queryset_path",
        #     "_queryset",
        #     "_ignore_attributes",
        #     "target",
        #     "_force_cache_overwrite",
        #     "initialized",
        #     "_instance_hash"
        #     "use_global_cache"
        # ]
        directories = {}
        relative = False
        for attr, value in self.__dict__.items():

            if str(attr) not in [
                "model_name",
                "root",
                "scripts",
                "_validate",
                "models",
                "templates",
                "_sys_paths",
                "_queryset",
                "queryset_path",
                "_ignore_attributes",
                "target",
                "_force_cache_overwrite",
                "initialized",
                "_instance_hash",
            ] and isinstance(value, Path):
                if not relative:
                    directories[str(attr)] = str(value)
                else:
                    if self.model_name in value.parts:
                        relative_path = value.relative_to(self.model_dir)
                    else:
                        relative_path = value
                    if relative_path == Path("."):
                        continue
                    directories[str(attr)] = str(relative_path)
        return directories

    def get_scripts(self) -> Dict[str, Optional[str]]:
        """
        Returns a dictionary of the scripts and their absolute paths.

        Returns:
            dict: A dictionary containing the scripts and their absolute paths.
        """
        scripts = {}
        relative = False
        for path in self.scripts:
            if isinstance(path, Path):
                if relative:
                    if self.model_dir in path.parents:
                        scripts[str(path.name)] = str(path.relative_to(self.model_dir))
                    else:
                        scripts[str(path.name)] = str(path)
                else:
                    scripts[str(path.name)] = str(path)
            else:
                scripts[str(path)] = None
        return scripts
    

# ============================================================ EnsemblePath ============================================================

class EnsemblePath(ModelPath):
    """
    A class to manage ensemble paths and directories within the ViEWS Pipeline.
    Inherits from ModelPath and sets the target to 'ensemble'.
    """

    _target = "ensemble"

    @classmethod
    def _initialize_class_paths(cls):
        """Initialize class-level paths for ensemble."""
        super()._initialize_class_paths()
        cls._models = cls._root / Path(cls._target + "s")
        # Additional ensemble-specific initialization...

    def __init__(
        self, ensemble_name_or_path: Union[str, Path], validate: bool = True
    ) -> None:
        """
        Initializes an EnsemblePath instance.

        Args:c
            ensemble_name_or_path (str or Path): The ensemble name or path.
            validate (bool, optional): Whether to validate paths and names. Defaults to True.
        """
        super().__init__(ensemble_name_or_path, validate)
        # Additional ensemble-specific initialization...
        print(self._validate)

    def _initialize_directories(self) -> None:
        """
        Initializes the necessary directories for the ensemble.

        Creates and sets up various directories required for the ensemble, such as architectures, artifacts, configs, data, etc.
        """
        # Call the parent class's _initialize_directories method
        super()._initialize_directories()
        # Initialize ensemble-specific directories only if the class is EnsemblePath
        if self.__class__.__name__ == "EnsemblePath":
            self._initialize_ensemble_specific_directories()

    def _initialize_ensemble_specific_directories(self):
        self.reports_figures = self._build_absolute_directory(Path("reports/figures"))
        self.reports_papers = self._build_absolute_directory(Path("reports/papers"))
        self.reports_plots = self._build_absolute_directory(Path("reports/plots"))
        self.reports_slides = self._build_absolute_directory(Path("reports/slides"))
        self.reports_timelapse = self._build_absolute_directory(
            Path("reports/timelapse")
        )

    def _initialize_scripts(self) -> None:
        """
        Initializes the necessary scripts for the ensemble.

        Creates and sets up various scripts required for the ensemble, such as configuration scripts, main script, and other utility scripts.
        """
        super()._initialize_scripts()
        # Initialize ensemble-specific scripts only if the class is EnsemblePath
        if self.__class__.__name__ == "EnsemblePath":
            self._initialize_ensemble_specific_scripts()

    def _initialize_ensemble_specific_scripts(self):
        """
        Initializes the ensemble-specific scripts by appending their absolute paths
        to the `self.scripts` list.

        The paths are built using the `_build_absolute_directory` method.

        Returns:
            None
        """
        self.scripts += [
            self._build_absolute_directory(Path("artifacts/model_metadata_dict.py")),
            self._build_absolute_directory(
                Path("src/offline_evaluation/evaluate_ensemble.py")
            ),
            self._build_absolute_directory(Path("src/training/train_ensemble.py")),
            self._build_absolute_directory(Path("src/utils/utils_check.py")),
            self._build_absolute_directory(Path("src/utils/utils_run.py")),
            self._build_absolute_directory(Path("src/visualization/visual.py")),
        ]
