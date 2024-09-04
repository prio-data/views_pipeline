import sys
from datetime import datetime
import pandas as pd
import wandb
import warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(filename='../../run.log', encoding='utf-8', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from pathlib import Path
PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths, setup_data_paths, setup_artifacts_paths
setup_project_paths(PATH)

from utils import save_model_outputs, get_standardized_df, create_log_file
from utils_artifacts import get_latest_model_artifact
from utils_evaluation_metrics import generate_metric_dict
from utils_model_outputs import generate_output_dict
from utils_wandb import log_wandb_log_dict
from views_forecasts.extensions import *


def evaluate_model_artifact(config, artifact_name):
    PATH_RAW, _, PATH_GENERATED = setup_data_paths(PATH)
    PATH_ARTIFACTS = setup_artifacts_paths(PATH)
    run_type = config['run_type']

    # if an artifact name is provided through the CLI, use it.
    # Otherwise, get the latest model artifact based on the run type
    if artifact_name:
        logger.info(f"Using (non-default) artifact: {artifact_name}")

        if not artifact_name.endswith('.pkl'):
            artifact_name += '.pkl'
        PATH_ARTIFACT = PATH_ARTIFACTS / artifact_name
    else:
        # use the latest model artifact based on the run type
        logger.info(f"Using latest (default) run type ({run_type}) specific artifact")
        PATH_ARTIFACT = get_latest_model_artifact(PATH_ARTIFACTS, run_type)

    config["timestamp"] = PATH_ARTIFACT.stem[-15:]
    df_viewser = pd.read_pickle(PATH_RAW / f"{run_type}_viewser_df.pkl")

    try:
        stepshift_model = pd.read_pickle(PATH_ARTIFACT)
    except FileNotFoundError:
        logger.exception(f"Model artifact not found at {PATH_ARTIFACT}")

    df = stepshift_model.predict(run_type, df_viewser)
    df = get_standardized_df(df, config)
    data_generation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output, df_output = generate_output_dict(df, config)
    evaluation, df_evaluation = generate_metric_dict(df, config)
    log_wandb_log_dict(config, evaluation)

    save_model_outputs(df_evaluation, df_output, PATH_GENERATED, config)
    create_log_file(PATH_GENERATED, config, data_generation_timestamp)
