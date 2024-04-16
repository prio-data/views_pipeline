import sys
from pathlib import Path
import numpy as np
import pandas as pd
import wandb
from sklearn.metrics import mean_squared_error

PATH = Path(__file__)  
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)

from xgboost import XGBRegressor, XGBClassifier

from views_partitioning.data_partitioner import DataPartitioner
from views_forecasts.extensions import *
from stepshift.views import StepshiftedModels
from views_stepshift.run import ViewsRun
from hurdle_model import HurdleRegression
from get_data import get_partition_data

def evaluate_sweep(model_config, para_config):
    if model_config["algorithm"] == "HurdleRegression":
        model = HurdleRegression(clf_name=model_config["clf_name"], reg_name=model_config["reg_name"], clf_params=para_config["clf"], reg_params=para_config["reg"])
    else:
        model = globals()[model_config["algorithm"]](**para_config)
    _, PATH_RAW, _, _ = setup_data_paths(PATH)
    dataset = pd.read_parquet(PATH_RAW / 'raw.parquet')

    stepshifter_model_calib = stepshift_training(model_config, "calib", model, get_partition_data(dataset, "calibration"))
    stepshifter_model_test = stepshift_training(model_config, "test", model, get_partition_data(dataset, "testing"))

    print('Evaluating...')
    
    steps = model_config["steps"]
    stepcols = [model_config["depvar"]]
    for step in steps:
        stepcols.append("step_pred_" + str(step))
    
    
    df_calib = stepshifter_model_calib.predict("calib", "predict", get_partition_data(dataset, "calibration"))
    df_test = stepshifter_model_test.predict("test", "predict", get_partition_data(dataset, "testing"))

    df_calib = df_calib.replace([np.inf, -np.inf], 0)[stepcols]
    df_test = df_test.replace([np.inf, -np.inf], 0)[stepcols]

    pred_cols = [f"step_pred_{str(i)}" for i in steps]
    df_calib["mse"] = df_calib.apply(lambda row: mean_squared_error([row[model_config["depvar"]]] * 36,
                                                        [row[col] for col in pred_cols]), axis=1)
    df_test["mse"] = df_test.apply(lambda row: mean_squared_error([row[model_config["depvar"]]] * 36,
                                                        [row[col] for col in pred_cols]), axis=1)
    
    wandb.log({'MSE_calib': df_calib['mse'].mean()})
    wandb.log({'MSE_test': df_test['mse'].mean()})

def stepshift_training(model_config, partition_name, model, dataset):
    steps = model_config["steps"]
    target = model_config["depvar"]
    partition = DataPartitioner({partition_name: model_config[f"{partition_name}_partitioner_dict"]})
    stepshifter_def = StepshiftedModels(model, steps, target)
    stepshifter_model = ViewsRun(partition, stepshifter_def)
    stepshifter_model.fit(partition_name, "train", dataset)
    return stepshifter_model
