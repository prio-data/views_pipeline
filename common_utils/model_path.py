from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


import importlib

# meta_tools/utils

from meta_tools.utils import utils_model_naming
from meta_tools.utils import utils_model_paths


class ModelPath:
    def __init__(self, model_name_or_path, validate=True, target="model") -> None:
        """
        Initializes a ModelPath object with the given model name or path and sets up the directory structure.

        Args:
            model_name_or_path (str, Path): The name or path from inside the model directory.
            validate (bool): Whether to validate the existence of the model directory or script file. Defaults to True.

        Attributes:
            validate (bool): Indicates whether to validate the existence of the model directory or script file.
            model_name (str): The name of the model.
            root (Path): The root directory of the project.
            models (Path): The directory containing all models.
            common_utils (Path): Path to the common utilities directory.
            common_configs (Path): Path to the common configurations directory.
            model_dir (Path or None): The directory of the model if it exists, otherwise None.
            architectures (Path): Path to the architectures directory.
            artifacts (Path): Path to the artifacts directory.
            configs (Path): Path to the configs directory.
            data (Path): Path to the data directory.
            data_generated (Path): Path to the generated data directory.
            data_processed (Path): Path to the processed data directory.
            data_raw (Path): Path to the raw data directory.
            dataloaders (Path): Path to the dataloaders directory.
            forecasting (Path): Path to the forecasting directory.
            management (Path): Path to the management directory.
            notebooks (Path): Path to the notebooks directory.
            offline_evaluation (Path): Path to the offline evaluation directory.
            online_evaluation (Path): Path to the online evaluation directory.
            reports (Path): Path to the reports directory.
            src (Path): Path to the src directory.
            templates (Path): Path to the templates directory.
            training (Path): Path to the training directory.
            utils (Path): Path to the utils directory.
            visualization (Path): Path to the visualization directory.
            common_querysets (Path): Path to the common querysets directory.
            scripts (list of Path): List of paths to expected script files.

        Raises:
            ValueError: If the model name is invalid.
            FileNotFoundError: If the model directory does not exist and validation is enabled.
        """
        self._validate = validate
        self._target = target
        self.model_name = model_name_or_path
        if self._is_path(self.model_name):
            logger.info(f"Path input detected: {self.model_name}")
            self.model_name = utils_model_paths.get_model_name_from_path(self.model_name)
        else:
            if not utils_model_naming.validate_model_name(self.model_name):
                raise ValueError(
                    f"Invalid {self._target} name. Please provide a valid {self._target} name that follows the lowercase 'adjective_noun' format that doesn't already exist."
                )
            else:
                logger.info(f"{self._target.title()} name detected: {self.model_name}")
        
        self.root = utils_model_paths.find_project_root()
        self.models = self.root / Path(self._target + "s")
        self.common_utils = self.root / "common_utils"
        self.common_configs = self.root / "common_configs"
        self.model_dir = self._get_model_dir()
        self.architectures = self._build_absolute_directory(Path("src/architectures"))
        self.artifacts = self._build_absolute_directory(Path("artifacts"))
        self.configs = self._build_absolute_directory(Path("configs"))
        self.data = self._build_absolute_directory(Path("data"))  # new
        self.data_generated = self._build_absolute_directory(
            Path("data/generated")
        )  # new
        self.data_processed = self._build_absolute_directory(
            Path("data/processed")
        )  # new
        self.data_raw = self._build_absolute_directory(Path("data/raw"))  # new
        self.dataloaders = self._build_absolute_directory(Path("src/dataloaders"))
        self.forecasting = self._build_absolute_directory(Path("src/forecasting"))
        self.management = self._build_absolute_directory(Path("src/management"))
        self.notebooks = self._build_absolute_directory(Path("notebooks"))
        self.offline_evaluation = self._build_absolute_directory(
            Path("src/offline_evaluation")
        )
        self.online_evaluation = self._build_absolute_directory(
            Path("src/online_evaluation")
        )
        self.reports = self._build_absolute_directory(Path("reports"))
        self.src = self._build_absolute_directory(Path("src"))
        self._templates = self.root / "meta_tools" / "templates"  # new
        self.training = self._build_absolute_directory(Path("src/training"))
        self.utils = self._build_absolute_directory(Path("src/utils"))
        self.visualization = self._build_absolute_directory(Path("src/visualization"))
        self._sys_paths = None
        self.common_querysets = self.root / "common_querysets"
        if self.common_querysets not in sys.path:
            sys.path.insert(0, str(self.common_querysets))
        self._queryset_path = self.common_querysets / f"queryset_{self.model_name}.py"
        self._queryset = None
        # ALWAYS use _build_absolute_directory to set the paths. This will check if the directory exists and return None if it doesn't. Linked to validate flag.
        self.scripts = [
            # self._build_absolute_directory(self._queryset_path),
            self._build_absolute_directory(Path("configs/config_deployment.py")),
            self._build_absolute_directory(Path("configs/config_hyperparameters.py")),
            self._build_absolute_directory(Path("configs/config_input_data.py")),
            self._build_absolute_directory(Path("configs/config_meta.py")),
            self._build_absolute_directory(Path("configs/config_sweep.py")),
            self._build_absolute_directory(Path("main.py")),
            self._build_absolute_directory(Path("README.md")),
            # self._build_absolute_directory(Path("requirements.txt")),
            self._build_absolute_directory(Path("src/dataloaders/get_data.py")),
            self._build_absolute_directory(
                Path("src/forecasting/generate_forecast.py")
            ),
            self._build_absolute_directory(
                Path("src/management/execute_model_runs.py")
            ),
            self._build_absolute_directory(
                Path("src/management/execute_model_tasks.py")
            ),
            self._build_absolute_directory(
                Path("src/offline_evaluation/evaluate_model.py")
            ),
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
            ]

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
            # Ensure the input is either a string or a Path object
            if not isinstance(path_input, (str, Path)):
                logger.error(f"Invalid type for path_input: {type(path_input)}. Expected str or Path.")
                return False

            # Convert string input to Path object
            if isinstance(path_input, str):
                path_input = Path(path_input)
            if len(path_input.parts) == 1:
                return False
            
            # Check if the path exists
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
        Adds the necessary paths for the current model to the system path (sys.path).

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
        # Detect if another model's paths are already added
        for path in sys.path:
            # Extract model name from path
            path = Path(path)
            # print(path)
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
                    
            # Add paths to sys.path
        # Initialize _sys_paths if not already done
        if self._sys_paths is None:
            self._sys_paths = []
        # Add paths to sys.path
        for attr, value in self.__dict__.items():
            if str(attr) not in self._ignore_paths:
                if (
                    isinstance(value, Path)
                    and value.is_absolute()
                    and self._check_if_dir_exists(value)
                    and str(value) not in sys.path
                ):
                    # current_sys_path.insert(0, str(value))
                    sys.path.insert(0, str(value))
                    if str(value) in sys.path:
                        self._sys_paths.append(str(value))
                        logger.info(f"Added path to sys.path: {str(value)}")
                    else:
                        logger.warning(f"Unable to add path to sys.path: {str(value)}")
                else:
                    logger.warning(f"Skipping path: {value}. Does not exist or already in sys.path.")
        # sys.path = current_sys_path
        return self._sys_paths
        

    def _add_path_to_sys(self, path: Path) -> None:
        """
        Helper method to add a path to sys.path.

        This method checks if the path is not already in sys.path and adds it to the beginning of sys.path.
        It also appends the path to the _sys_paths attribute.

        Args:
            path (Path): The path to add to sys.path.

        Raises:
            Warning: If the path cannot be added to sys.path.
        """
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
            if str(path) not in sys.path:
                logger.warning(f"Unable to add path to sys.path: {str(path)}")
            else:
                self._sys_paths.append(str(path))
                logger.info(f"Added path to sys.path: {str(path)}")

    def _create_and_add_path(self, path: Path) -> None:
        """
        Helper method to create a directory and add it to sys.path.

        This method attempts to create the specified directory and adds it to sys.path if successful.

        Args:
            path (Path): The directory path to create and add to sys.path.

        Raises:
            Exception: If there is an error creating the directory.
        """
        try:
            path.mkdir(parents=True)
            logger.info(f"Created directory: {path}")
            self._add_path_to_sys(path)
        except Exception as e:
            logger.error(f"Error creating directory: {e}")


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
                        logger.info(f"Removed path from sys.path: {path}")
                        # print(f"Removed path from sys.path: {path}")
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

    # Relative paths flag will always be False. Not a good idea to use it but logic still maintained.
    def get_directories(self) -> dict:
        """
        Retrieve a dictionary of directory names and their paths.

        Returns:
            dict: A dictionary where keys are directory names and values are their paths.
        """
        directories = {}
        relative = False
        for attr, value in self.__dict__.items():
            # Ignore certain attributes and check if the value is a Path object
            if str(attr) not in [
                "model_name",
                "root",
                "scripts",
                "_validate",
                "models",
                "templates",
                "_sys_paths",
                # "common_querysets",
                "_queryset",
                "_queryset_path",
                "_ignore_paths",
                "_target",
            ] and isinstance(value, Path):
                if not relative:
                    directories[str(attr)] = str(value)
                else:
                    if self.model_name in value.parts:
                        relative_path = value.relative_to(self.model_dir)
                    else:
                        relative_path = value
                        # relative_path = value.relative_to(self.root)
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
                        # scripts[str(path.name)] = str(path.relative_to(self.root))
                        scripts[str(path.name)] = str(path)
                else:
                    scripts[str(path.name)] = str(path)
            else:
                scripts[str(path)] = None
        return scripts
    
if __name__ == "__main__":
    model = ModelPath("blank_space", validate=True)
    print(model.model_dir)
    del model
    print(sys.path)
