from utils import utils_script_gen
from pathlib import Path


def generate(script_dir: Path, model_name: str) -> bool:
    """
    Generates a script that defines the `get_meta_config` function for model metadata.

    Parameters:
        script_dir (Path):
            The directory where the generated deployment configuration script will be saved.
            This should be a valid writable path.

        model_name (str):
            The name of the model. This will be included in the metadata configuration.

    Returns:
        bool:
            True if the script was written and compiled successfully, False otherwise.
    """
    code = f"""def get_meta_config():
    \"""
    Contains the metadata for the model (model architecture, name, target variable, and level of analysis).
    This config is for documentation purposes only, and modifying it will not affect the model, the training, or the evaluation.

    Returns:
    - meta_config (dict): A dictionary containing model meta configuration.
    \"""
    meta_config = {{
        "name": "{model_name}", # Eg. "happy_kitten"
        "models": [], # Eg. ["model1", "model2", "model3"]
        "depvar": "ln_ged_sb_dep",  # Eg. "ln_ged_sb_dep"
        "level": "pgm", # Eg. "pgm", "cm"
        "aggregation": "median", # Eg. "median", "mean"
        "creator": "Your name here" 
    }}
    return meta_config
"""
    return utils_script_gen.save_script(script_dir, code)