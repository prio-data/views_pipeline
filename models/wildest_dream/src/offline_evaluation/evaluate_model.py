import sys
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")
import wandb

PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths, setup_data_paths, setup_artifacts_paths
setup_project_paths(PATH)

from utils import save_model_outputs, get_partition_data, get_standardized_df
from utils_artifacts import get_latest_model_artifact
from utils_evaluation_metrics import generate_metric_dict
from utils_model_outputs import generate_output_dict
from utils_wandb import generate_wandb_log_dict
from views_forecasts.extensions import *


def evaluate_model_artifact(config, artifact_name):
    PATH_RAW, _, PATH_GENERATED = setup_data_paths(PATH)
    PATH_ARTIFACTS = setup_artifacts_paths(PATH)

    # if an artifact name is provided through the CLI, use it.
    # Otherwise, get the latest model artifact based on the run type
    if artifact_name:
        print(f"Using (non-default) artifact: {artifact_name}")

        if not artifact_name.endswith('.pkl'):
            artifact_name += '.pkl'
        PATH_ARTIFACT = PATH_ARTIFACTS / artifact_name
    else:
        # use the latest model artifact based on the run type
        print(f"Using latest (default) run type ({config.run_type}) specific artifact")
        PATH_ARTIFACT = get_latest_model_artifact(PATH_ARTIFACTS, config.run_type)

    config["timestamp"] = PATH_ARTIFACT.stem[-15:]
    dataset = pd.read_parquet(PATH_RAW / f'raw_{config.run_type}.parquet')
    
    try:
        stepshift_model = pd.read_pickle(PATH_ARTIFACT)
    except:
        raise FileNotFoundError(f"Model artifact not found at {PATH_ARTIFACT}")

    df = stepshift_model.predict(config.run_type, "predict", get_partition_data(dataset, config.run_type))
    df = get_standardized_df(df, config.run_type)

    evaluation, df_evaluation = generate_metric_dict(df, config)
    output, df_output = generate_output_dict(df, config)
    for t in config.steps:
        log_dict = {}
        log_dict["monthly/out_sample_month"] = t
        step = f"step{str(t).zfill(2)}"
        log_dict = generate_wandb_log_dict(log_dict, evaluation, step)
        wandb.log(log_dict)

    save_model_outputs(df_evaluation, df_output, PATH_GENERATED, config)