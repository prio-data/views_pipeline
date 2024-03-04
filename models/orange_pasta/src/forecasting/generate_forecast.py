import pandas as pd
from pathlib import Path

import sys
pipeline_path = f"{Path(__file__).parent.parent.parent.parent.parent}"
sys.path.append(str(pipeline_path)+"/common_utils")
from common_utils.set_path import get_artifacts_path, get_data_path


def forecast(common_config):
    print('Predicting...')

    stepshifter_model = pd.read_pickle(get_artifacts_path(common_config["name"], "forecast"))
    dataset = pd.read_parquet(get_data_path(common_config["name"], "raw"))

    predictions = stepshifter_model.predict("forecast", "predict", dataset)

    pred_cols = [f"step_pred_{str(i)}" for i in common_config["steps"]]
    predictions = predictions[pred_cols]

    predictions.to_parquet(get_data_path(common_config["name"], "generated"))

    return predictions