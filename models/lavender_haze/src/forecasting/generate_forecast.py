import sys
import pandas as pd
from datetime import datetime

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

from set_partition import get_partitioner_dict
from utils_log_files import create_log_file
from utils_run import get_standardized_df
from utils_outputs import save_predictions
from utils_artifacts import get_latest_model_artifact


def forecast_model_artifact(config, artifact_name):
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

    partition = get_partitioner_dict(run_type)['predict']
    df_predictions = stepshift_model.future_point_predict(partition[0] - 1, df_viewser, keep_specific=True)
    df_predictions = get_standardized_df(df_predictions, config)
    data_generation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    save_predictions(df_predictions, PATH_GENERATED, config)
    create_log_file(PATH_GENERATED, config, config["timestamp"], data_generation_timestamp)
