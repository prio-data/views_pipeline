import pandas as pd
import numpy as np
from pathlib import Path

import sys
PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils"))
from set_path import setup_project_paths, setup_data_paths, setup_artifacts_paths
setup_project_paths(PATH)

from get_data import get_partition_data
from utils_artifacts import get_latest_model_artifact

def forecast_model_artifact(config, artifact_name):
    run_type = config['run_type']
    PATH_RAW, _, PATH_GENERATED = setup_data_paths(PATH)
    PATH_ARTIFACTS = setup_artifacts_paths(PATH)
    dataset = pd.read_parquet(PATH_RAW / f'raw_{run_type}.parquet')

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

    try:
        stepshift_model = pd.read_pickle(PATH_ARTIFACT)
    except:
        raise FileNotFoundError(f"Model artifact not found at {PATH_ARTIFACT}")

    pred_cols = [f"step_pred_{str(i)}" for i in config["steps"]]
    predictions = stepshift_model.predict("forecasting", "predict", get_partition_data(dataset, run_type))
    predictions = predictions[pred_cols]
    predictions = predictions.replace([np.inf, -np.inf], 0)
    predictions = predictions.mask(predictions < 0, 0)
    predictions.to_parquet(PATH_GENERATED / 'generated.parquet')

    return predictions