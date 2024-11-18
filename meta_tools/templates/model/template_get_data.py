from utils import utils_script_gen
from pathlib import Path


def generate(script_dir: Path) -> bool:
    """
    Generates a Python script with a predefined template and saves it to the specified directory.

    Args:
        script_dir (Path): The directory where the generated script will be saved.

    Returns:
        bool: True if the script was successfully saved, False otherwise.
    """

    code = f"""import logging
from model_path import ModelPath
from utils_dataloaders import fetch_or_load_views_df

logger = logging.getLogger(__name__)

def get_data(args, model_name, self_test):
    model_path = ModelPath(model_name, validate=False)
    path_raw = model_path.data_raw

    data, alerts = fetch_or_load_views_df(model_name, args.run_type, path_raw, self_test, use_saved=args.saved)
    logger.debug(f"DataFrame shape: {{data.shape if data is not None else 'None'}}")

    return data
"""
    return utils_script_gen.save_script(script_dir, code)