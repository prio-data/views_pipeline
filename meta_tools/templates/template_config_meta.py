from utils import utils_script_gen
from pathlib import Path


def generate(script_dir: Path, model_name: str, model_architecture: str) -> bool:
    """
    Generates a script that defines the `get_meta_config` function for model metadata.

    Parameters:
        script_dir (Path): 
            The directory where the generated deployment configuration script will be saved. 
            This should be a valid writable path.

        model_name (str): 
            The name of the model. This will be included in the metadata configuration.

        model_architecture (str): 
            The architecture of the model. This string will also be included in the metadata configuration.

    Returns:
        bool: 
            True if the script was written and compiled successfully, False otherwise.
    """
    code = f"""def get_meta_config():
    \"""
    Contains the meta data for the model (model architecture, name, target variable, and level of analysis).
    This config is for documentation purposes only, and modifying it will not affect the model, the training, or the evaluation.

    Returns:
    - meta_config (dict): A dictionary containing model meta configuration.
    \"""
    
    meta_config = {{
        "name": "{model_name}",
        "architecture": "{model_architecture}", 
        # Uncomment and modify the following lines as needed for additional metadata:
        # "target(S)": ["ln_sb_best", "ln_ns_best", "ln_os_best", "ln_sb_best_binarized", "ln_ns_best_binarized", "ln_os_best_binarized"],
        # "queryset": "escwa001_cflong",
        # "level": "pgm",
        # "creator": "Your name here"
    }}
    return meta_config
"""
    return utils_script_gen.save_script(script_dir, code)
