import sys
from pathlib import Path
import numpy as np
import pandas as pd
import json
import warnings
warnings.filterwarnings("ignore")

PATH = Path(__file__)
from set_path import setup_project_paths, setup_data_paths, setup_artifacts_paths
setup_project_paths(PATH)
from get_data import get_partition_data
from generate_metric_dict import generate_metric_dict

from views_forecasts.extensions import *


def evaluate_model(model_config):
    print("Evaluating...")

    PATH_MODEL, PATH_RAW, _, _ = setup_data_paths(PATH)
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

    evaluation_calib, df_evaluation_calib = generate_metric_dict(df_calib, steps, model_config["depvar"])
    evaluation_test, df_evaluation_test = generate_metric_dict(df_test, steps, model_config["depvar"])

    print("MSE_calib:", df_evaluation_calib.loc["mean"]["MSE"])
    print("MSE_test:", df_evaluation_test.loc["mean"]["MSE"])

    
    # with open(PATH_MODEL / "evaluation_test.json", "w") as f:
    #     json.dump(evaluation_test, f, indent=2)
    # df_evaluation_test.to_csv(PATH_MODEL / "evaluation_test.csv")