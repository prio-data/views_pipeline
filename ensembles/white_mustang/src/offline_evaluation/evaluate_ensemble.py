import sys
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
from set_path import setup_project_paths, setup_data_paths, setup_artifacts_paths, setup_root_paths
setup_project_paths(PATH)

from utils import save_model_outputs, get_standardized_df, get_aggregated_df, create_log_file
from utils_evaluation_metrics import generate_metric_dict
from utils_model_outputs import generate_output_dict
from utils_artifacts import get_latest_model_artifact
from utils_wandb import log_wandb_log_dict
from views_forecasts.extensions import *


def evaluate_ensemble(config):
    run_type = config['run_type']
    steps = config["steps"]
    PATH_MODELS = setup_root_paths(PATH) / "models"
    _, _, PATH_GENERATED_E = setup_data_paths(PATH)
    dfs = []
    timestamp = ''

    for model in config["models"]:
        logger.info(f"Evaluating single model {model}...")
        PATH_MODEL = PATH_MODELS / model
        PATH_RAW, _, PATH_GENERATED = setup_data_paths(PATH_MODEL)
        PATH_ARTIFACTS = setup_artifacts_paths(PATH_MODEL)
        PATH_ARTIFACT = get_latest_model_artifact(PATH_ARTIFACTS, run_type)

        timestamp += model + PATH_ARTIFACT.stem[-15:] + '_'

        df_viewser = pd.read_pickle(PATH_RAW / f"{run_type}_viewser_df.pkl")
        try:
            stepshift_model = pd.read_pickle(PATH_ARTIFACT)
        except FileNotFoundError:
            logger.exception(f"Model artifact not found at {PATH_ARTIFACT}")

        df = stepshift_model.predict(run_type, "predict", df_viewser)
        df = get_standardized_df(df, config)
        dfs.append(df)

    df = get_aggregated_df(dfs, config["aggregation"])
    data_generation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output, df_output = generate_output_dict(df, config)
    evaluation, df_evaluation = generate_metric_dict(df, config)
    log_wandb_log_dict(config, evaluation)

    # I don't think current timestamp is useful here.
    # Timestamp of single models is more important but how should we register them in ensemble config?
    config["timestamp"] = timestamp[:-1]
    save_model_outputs(df_evaluation, df_output, PATH_GENERATED_E, config)
    create_log_file(PATH_GENERATED_E, config, data_generation_timestamp)




