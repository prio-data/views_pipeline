import sys
from pathlib import Path
import numpy as np
import json
import warnings
warnings.filterwarnings("ignore")
import wandb

PATH = Path(__file__)
from set_path import setup_project_paths, setup_data_paths, setup_artifacts_paths, setup_model_paths
setup_project_paths(PATH)

from views_forecasts.extensions import *
from get_data import get_partition_data
from generate_metric_dict import generate_metric_dict
from artifacts_utils import get_latest_model_artifact

def evaluate_model_artifact(config, artifact_name):
    PATH_MODEL = setup_model_paths(PATH)
    PATH_RAW, _, _ = setup_data_paths(PATH)
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

    run_type = config["run_type"]
    steps = config["steps"]
    stepcols = [config["depvar"]]
    for step in steps:
        stepcols.append("step_pred_" + str(step))

    dataset = pd.read_parquet(PATH_RAW / f'raw_{run_type}.parquet')
    try:
        stepshift_model = pd.read_pickle(PATH_ARTIFACT)
    except:
        raise FileNotFoundError(f"Model artifact not found at {PATH_ARTIFACT}")

    df = stepshift_model.predict(run_type, "predict", get_partition_data(dataset, run_type))
    df = df.replace([np.inf, -np.inf], 0)[stepcols]
    df = df.mask(df < 0, 0)

    evaluation, df_evaluation = generate_metric_dict(df, steps, config["depvar"])
    print(f"MSE_{run_type}:", df_evaluation.loc["mean"]["MSE"])



