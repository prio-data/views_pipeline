import pandas as pd
from pathlib import Path

import sys
PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils"))
from set_path import setup_project_paths, setup_data_paths, setup_artifacts_paths
setup_project_paths(PATH)

from get_data import get_partition_data


def forecast(model_config):
    print('Predicting...')

    PATH_RAW, _, PATH_GENERATED = setup_data_paths(PATH)
    PATH_ARTIFACTS = setup_artifacts_paths(PATH)
    dataset = pd.read_parquet(PATH_RAW / 'raw.parquet')
    stepshifter_model = pd.read_pickle(PATH_ARTIFACTS / "model_forecast_partition.pkl")
    
    predictions = stepshifter_model.predict("forecast", "predict", get_partition_data(dataset, "forecasting"))

    pred_cols = [f"step_pred_{str(i)}" for i in model_config["steps"]]
    predictions = predictions[pred_cols]

    predictions.to_parquet(PATH_GENERATED / 'generated.parquet')

    return predictions