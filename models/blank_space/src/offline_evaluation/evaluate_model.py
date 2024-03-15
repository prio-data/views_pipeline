import sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_data_paths, setup_artifacts_paths
setup_project_paths(PATH)
from get_data import get_partition_data

from views_forecasts.extensions import *


def evaluate_model(model_config):
    print("Evaluating...")

    PATH_RAW, _, _ = setup_data_paths(PATH)
    PATH_ARTIFACTS = setup_artifacts_paths(PATH)
    stepshifter_model_calib = pd.read_pickle(PATH_ARTIFACTS / "model_calib_partition.pkl")
    stepshifter_model_test = pd.read_pickle(PATH_ARTIFACTS / "model_test_partition.pkl")
    dataset = pd.read_parquet(PATH_RAW / 'raw.parquet')

    steps = model_config["steps"]
    stepcols = [model_config["depvar"]]
    for step in steps:
        stepcols.append("step_pred_" + str(step))

    try:
        df_calib = pd.DataFrame.forecasts.read_store(name=f'{model_config["name"]}_calib')
    except:
        df_calib = stepshifter_model_calib.predict("calib", "predict", get_partition_data(dataset, "calibration"))
        df_calib.forecasts.to_store(name=f'{model_config["name"]}_calib')  #Remember to set the run name in actual implementation

    try:
        df_test = pd.DataFrame.forecasts.read_store(name=f'{model_config["name"]}_test')
    except:
        df_test = stepshifter_model_test.predict("test", "predict", get_partition_data(dataset, "testing"))
        df_test.forecasts.to_store(name=f'{model_config["name"]}_test')  #Remember to set the run name in actual implementation

    df_calib = df_calib.replace([np.inf, -np.inf], 0)[stepcols]
    df_test = df_test.replace([np.inf, -np.inf], 0)[stepcols]

    pred_cols = [f"step_pred_{str(i)}" for i in steps]
    df_calib["mse"] = df_calib.apply(lambda row: mean_squared_error([row[model_config["depvar"]]] * 36,
                                                        [row[col] for col in pred_cols]), axis=1)
    df_test["mse"] = df_test.apply(lambda row: mean_squared_error([row[model_config["depvar"]]] * 36,
                                                        [row[col] for col in pred_cols]), axis=1)
    print("MSE_calib:", df_calib["mse"].mean())
    print("MSE_test:", df_test["mse"].mean())