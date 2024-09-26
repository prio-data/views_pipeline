from utils import utils_script_gen
from pathlib import Path


def generate(script_dir: Path, model_architecture: str) -> bool:
    """
    Generates a script that defines the `get_sweep_config` function for hyperparameter sweeps.

    Parameters:
        script_dir (Path):
            The directory where the generated deployment configuration script will be saved.
            This should be a valid writable path.

        model_architecture (str):
            The architecture of the model to be used in the hyperparameter sweep. This string will be included
            in the configuration to define the model being tuned.

    Returns:
        bool:
            True if the script was written and compiled successfully, False otherwise.
    """
    code = f"""def get_sweep_config():
    \"""
    Contains the configuration for hyperparameter sweeps using WandB.
    This configuration is "operational" so modifying it will change the search strategy, parameter ranges, and other settings for hyperparameter tuning aimed at optimizing model performance.

    Returns:
    - sweep_config (dict): A dictionary containing the configuration for hyperparameter sweeps, defining the methods and parameter ranges used to search for optimal hyperparameters.
    \"""

    sweep_config = {{
        'method': 'grid',
    }}

    # Example metric setup:
    metric = {{
        'name': 'MSE',
        'goal': 'minimize'
    }}
    sweep_config['metric'] = metric

    # Example parameters setup:
    parameters_dict = {{
        'model': {{
            'value': '{model_architecture}' # Eg. "LSTM", "CNN", "Transformer"
        }},
    }}
    sweep_config['parameters'] = parameters_dict

    return sweep_config
"""
    return utils_script_gen.save_script(script_dir, code)
