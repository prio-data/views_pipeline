from pathlib import Path
import py_compile
from typing import Dict
from utils.utils_model_naming import validate_model_name
from utils.utils_model_paths import find_project_root

# TODO: Implement a mechanism to generate the scripts from template files at views_pipeline/meta_tools/templates
from templates import (
    template_config_deployment,
    template_config_hyperparameters,
    template_config_input_data,
    template_config_meta,
    template_config_sweep,
    template_main,
)

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelScriptBuilder:
    """
    A class to build and manage Python scripts for machine learning model deployment and evaluation.

    Attributes:
        model_name (str): The name of the model which determines the directory structure and script names.
        model_dir (Path): The path to the model directory where scripts are saved.
        alfgorithm (str): The algorithm of the model, set during script generation.
        obligatory_scripts (list of str): List of paths to the obligatory scripts that should be present in the model directory.
        root (Path): The path to the project root directory.
        models_dir (Path): The path to the `models` directory where all model directories are stored.

    Methods:
        __init__(model_name: str):
            Initializes the ModelScriptBuilder with the provided model name, setting up the paths and attributes.

        _check_if_model_dir_exists() -> bool:
            Checks if the model directory exists.

        build_model_scripts():
            Builds all required scripts if the model directory exists, and prompts the user for model algorithm.

        assess_model_scripts() -> dict:
            Assesses the model directory to check for the presence of all obligatory scripts and returns the results.

            Returns:
                dict: A dictionary containing assessment results with two keys:
                    - 'model_dir': The path to the model directory.
                    - 'missing_scripts': A list of errors related to missing scripts.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model_dir = Path(self.model_name)
        self.model_algorithm = None
        self.obligatory_scripts = [
            "configs/config_deployment.py",
            "configs/config_hyperparameters.py",
            # "configs/config_input_data.py",
            "configs/config_meta.py",
            "configs/config_sweep.py",
            "src/dataloaders/get_data.py",
            "src/training/train_ensemble.py",
            "src/forecasting/generate_forececast.py",
            "src/offline_evaluation/evaluate_model.py",
            "src/management/execute_model_runs.py",
            "src/management/execute_model_tasks.py",
            "main.py",
            "README.md",
        ]

        self.root = find_project_root()
        self.models_dir = self.root / "models"
        self.model_dir = self.models_dir / model_name

    def _check_if_model_dir_exists(self):
        """
        Checks if the model directory already exists.

        Returns:
        bool: True if the model directory exists, False otherwise.
        """
        return self.model_dir.exists()

    def build_model_scripts(self):
        if not self._check_if_model_dir_exists():
            raise FileNotFoundError(
                f"Model directory {self.model_dir} does not exist. Please run the `make_new_model_dir.py` script first. Aborting script generation."
            )
        template_config_deployment.generate(
            script_dir=self.model_dir / "configs/config_deployment.py"
        )
        self.model_algorithm = input(
            "Enter the algorithm of the model (e.g. XGBoost, LightBGM, HydraNet): "
        )
        template_config_hyperparameters.generate(
            script_dir=self.model_dir / "configs/config_hyperparameters.py",
            model_algorithm=self.model_algorithm,
        )
        template_config_input_data.generate(
            script_dir=self.root / "common_querysets" / f"config_input_data_{self.model_name}.py",
            model_name=self.model_name,
        )
        template_config_meta.generate(
            script_dir=self.model_dir / "configs/config_meta.py",
            model_name=self.model_name,
            model_algorithm=self.model_algorithm,
        )
        template_config_sweep.generate(
            script_dir=self.model_dir / "configs/config_sweep.py",
            model_algorithm=self.model_algorithm,
        )
        template_main.generate(script_dir=self.model_dir / "main.py")

    def assess_model_scripts(self) -> dict:
        """
        Assess the model directory by checking for the presence of expected obligatory scripts.

        Returns:
            dict: A dictionary containing assessment results with two keys:
                - 'model_dir': The path to the model directory.
                - 'missing_scripts': A list of errors related to missing script files.
        """
        assessment = {"model_dir": self.model_dir, "missing_scripts": []}
        # Check scripts
        for script_path in self.obligatory_scripts:
            full_script_path = self.model_dir / script_path
            if not full_script_path.exists():
                assessment["missing_scripts"].append(f"Missing script: {script_path}")
        return assessment


if __name__ == "__main__":
    model_name = input("Enter the name of the model: ")
    while not validate_model_name(model_name):
        logging.error(
            "Invalid model name. Please use the format 'adjective_noun' in lowercase."
        )
        model_name = input("Enter the name of the model: ")
    script_builder = ModelScriptBuilder(model_name)
    script_builder.build_model_scripts()
    assessment = script_builder.assess_model_scripts()
    # logging.info(f"Model directory: {assessment['model_dir']}")
    if not assessment["missing_scripts"]:
        logging.info("All scripts have been successfully generated.")
    else:
        logging.warning(f"Structure errors: {assessment['missing_scripts']}")
