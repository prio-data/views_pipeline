from utils import utils_script_gen
from pathlib import Path


def generate(script_dir: Path, model_algorithm: str) -> bool:
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
    code = f"""def get_hp_config():
    \"""
    Contains the hyperparameter configurations for model training.
    This configuration is "operational" so modifying these settings will impact the model's behavior during the training.

    Returns:
    - hyperparameters (dict): A dictionary containing hyperparameters for training the model, which determine the model's behavior during the training phase.
    \"""
    
    hyperparameters = {{
        'steps': [*range(1, 36 + 1, 1)],
        # Add more hyperparameters as needed
    }}
    return hyperparameters
"""
    return utils_script_gen.save_script(script_dir, code)
