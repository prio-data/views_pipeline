from pathlib import Path
from utils.utils_model_naming import validate_model_name
from utils.utils_model_paths import find_project_root
import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelDirectoryBuilder:
    """
    A class to create and manage the directory structure for a machine learning model.

    Attributes:
        expected_structure (list of str): A list of expected directories to be created within the model directory.
        current_dir (Path): The current working directory from which the script is run.
        relative_path (str): The relative path to the `models` directory.
        model_name (str): The name of the model for which the directory structure is to be created.
        models_dir (Path): The path to the `models` directory where all model directories are stored.
        model_dir (Path): The path to the model directory where the structure and files will be created.
        subdirs (list of str): A list of subdirectories to be created within the model directory.

    Methods:
        __init__(model_name: str) -> None:
            Initializes the ModelDirectoryBuilder with the given model name and sets up paths.

        build_model_directory() -> Path:
            Creates the model directory and its subdirectories, and initializes necessary files such as README.md
            and requirements.txt.

            Returns:
                Path: The path to the created model directory.

            Raises:
                FileExistsError: If the model directory already exists.

        assess_model_directory() -> dict:
            Assesses the model directory by checking for the presence of expected directories.

            Returns:
                dict: A dictionary containing assessment results with two keys:
                    - 'model_dir': The path to the model directory.
                    - 'structure_errors': A list of errors related to missing directories.
    """

    def __init__(self, model_name) -> None:
        """
        Initialize a ModelDirectory object with the given model name and set up paths.

        Args:
            model_name (str): The name of the model for which directories and files are to be created.

        Returns:
            None
        """

        self.expected_structure = [
            "configs",
            "artifacts",
            "notebooks",
            "reports",
            "src/dataloaders",
            "src/architectures",
            "src/utils",
            "src/training",
            "src/offline_evaluation",
            "src/online_evaluation",
            "src/forecasting",
        ]

        self.model_name = model_name
        if not validate_model_name(self.model_name):
            raise ValueError(
                "Invalid model name. Please use the format 'adjective_noun' in lowercase."
            )
        self.root = find_project_root()
        self.models_dir = self.root / "models"
        self.model_dir = self.models_dir / model_name

        # self.model_path = Path(f'../models/{self.model_dir}')

        self.subdirs = [
            "configs",
            "data/raw",
            "data/processed",
            "data/generated",
            "artifacts",
            "notebooks",
            "reports",  # new
            "src/online_evaluation",  # new
            "src/dataloaders",
            "src/architectures",
            "src/utils",
            "src/visualization",
            "src/training",
            "src/offline_evaluation",
            "src/forecasting",
            "src/management",
        ]

    def build_model_directory(self) -> Path:
        """
        Create the model directory and its subdirectories, and initialize necessary files such as README.md and requirements.txt.

        Returns:
            Path: The path to the created model directory.

        Raises:
            FileExistsError: If the model directory already exists.
        """
        if self.model_dir.exists():
            logger.info(
                f"Model directory already exists: {self.model_dir}. Proceeding with existing directory."
            )
        else:
            self.model_dir.mkdir(parents=True, exist_ok=False)
            logger.info(f"Created new model directory: {self.model_dir}")

        for subdir in self.subdirs:
            subdir_path = self.model_dir / subdir
            if not subdir_path.exists():
                subdir_path.mkdir(parents=True, exist_ok=True)
                logging.info(f"Created subdirectory: {subdir_path}")
            else:
                logging.info(f"Subdirectory already exists: {subdir_path}. Skipping.")

        # Create README.md and requirements.txt
        readme_path = self.model_dir / "README.md"
        with open(readme_path, "w") as readme_file:
            readme_file.write(
                f"# Model README\n## Model name: {self.model_name}\n## Created on: {str(datetime.datetime.now())}"
            )
        logging.info(f"Created README.md: {readme_path}")

        requirements_path = self.model_dir / "requirements.txt"
        with open(requirements_path, "w") as requirements_file:
            requirements_file.write("# Requirements\n")
        logging.info(f"Created requirements.txt: {requirements_path}")
        return self.model_dir

    def assess_model_directory(self) -> dict:
        """
        Assess the model directory by checking for the presence of expected directories.

        Returns:
            dict: A dictionary containing assessment results with two keys:
                - 'model_dir': The path to the model directory.
                - 'structure_errors': A list of errors related to missing directories or files.
        """
        assessment = {"model_dir": self.model_dir, "structure_errors": []}

        # Check structure
        for item in self.expected_structure:
            item_path = self.model_dir / item
            if not item_path.exists():
                assessment["structure_errors"].append(
                    f"Missing directory or file: {item}"
                )
        return assessment


if __name__ == "__main__":
    model_name = input("Enter the name of the model: ")
    while not validate_model_name(model_name):
        print(
            "Invalid model name. Please use the format 'adjective_noun' in lowercase, e.g., 'happy_kitten'."
        )
        model_name = input("Enter the name of the model: ")
    model_directory_builder = ModelDirectoryBuilder(model_name)
    model_directory_builder.build_model_directory()
    assessment = model_directory_builder.assess_model_directory()
    logging.info("\nDirectory assessment results:")
    logging.info(f"Model directory: {assessment['model_dir']}")
    logging.info(f"Structure errors: {assessment['structure_errors']}")
