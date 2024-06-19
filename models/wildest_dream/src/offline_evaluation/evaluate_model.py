import sys
from pathlib import Path
import numpy as np
import pandas as pd
import json
import warnings

warnings.filterwarnings("ignore")

PATH = Path(__file__)
from set_path import setup_project_paths, setup_data_paths, setup_artifacts_paths, setup_model_paths

setup_project_paths(PATH)
from get_data import get_partition_data
from generate_metric_dict import generate_metric_dict

from views_forecasts.extensions import *


def evaluate_model(model_config):
    print("Evaluating...")

    PATH_MODEL= setup_model_paths(PATH)
    PATH_RAW, _, _ = setup_data_paths(PATH)
    PATH_ARTIFACTS = setup_artifacts_paths(PATH)

    run_type = model_config["run_type"]
    steps = model_config["steps"]
    stepcols = [model_config["depvar"]]
    for step in steps:
        stepcols.append("step_pred_" + str(step))

    dataset = pd.read_parquet(PATH_RAW / 'raw_calibration.parquet')
    try:
        stepshift_model = pd.read_pickle(PATH_ARTIFACTS / f'model_{run_type}_partition.pkl')
    except:
        raise FileNotFoundError("Model not found. Please train the model first.")

    # try:
    #     df = pd.DataFrame.forecasts.read_store(name=f'{model_config["name"]}_{run_type}')
    # except:
    #     df = model.predict(run_type, "predict", get_partition_data(dataset, run_type))
    #     df.forecasts.to_store(name=f'{model_config["name"]}_{run_type}')  #Remember to set the run name in actual implementation

    df = stepshift_model.predict(run_type, "predict", get_partition_data(dataset, run_type))
    df = df.replace([np.inf, -np.inf], 0)[stepcols]
    df = df.mask(df < 0, 0)

    evaluation, df_evaluation = generate_metric_dict(df, steps, model_config["depvar"])

    print(f"MSE_{run_type}:", df_evaluation.loc["mean"]["MSE"])

    with open(PATH_MODEL / f"evaluation_{run_type}.json", "w") as f:
        json.dump(evaluation, f, indent=2)
    df_evaluation.to_csv(PATH_MODEL / f"evaluation_{run_type}.csv")
