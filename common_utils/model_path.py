from pathlib import Path
import sys
import logging
import importlib
import hashlib

sys.path.append(str(Path(__file__).parent.parent))
from meta_tools.utils import utils_model_naming, utils_model_paths
from global_cache import GlobalCache

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class ModelPath:
    """
    A class to manage model paths and directories within the ViEWS Pipeline.

    Attributes:
        __instances__ (int): A class-level counter to track the number of ModelPath instances.
        model_name (str): The name of the model.
        _validate (bool): A flag to indicate whether to validate paths and names.
        _target (str): The target type (e.g., 'model').
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
        _queryset_path (Path): The path to the queryset script.
        _queryset (module): The imported queryset module.
        scripts (list): A list of script paths.
        _ignore_paths (list): A list of paths to ignore.
    """
    __instances__ = 0

    # def __new__(cls, model_name_or_path, validate=True, target="model", force_cache_overwrite=False):
    #     """
    #     Ensures that only one instance of the ModelPath class is created for each unique set of arguments.
    #     """
    #     instance_hash = cls._generate_hash(model_name_or_path, validate, target)
    #     cached_instance = GlobalCache().get(instance_hash)
    #     if cached_instance and not force_cache_overwrite:
    #         logger.info(f"Using cached ModelPath instance for hash: {instance_hash}")
    #         return cached_instance
    #     instance = super(ModelPath, cls).__new__(cls)
    #     instance._instance_hash = instance_hash
    #     return instance

    def __init__(self, model_name_or_path, validate=True, target="model", force_cache_overwrite=False) -> None:
        """
        Initializes a ModelPath instance.

        Args:
            model_name_or_path (str or Path): The model name or path.
            validate (bool, optional): Whether to validate paths and names. Defaults to True.
            target (str, optional): The target type (e.g., 'model'). Defaults to 'model'.
            force_cache_overwrite (bool, optional): Whether to force overwrite the cache. Defaults to False.
        """
        # if hasattr(self, 'initialized') and self.initialized:
        #     return

        """
        Initializes a ModelPath instance.

        Args:
            model_name_or_path (str or Path): The model name or path.
            validate (bool, optional): Whether to validate paths and names. Defaults to True.
            target (str, optional): The target type (e.g., 'model'). Defaults to 'model'.
            force_cache_overwrite (bool, optional): Whether to force overwrite the cache. Defaults to False.
        """
        ModelPath.__instances__ += 1
        self._validate = validate
        self._target = target
        self._force_cache_overwrite = force_cache_overwrite
        self.model_name = model_name_or_path
        if self._is_path(self.model_name):
            logger.debug(f"Path input detected: {self.model_name}")
            self.model_name = utils_model_paths.get_model_name_from_path(self.model_name)
        else:
            if not utils_model_naming.validate_model_name(self.model_name):
                raise ValueError(
                    f"Invalid {self._target} name. Please provide a valid {self._target} name that follows the lowercase 'adjective_noun' format that doesn't already exist."
                )
            else:
                logger.debug(f"{self._target.title()} name detected: {self.model_name}")
        logger.debug(f"ModelPath instance count: {ModelPath.__instances__}")
        self.root = utils_model_paths.find_project_root()
        self.models = self.root / Path(self._target + "s")
        self.common_utils = self.root / "common_utils"
        self.common_configs = self.root / "common_configs"
        self.model_dir = self._get_model_dir()
        self.architectures = self._build_absolute_directory(Path("src/architectures"))
        self.artifacts = self._build_absolute_directory(Path("artifacts"))
        self.configs = self._build_absolute_directory(Path("configs"))
        self.data = self._build_absolute_directory(Path("data"))
        self.data_generated = self._build_absolute_directory(Path("data/generated"))
        self.data_processed = self._build_absolute_directory(Path("data/processed"))
        self.data_raw = self._build_absolute_directory(Path("data/raw"))
        self.dataloaders = self._build_absolute_directory(Path("src/dataloaders"))
        self.forecasting = self._build_absolute_directory(Path("src/forecasting"))
        self.management = self._build_absolute_directory(Path("src/management"))
        self.notebooks = self._build_absolute_directory(Path("notebooks"))
        self.offline_evaluation = self._build_absolute_directory(Path("src/offline_evaluation"))
        self.online_evaluation = self._build_absolute_directory(Path("src/online_evaluation"))
        self.reports = self._build_absolute_directory(Path("reports"))
        self.src = self._build_absolute_directory(Path("src"))
        self._templates = self.root / "meta_tools" / "templates"
        self.training = self._build_absolute_directory(Path("src/training"))
        self.utils = self._build_absolute_directory(Path("src/utils"))
        self.visualization = self._build_absolute_directory(Path("src/visualization"))
        self._sys_paths = None
        self.common_querysets = self.root / "common_querysets"
        if self.common_querysets not in sys.path:
            sys.path.insert(0, str(self.common_querysets))
        self._queryset_path = self.common_querysets / f"queryset_{self.model_name}.py"
        self._queryset = None
        self.scripts = [
            self._build_absolute_directory(Path("configs/config_deployment.py")),
            self._build_absolute_directory(Path("configs/config_hyperparameters.py")),
            self._build_absolute_directory(Path("configs/config_input_data.py")),
            self._build_absolute_directory(Path("configs/config_meta.py")),
            self._build_absolute_directory(Path("configs/config_sweep.py")),
            self._build_absolute_directory(Path("main.py")),
            self._build_absolute_directory(Path("README.md")),
            self._build_absolute_directory(Path("src/dataloaders/get_data.py")),
            self._build_absolute_directory(Path("src/forecasting/generate_forecast.py")),
            self._build_absolute_directory(Path("src/management/execute_model_runs.py")),
            self._build_absolute_directory(Path("src/management/execute_model_tasks.py")),
            self._build_absolute_directory(Path("src/offline_evaluation/evaluate_model.py")),
            self._build_absolute_directory(Path("src/training/train_ensemble.py")),
        ]
        self._ignore_paths = [
            "model_name",
            "model_dir",
            "scripts",
            "_validate",
            "models",
            "_sys_paths",
            "_queryset_path",
            "_queryset",
            "_ignore_paths",
            "_target",
            "_force_cache_overwrite",
        ]

        # Cache management
        try:
            instance_hash = self._generate_hash(model_name_or_path, validate, target)
            if self._force_cache_overwrite:
                GlobalCache()[instance_hash] = self
                logger.info(f"Model {self.model_name} with hash {instance_hash} overwritten to cache.")
                self._return_cached_model_path()
            
            if not GlobalCache().__getitem__(instance_hash):
                GlobalCache()[instance_hash] = self
                logger.info(f"Model {self.model_name} with hash {instance_hash} added to cache.")
                self._return_cached_model_path()
        except Exception as e:
            logger.error(f"Error adding model {self.model_name} to cache: {e}")
            pass

        # self.initialized = True

    def __hash__(self):
        """
        Generates a unique hash for the ModelPath instance.

        Returns:
            str: The SHA-256 hash of the model name, validation flag, and target.
        """
        return hashlib.sha256(str((self.model_name, self._validate, self._target)).encode()).hexdigest()

    def _return_cached_model_path(self):
        """
        Returns the cached model path if it exists in the cache.

        Returns:
            ModelPath or None: The cached ModelPath instance or None if not found.
        """
        try:
            result = GlobalCache()[self.__hash__()]
            if result:
                logger.info(f"Model {self.model_name} with hash {self.__hash__()} found in cache.")
                return result
        except KeyError:
            logger.warning(f"Model {self.model_name} not found in cache.")
    
    @staticmethod
    def _generate_hash(model_name_or_path, validate, target):
        """
        Generates a unique hash for the ModelPath instance.

        Args:
            model_name_or_path (str or Path): The model name or path.
            validate (bool): Whether to validate paths and names.
            target (str): The target type (e.g., 'model').

        Returns:
            str: The SHA-256 hash of the model name, validation flag, and target.
        """
        return hashlib.sha256(str((model_name_or_path, validate, target)).encode()).hexdigest()

    def _is_path(self, path_input) -> bool:
        """
        Determines if the given input is a valid path.

        This method checks if the input is a string or a Path object and verifies if it points to an existing file or directory.

        Args:
            path_input (Union[str, Path]): The input to check.

        Returns:
            bool: True if the input is a valid path, False otherwise.
        """
        try:
            if not isinstance(path_input, (str, Path)):
                logger.error(f"Invalid type for path_input: {type(path_input)}. Expected str or Path.")
                return False
            if isinstance(path_input, str):
                path_input = Path(path_input)
            if len(path_input.parts) == 1:
                return False
            if path_input.exists():
                return True
            else:
                logger.warning(f"Path {path_input} does not exist. Use model name instead")
                return False
        except Exception as e:
            logger.error(f"Error checking if input is a path: {e}")
            return False

    def get_queryset(self):
        """
        Returns the queryset for the model if it exists.

        This method checks if the queryset directory exists and attempts to import the queryset module.
        If the queryset module is successfully imported, it calls the `generate` method of the queryset module.

        Returns:
            module or None: The queryset module if it exists, or None otherwise.

        Raises:
            FileNotFoundError: If the common queryset directory does not exist and validation is enabled.
        """
        if self._validate and not self._check_if_dir_exists(self.common_querysets):
            raise FileNotFoundError(
                f"Common queryset directory {self.common_querysets} does not exist. Please create it first using `make_new_scripts.py` or set validate to `False`."
            )
        elif self._validate and self._check_if_dir_exists(self._queryset_path):
            try:
                self._queryset = importlib.import_module(self._queryset_path.stem)
            except Exception as e:
                logger.error(f"Error importing queryset: {e}")
                self._queryset = None
            else:
                logger.info(f"Queryset {self._queryset_path} imported successfully.")
                return self._queryset.generate() if self._queryset else None
        else:
            logger.warning(
                f"Queryset {self._queryset_path} does not exist. Continuing..."
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
        try:
            model_dir = self.models / self.model_name
            if not self._check_if_dir_exists(model_dir):
                if self._validate:
                    raise FileNotFoundError(
                        f"{self._target.title()} directory {model_dir} does not exist. Please run the `make_new_{self._target}.py` script first."
                    )
            return model_dir
        except Exception as e:
            logger.error(f"Error getting {self._target} directory: {e}")
            return

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

    def add_paths_to_sys(self) -> list:
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
            if str(self._target + "s") in path.parts:
                model_name = utils_model_paths.get_model_name_from_path(path)
                if model_name != self.model_name:
                    logger.error(
                        f"Paths for another {self._target} ('{model_name}') are already added to sys.path. Please remove them first by calling remove_paths_from_sys()."
                    )
                    return
                if model_name == self.model_name:
                    logger.info(
                        f"Path {str(path)} for '{model_name}' is already added to sys.path. Skipping..."
                    )
        if self._sys_paths is None:
            self._sys_paths = []
        for attr, value in self.__dict__.items():
            if str(attr) not in self._ignore_paths:
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
                    logger.warning(f"Skipping path: {value}. Does not exist or already in sys.path.")
        return self._sys_paths

    def remove_paths_from_sys(self) -> None:
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
        It ignores certain attributes specified in the _ignore_paths list.
        """
        print("\n{:<20}\t{:<50}".format("Name", "Path"))
        print("=" * 72)
        for attr, value in self.__dict__.items():
            if attr not in self._ignore_paths and isinstance(value, Path):
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

    def get_directories(self) -> dict:
        """
        Retrieve a dictionary of directory names and their paths.

        Returns:
            dict: A dictionary where keys are directory names and values are their paths.
        """
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
                "_queryset_path",
                "_ignore_paths",
                "_target",
                "_force_cache_overwrite",
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

    def get_scripts(self) -> dict:
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