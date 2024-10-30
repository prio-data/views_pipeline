from utils import utils_script_gen
from pathlib import Path


def generate(script_dir: Path) -> bool:
    """
    Generates a Python script with a predefined template and saves it to the specified directory.

    The generated script includes a function to evaluate a model artifact. It handles loading the model,
    making predictions, standardizing the data, generating evaluation metrics, and saving the outputs.
    It also logs relevant information using Weights & Biases (wandb).

    Args:
        script_dir (Path): The directory where the generated script will be saved.

    Returns:
        bool: True if the script was successfully saved, False otherwise.
    """

    code = f"""
from datetime import datetime
import pandas as pd
import logging
from model_path import ModelPath
from utils_log_files import create_log_file, read_log_file
from utils_outputs import save_model_outputs, save_predictions
from utils_run import get_standardized_df
from utils_artifacts import get_latest_model_artifact
from utils_evaluation_metrics import generate_metric_dict
from utils_model_outputs import generate_output_dict
from utils_wandb import log_wandb_log_dict
from views_forecasts.extensions import *

logger = logging.getLogger(__name__)

def evaluate_model_artifact(config, artifact_name):
    model_path = ModelPath(config["name"])
    path_raw = model_path.data_raw
    path_generated = model_path.data_generated
    path_artifacts = model_path.artifacts
    run_type = config["run_type"]

    # if an artifact name is provided through the CLI, use it.
    # Otherwise, get the latest model artifact based on the run type
    if artifact_name:
        logger.info(f"Using (non-default) artifact: {{artifact_name}}")

        if not artifact_name.endswith(".pkl"):
            artifact_name += ".pkl"
        PATH_ARTIFACT = path_artifacts / artifact_name
    else:
        # use the latest model artifact based on the run type
        logger.info(f"Using latest (default) run type ({{run_type}}) specific artifact")
        PATH_ARTIFACT = get_latest_model_artifact(path_artifacts, run_type)

    config["timestamp"] = PATH_ARTIFACT.stem[-15:]
    df_viewser = pd.read_pickle(path_raw / f"{{run_type}}_viewser_df.pkl")

    try:
        stepshift_model = pd.read_pickle(PATH_ARTIFACT)
    except FileNotFoundError:
        logger.exception(f"Model artifact not found at {{PATH_ARTIFACT}}")

    df = stepshift_model.predict(run_type, df_viewser)
    df = get_standardized_df(df, config)
    data_generation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    date_fetch_timestamp = read_log_file(path_raw / f"{{run_type}}_data_fetch_log.txt").get("Data Fetch Timestamp", None)

    _, df_output = generate_output_dict(df, config)
    evaluation, df_evaluation = generate_metric_dict(df, config)
    log_wandb_log_dict(config, evaluation)

    save_model_outputs(df_evaluation, df_output, path_generated, config)
    save_predictions(df, path_generated, config)
    create_log_file(path_generated, config, config["timestamp"], data_generation_timestamp, date_fetch_timestamp)
"""
    return utils_script_gen.save_script(script_dir, code)