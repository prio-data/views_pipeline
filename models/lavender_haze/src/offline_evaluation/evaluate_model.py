import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_squared_error

import sys
pipeline_path = f"{Path(__file__).parent.parent.parent.parent.parent}"
sys.path.append(str(pipeline_path)+"/common_utils")

from views_forecasts.extensions import *
from common_utils.set_path import get_artifacts_path, get_data_path


def evaluate_model(common_config):
    print("Evaluating...")

    stepshifter_model_calib = pd.read_pickle(get_artifacts_path(common_config["name"], "calib"))
    stepshifter_model_test = pd.read_pickle(get_artifacts_path(common_config["name"], "test"))
    dataset = pd.read_parquet(get_data_path(common_config["name"], "raw"))

    steps = common_config["steps"]
    stepcols = [common_config["depvar"]]
    for step in steps:
        stepcols.append("step_pred_" + str(step))

    try:
        df_calib = pd.DataFrame.forecasts.read_store(name=f'{common_config["name"]}_calib')
    except:
        df_calib = stepshifter_model_calib.predict("calib", "predict", dataset)
        df_calib.forecasts.to_store(name=f'{common_config["name"]}_calib')  #Remember to set the run name in actual implementation

    try:
        df_test = pd.DataFrame.forecasts.read_store(name=f'{common_config["name"]}_test')
    except:
        df_test = stepshifter_model_test.predict("test", "predict", dataset)
        df_test.forecasts.to_store(name=f'{common_config["name"]}_test')  #Remember to set the run name in actual implementation

    df_calib = df_calib.replace([np.inf, -np.inf], 0)[stepcols]
    df_test = df_test.replace([np.inf, -np.inf], 0)[stepcols]

    pred_cols = [f"step_pred_{str(i)}" for i in steps]
    df_calib["mse"] = df_calib.apply(lambda row: mean_squared_error([row[common_config["depvar"]]] * 36,
                                                        [row[col] for col in pred_cols]), axis=1)
    df_test["mse"] = df_test.apply(lambda row: mean_squared_error([row[common_config["depvar"]]] * 36,
                                                        [row[col] for col in pred_cols]), axis=1)
    print("MSE_calib:", df_calib["mse"].mean())
    print("MSE_test:", df_test["mse"].mean())