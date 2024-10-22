import re
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
import sys
sys.path.append(str(Path(__file__).parent))

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

def check_if_model_exists(name: str) -> bool:
    """
    Check if a model with the given name exists in the models directory.

    Parameters:
        name (str): The model name to check.

    Returns:
        bool: True if the model exists, False otherwise.
    """
    # Assuming the models are stored in a directory named "models"
    import utils_model_paths
    models_dir = Path("models")
    model_path = utils_model_paths.find_project_root() / models_dir / name.lower()
    result = model_path.exists()
    if result:
        logger.error(f"Model '{name}' already exists. Please use a different name.")
    return result

def check_if_ensemble_exists(name: str) -> bool:
    """
    Check if an ensemble with the given name exists in the ensembles directory.

    Parameters:
        name (str): The ensemble name to check.

    Returns:
        bool: True if the ensemble exists, False otherwise.
    """
    # Assuming the ensembles are stored in a directory named "ensembles"
    import utils_model_paths
    ensembles_dir = Path("ensembles")
    ensemble_path = utils_model_paths.find_project_root() / ensembles_dir / name.lower()
    result = ensemble_path.exists()
    if result:
        logger.error(f"Ensemble '{name}' already exists. Please use a different name.")
    return result