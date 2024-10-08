from pathlib import Path
import sys
import re

sys.path.append(str(Path(__file__).parent.parent))

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


import importlib

# meta_tools/utils

from meta_tools.utils import utils_model_naming


class ModelPath:
    def __init__(self, model_name_or_path, validate=True) -> None:
        """
        Initializes a ModelPath object with the given model name and sets up the directory structure.
        Args:
            model_name_or_path (str, Path): The name or path from inside the model directory.
            validate (bool): Whether to validate the existence of the model directory or script file. Defaults to True.
        Attributes:
            validate (bool): Indicates whether to validate the existence of the model directory or script file.
            model_name (str): The name of the model.
            root (Path): The root directory of the project.
            model_dir (Path or None): The directory of the model if it exists, otherwise None.
            utils (Path): Path to the utils directory.
            src (Path): Path to the src directory.
            management (Path): Path to the management directory.
            architectures (Path): Path to the architectures directory.
            artifacts (Path): Path to the artifacts directory.
            training (Path): Path to the training directory.
            forecasting (Path): Path to the forecasting directory.
            offline_evaluation (Path): Path to the offline evaluation directory.
            online_evaluation (Path): Path to the online evaluation directory.
            dataloaders (Path): Path to the dataloaders directory.
            configs (Path): Path to the configs directory.
            reports (Path): Path to the reports directory.
            notebooks (Path): Path to the notebooks directory.
            visualization (Path): Path to the visualization directory.
            scripts (list of Path): List of paths to expected script files.
        Raises:
            FileNotFoundError: If the model directory does not exist and validation is enabled.
        """
        self.validate = validate
        self.model_name = model_name_or_path
        if self._is_path(self.model_name):
            logger.info(f"Path input detected: {self.model_name}")
            self.model_name = self._get_model_name_from_path(self.model_name)
        else:
            if not utils_model_naming.validate_model_name(self.model_name):
                raise ValueError(
                    "Invalid model name. Please provide a valid model name that follows the lowercase 'adjective_noun' format."
                )
            else:
                logger.info(f"Model name detected: {self.model_name}")
        self.root = self._find_project_root()
        self.models = self.root / "models"
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
        self.templates = self.root / "meta_tools" / "templates"  # new
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
            self._build_absolute_directory(self._queryset_path),
            self._build_absolute_directory(Path("configs/config_deployment.py")),
            self._build_absolute_directory(Path("configs/config_hyperparameters.py")),
            self._build_absolute_directory(Path("configs/config_input_data.py")),
            self._build_absolute_directory(Path("configs/config_meta.py")),
            self._build_absolute_directory(Path("configs/config_sweep.py")),
            self._build_absolute_directory(Path("main.py")),
            self._build_absolute_directory(Path("README.md")),
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

    def _is_path(self, path_input):
        """
        Check if the given input is a valid path.

        Parameters:
        path_input (str or Path): The input to check.

        Returns:
        bool: True if the input is a valid path, False otherwise.
        """
        try:
            # Convert to Path if the input is a string
            if isinstance(path_input, str):
                path = Path(path_input)
            elif isinstance(path_input, Path):
                path = path_input
            else:
                logger.error(f"Invalid input type: {type(path_input)}")
            return path.is_absolute()
        except:
            return False

    def _get_model_name_from_path(self, path) -> str:
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
        logger.info(f"Extracting model name from Path: {path}")
        if "models" in path.parts:
            try:
                model_idx = path.parts.index("models")
                model_name = path.parts[model_idx + 1]
                if utils_model_naming.validate_model_name(model_name):
                    logger.info(f"Valid model name found in path: {model_name}")
                    return str(model_name)
                else:
                    error_message = f"Invalid model name `{model_name}` found in path. Please provide a valid model name that follows the lowercase 'adjective_noun' format."
                    logger.error(error_message)
                    raise ValueError(error_message)
            except Exception as e:
                logger.error(f"Could not find model name in path: {e}")
        else:
            error_message = (
                "`models` directory not found in path. Please provide a valid path."
            )
            logger.warning(error_message)
            raise ValueError(error_message)

    def get_queryset(self):
        """
        Returns the queryset for the model if it exists.
        Returns:
            module or None: The queryset module if it exists, or None otherwise.
        """
        if self.validate and not self._check_if_dir_exists(self._common_querysets):
            raise FileNotFoundError(
                f"Common queryset directory {self._common_querysets} does not exist. Please create it first using `make_new_scripts.py` or set validate to `False`."
            )
        elif self.validate and self._check_if_dir_exists(self._queryset_path):
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
        return

    def _get_model_dir(self) -> Path:
        """
        Determines the model directory based on validation.
        Returns:
            Path: The model directory path.
        Raises:
            FileNotFoundError: If the model directory does not exist and validation is enabled.
        """
        try:
            model_dir = self.models / self.model_name
            if not self._check_if_dir_exists(model_dir):
                if self.validate:
                    raise FileNotFoundError(
                        f"Model directory {model_dir} does not exist. Please run the `make_new_model_dir.py` script first."
                    )
            return model_dir
        except Exception as e:
            logger.error(f"Error getting model directory: {e}")
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
        Sets the absolute path of a directory by joining it with the model directory path.
        Args:
            directory (Path): The directory path to set.
        Returns:
            Path: The absolute path of the directory if it exists, or None otherwise.
        """
        # Check if the directory is a Path object or a string
        directory = self.model_dir / directory
        if self.validate:
            if not self._check_if_dir_exists(directory=directory):
                logger.warning(f"Directory {directory} does not exist. Continuing...")
                if directory.name.endswith(".py"):
                    return directory.name
                return None
        return directory

    def _find_project_root(self, marker="LICENSE.md") -> Path:
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
        while (
            current_path != current_path.parent
        ):  # Loop until we reach the root directory
            if (current_path / marker).exists():
                return current_path
            current_path = current_path.parent
        raise FileNotFoundError(
            f"{marker} not found in the directory hierarchy. Unable to find project root."
        )

    def add_paths_to_sys(self) -> None:
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

        Raises:
            AttributeError: If sys.path is not found.
        """
        # Detect if another model's paths are already added
        for path in sys.path:
            # Extract model name from path
            path = Path(path)
            if "models" in path.parts:
                model_name = self._get_model_name_from_path(path)
                if model_name != self.model_name:
                    logger.error(
                        f"Paths for another model ('{model_name}') are already added to sys.path. Please remove them first by calling remove_paths_from_sys()."
                    )
                    return
            # Add paths to sys.path
        # Initialize _sys_paths if not already done
        if self._sys_paths is None:
            self._sys_paths = []

        # Add paths to sys.path
        for attr, value in self.__dict__.items():
            if attr not in [
                "model_name",
                "model_dir",
                "scripts",
                "validate",
                "models",
                "_sys_paths",
                "_queryset_path",
                "_queryset",
            ]:
                # print(attr, value)
                if (
                    isinstance(value, Path)
                    and value.is_absolute()
                    and self._check_if_dir_exists(value)
                    # and str(value) not in current_sys_path
                ):
                    # current_sys_path.insert(0, str(value))
                    self._sys_paths.append(str(value))
                    sys.path.insert(0, str(value))
                    logger.info(f"Added path to sys.path: {value}")
                else:
                    logger.warning(f"Skipping path: {value}.")
        # sys.path = current_sys_path
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
                        logger.info(f"Removed path from sys.path: {path}")
                        print(f"Removed path from sys.path: {path}")
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
        """
        print("\n{:<20}\t{:<50}".format("Name", "Path"))
        print("=" * 72)
        for attr, value in self.__dict__.items():
            if attr not in [
                "model_name",
                "root",
                "model_dir",
                "scripts",
                "validate",
                "_sys_paths",
                "_common_querysets",
                "_queryset",
            ] and isinstance(value, Path):
                print("{:<20}\t{:<50}".format(str(attr), str(value)))

    def view_scripts(self) -> None:
        """
        Prints a formatted list of the scripts and their absolute paths.
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
        Args:
            relative (bool): If True, returns paths relative to the model directory.
                            If False, returns absolute paths. Default is False.
        Returns:
            dict: A dictionary where keys are directory names and values are their paths.
        """
        directories = {}
        relative = False
        for attr, value in self.__dict__.items():
            # Ignore certain attributes and check if the value is a Path object
            if attr not in [
                "model_name",
                "root",
                "scripts",
                "validate",
                "models",
                "templates",
                "_sys_paths",
                "_common_querysets",
                "_queryset",
                "_queryset_path",
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
        Args:
            relative (bool): If True, returns paths relative to the model directory.
                            If False, returns absolute paths. Default is False.
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


# if __name__ == "__main__":
#     purple_alien = ModelPath(model_name_or_path="blank_space", validate=True)
#     directories = list(purple_alien.get_directories().values())
#     path_directories = [Path(d) for d in directories if d is not None]
#     print(path_directories)
# print(purple_alien.get_scripts())
# print(purple_alien.data_raw)
