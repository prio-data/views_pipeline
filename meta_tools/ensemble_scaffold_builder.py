from pathlib import Path
from utils.utils_model_naming import validate_model_name
import datetime
import logging
import sys

PATH = Path(__file__)
if 'views_pipeline' in PATH.parts:
    PATH_ROOT = Path(*PATH.parts[:PATH.parts.index('views_pipeline') + 1])
    PATH_COMMON_UTILS = PATH_ROOT / 'common_utils'
    if not PATH_COMMON_UTILS.exists():
        raise ValueError("The 'common_utils' directory was not found in the provided path.")
    sys.path.insert(0, str(PATH_COMMON_UTILS))
    sys.path.insert(0, str(PATH_ROOT))
else:
    raise ValueError("The 'views_pipeline' directory was not found in the provided path.")

# print(str(Path(__file__).parent.parent))
from common_utils import model_path, ensemble_path

from templates.ensemble import (
    template_config_deployment,
    template_config_hyperparameters,
    template_config_meta,
    template_main,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnsembleScaffoldBuilder:
    """
    A class to create and manage the directory structure and scripts for a machine learning ensemble.

    Attributes:
        model_name (str): The name of the ensemble for which the directory structure is to be created.
        _model (ModelPath): An instance of the ModelPath class to manage model paths.
        _subdirs (list of str): A list of subdirectories to be created within the ensemble directory.
        _scripts (list of str): A list of script paths to be created within the ensemble directory.

    Methods:
        __init__(model_name: str) -> None:
            Initializes the EnsembleScaffoldBuilder with the given model name and sets up paths.

        build_model_directory() -> Path:
            Creates the ensemble directory and its subdirectories, and initializes necessary files such as README.md
            and requirements.txt.

            Returns:
                Path: The path to the created ensemble directory.

            Raises:
                FileExistsError: If the ensemble directory already exists.

        build_model_scripts() -> None:
            Generates the necessary configuration and main scripts for the ensemble.

            Raises:
                FileNotFoundError: If the ensemble directory does not exist.

        assess_model_directory() -> dict:
            Assesses the ensemble directory by checking for the presence of expected directories.

            Returns:
                dict: A dictionary containing assessment results with two keys:
                    - 'model_dir': The path to the ensemble directory.
                    - 'structure_errors': A list of errors related to missing directories.

        assess_model_scripts() -> dict:
            Assesses the ensemble directory by checking for the presence of expected scripts.

            Returns:
                dict: A dictionary containing assessment results with two keys:
                    - 'model_dir': The path to the ensemble directory.
                    - 'missing_scripts': A set of missing script paths.
    """

    def __init__(self, model_name) -> None:
        """
        Initialize a EnsembleScaffoldBuilder object with the given ensemble name and set up paths.

        Args:
            model_name (str): The name of the model for which directories and files are to be created.

        Returns:
            None
        """
        self._model = ensemble_path.EnsemblePath(model_name, validate=False)
        self._subdirs = self._model.get_directories().values()
        self._scripts = self._model.get_scripts().values()

    def build_model_directory(self) -> Path:
        """
        Create the ensemble directory and its subdirectories, and initialize necessary files such as README.md and requirements.txt.

        Returns:
            Path: The path to the created ensemble directory.

        Raises:
            FileExistsError: If the ensemble directory already exists.
        """
        if self._model.model_dir.exists():
            logger.info(
                f"Ensemble directory already exists: {self._model.model_dir}. Proceeding with existing directory."
            )
        else:
            self._model.model_dir.mkdir(parents=True, exist_ok=False)
            logger.info(f"Created new ensemble directory: {self._model.model_dir}")

        for subdir in self._subdirs:
            subdir = Path(subdir)
            if not subdir.exists():
                try:
                    subdir.mkdir(parents=True, exist_ok=True)
                    if subdir.exists():
                        logging.info(f"Created subdirectory: {subdir}")
                    else:
                        logging.error(f"Did not create subdirectory: {subdir}")
                except Exception as e:
                    logging.error(f"Error creating subdirectory: {subdir}. {e}")
            else:
                logging.info(f"Subdirectory already exists: {subdir}. Skipping.")

        # Create README.md and requirements.txt
        readme_path = self._model.model_dir / "README.md"
        with open(readme_path, "w") as readme_file:
            readme_file.write(
                f"# Ensemble README\n## Ensemble name: {self._model.model_name}\n## Created on: {str(datetime.datetime.now())}"
            )
        if readme_path.exists():
            logging.info(f"Created README.md: {readme_path}")
        else:
            logging.error(f"Did not create README.md: {readme_path}")

        requirements_path = self._model.model_dir / "requirements.txt"
        with open(requirements_path, "w") as requirements_file:
            requirements_file.write("# Requirements\n")
        if requirements_path.exists():
            logging.info(f"Created requirements.txt: {requirements_path}")
        else:
            logging.error(f"Did not create requirements.txt: {requirements_path}")
        return self._model.model_dir

    def build_model_scripts(self):
        if not self._model.model_dir.exists():
            raise FileNotFoundError(
                f"Ensemble directory {self._model.model_dir} does not exist. Please call build_model_directory() first. Aborting script generation."
            )
        template_config_deployment.generate(
            script_dir=self._model.model_dir / "configs/config_deployment.py"
        )
        template_config_hyperparameters.generate(
            script_dir=self._model.model_dir / "configs/config_hyperparameters.py",
        )
        template_config_meta.generate(
            script_dir=self._model.model_dir / "configs/config_meta.py",
            model_name=self._model.model_name,
        )
        template_main.generate(script_dir=self._model.model_dir / "main.py")

    def assess_model_directory(self) -> dict:
        """
        Assess the ensemble directory by checking for the presence of expected directories.

        Returns:
            dict: A dictionary containing assessment results with two keys:
                - 'model_dir': The path to the ensemble directory.
                - 'structure_errors': A list of errors related to missing directories or files.
        """
        assessment = {"model_dir": self._model.model_dir, "structure_errors": []}
        if not self._model.model_dir.exists():
            raise FileNotFoundError(
                f"Ensemble directory {self._model.model_dir} does not exist. Please call build_model_directory() first."
            )
        updated_model_path = ensemble_path.EnsemblePath(self._model.model_name, validate=True)
        assessment["structure_errors"] = set(
            updated_model_path.get_directories().values()
        ) - set(self._subdirs)
        del updated_model_path
        return assessment

    def assess_model_scripts(self) -> dict:
        """
        Assess the ensemble directory by checking for the presence of expected directories.

        Returns:
            dict: A dictionary containing assessment results with two keys:
                - 'model_dir': The path to the ensemble directory.
                - 'structure_errors': A list of errors related to missing directories or files.
        """
        assessment = {"model_dir": self._model.model_dir, "missing_scripts": set()}
        if not self._model.model_dir.exists():
            raise FileNotFoundError(
                f"Ensemble directory {self._model.model_dir} does not exist. Please call build_model_directory() first."
            )
        for script_path in self._scripts:
            script_path = Path(script_path)
            if not script_path.exists():
                assessment["missing_scripts"].add(script_path)
        return assessment
    
    # Add a .gitkeep file to empty directories and remove it from non-empty directories
    def update_gitkeep_empty_directories(self, delete_gitkeep=True):
        for subdir in self._subdirs:
            subdir = Path(subdir)
            if not list(subdir.glob("*")):
                gitkeep_path = subdir / ".gitkeep"
                if not gitkeep_path.exists():
                    gitkeep_path.touch()
                    logging.info(f"Created .gitkeep file in empty directory: {subdir}")
            else:
                if delete_gitkeep:
                    gitkeep_path = subdir / ".gitkeep"
                    if gitkeep_path.exists():
                        gitkeep_path.unlink()
                        logging.info(f"Removed .gitkeep file from non-empty directory: {subdir}")


if __name__ == "__main__":
    model_name = str(input("Enter the name of the ensemble: "))
    while (
        not validate_model_name(model_name)
        or model_path.ModelPath.check_if_model_dir_exists(model_name)
        or ensemble_path.EnsemblePath.check_if_model_dir_exists(model_name)
    ):
        error = "Invalid input. Please use the format 'adjective_noun' in lowercase, e.g., 'happy_kitten' that does not already exist as a model or ensemble."
        logging.error(error)
        model_name = str(input("Enter the name of the model: "))
    model_directory_builder = EnsembleScaffoldBuilder(model_name)
    model_directory_builder.build_model_directory()
    assessment = model_directory_builder.assess_model_directory()
    if not assessment["structure_errors"]:
        logging.info("Ensemble directory structure is complete.")
    else:
        logging.warning(f"Structure errors: {assessment['structure_errors']}")
    model_directory_builder.build_model_scripts()
    assessment = model_directory_builder.assess_model_scripts()
    if not assessment["missing_scripts"]:
        logging.info("All scripts have been successfully generated.")
    else:
        logging.warning(f"Missing scripts: {assessment['missing_scripts']}")
    model_directory_builder.update_gitkeep_empty_directories()
