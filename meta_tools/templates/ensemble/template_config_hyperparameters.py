from utils import utils_script_gen
from pathlib import Path


def generate(script_dir: Path) -> bool:
    """
    Generates a script that defines a function for obtaining hyperparameter configurations
    necessary for model training.

    Parameters:
        script_dir (Path):
            The directory where the generated deployment configuration script will be saved.
            This should be a valid writable path.

        model_algorithm (str):
            The architecture of the model to be used for training. This string will be included in the
            hyperparameter configuration and can be modified to test different algorithms.

    Returns:
        bool:
            True if the script was written and compiled successfully, False otherwise.
    """
    code = """def get_hp_config(): 
    hp_config = {
        "steps": [*range(1, 36 + 1, 1)]
    }
    return hp_config
"""
    return utils_script_gen.save_script(script_dir, code)