from pathlib import Path
from utils import validate_model_name


class ModelDirectoryBuilder:
    """
    Class to manage the creation and assessment of model directories for organizing machine learning projects.

    Attributes:
        expected_structure (list of str): List of directories and files that are expected in the model directory structure.
        current_dir (Path): The current working directory when the object is initialized.
        relative_path (str): The relative path where the model directories will be created.
        models_dir (Path): The path where model directories will be stored.
        model_dir (Path): The specific path for the current model's directory.
        subdirs (list of str): List of subdirectories to be created within the model directory.
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
            "src/forecasting"
        ]

        self.current_dir = Path.cwd()
        self.relative_path = "models"

        # TODO: Fix this
        # If the current directory is not the root directory, go up one level and append "models"
        if self.current_dir.match('*meta_tools'):
            self.models_dir = self.current_dir.parent / self.relative_path
        else:
            self.models_dir = self.current_dir / self.relative_path

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
            "src/management"
        ]

    def build(self) -> Path:
        """
        Create the model directory and its subdirectories, and initialize necessary files such as README.md and requirements.txt.

        Returns:
            Path: The path to the created model directory.

        Raises:
            FileExistsError: If the model directory already exists.
        """
        try:
            self.model_dir.mkdir(parents=True, exist_ok=False)
            print(f"Created new model directory: {self.model_dir}")
        except FileExistsError:
            print(f"Model directory already exists: {self.model_dir}")

        for subdir in self.subdirs:
            subdir_path = self.model_dir / subdir
            subdir_path.mkdir(parents=True, exist_ok=True)
            print(f"Created subdirectory: {subdir_path}")

        # Create README.md and requirements.txt
        readme_path = self.model_dir / "README.md"
        with open(readme_path, "w") as readme_file:
            readme_file.write("# Model README\n")
        print(f"Created README.md: {readme_path}")

        requirements_path = self.model_dir / "requirements.txt"
        with open(requirements_path, "w") as requirements_file:
            requirements_file.write("# Requirements\n")
        print(f"Created requirements.txt: {requirements_path}")
        print(f"<TEST> model_dir: {self.model_dir}")
        return self.model_dir

    def assess(self) -> dict:
        """
        Assess the model directory by checking for the presence of expected directories.

        Returns:
            dict: A dictionary containing assessment results with two keys:
                - 'model_dir': The path to the model directory.
                - 'structure_errors': A list of errors related to missing directories or files.
        """
        assessment = {
            "model_dir": self.model_dir,
            "structure_errors": []
        }

        # Check structure
        for item in self.expected_structure:
            item_path = self.model_dir / item
            if not item_path.exists():
                assessment["structure_errors"].append(
                    f"Missing directory or file: {item}")
        return assessment


if __name__ == "__main__":
    model_name = input("Enter the name of the model: ")
    while not validate_model_name(model_name):
        print("Invalid model name. Please use the format 'noun_adjective' in lowercase.")
        model_name = input("Enter the name of the model: ")
    model_directory_builder = ModelDirectoryBuilder(model_name)
    model_directory_builder.build()
    assessment = model_directory_builder.assess()
    print("\nDirectory assessment results:")
    print(f"Model directory: {assessment['model_dir']}")
    print(f"Structure errors: {assessment['structure_errors']}")
