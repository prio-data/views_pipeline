import pandas as pd
from datetime import datetime
import logging
from model_path import ModelPath
from utils_log_files import create_log_file
from utils_run import get_standardized_df
from utils_outputs import save_predictions
from utils_artifacts import get_latest_model_artifact

logger = logging.getLogger(__name__)


def forecast_model_artifact(config, artifact_name):
    model_path = ModelPath(config["name"], validate=False)
    path_raw = model_path.data_raw
    path_generated = model_path.data_generated
    path_artifacts = model_path.artifacts
    run_type = config["run_type"]

    # if an artifact name is provided through the CLI, use it.
    # Otherwise, get the latest model artifact based on the run type
    if artifact_name:
        logger.info(f"Using (non-default) artifact: {artifact_name}")

        if not artifact_name.endswith(".pkl"):
            artifact_name += ".pkl"
        path_artifact = path_artifacts / artifact_name
    else:
        # use the latest model artifact based on the run type
        logger.info(f"Using latest (default) run type ({run_type}) specific artifact")
        path_artifact = get_latest_model_artifact(path_artifacts, run_type)

    config["timestamp"] = path_artifact.stem[-15:]
    df_viewser = pd.read_pickle(path_raw / f"{run_type}_viewser_df.pkl")

    try:
        stepshift_model = pd.read_pickle(path_artifact)
    except FileNotFoundError:
        logger.exception(f"Model artifact not found at {path_artifact}")

    df_predictions = stepshift_model.predict(run_type, df_viewser)
    df_predictions = get_standardized_df(df_predictions, config)
    data_generation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    save_predictions(df_predictions, path_generated, config)
    create_log_file(path_generated, config, config["timestamp"], data_generation_timestamp)
