import numpy as np
import pandas as pd
import wandb
from pathlib import Path
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor

import sys
src_path = f"{Path(__file__).parent.parent}"
sys.path.append(str(src_path)+"/utils")

from utils import get_data_path
from views_partitioning.data_partitioner import DataPartitioner
from views_forecasts.extensions import *
from stepshift.views import StepshiftedModels
from views_stepshift.run import ViewsRun

def evaluate_sweep(common_config, para_config):
    model = globals()[common_config["algorithm"]](**para_config)
    dataset = pd.read_parquet(get_data_path("raw"))

    stepshifter_model_calib = stepshift_training(common_config, "calib", model, dataset)
    stepshifter_model_test = stepshift_training(common_config, "test", model, dataset)

    print('Evaluating...')
    
    steps = common_config["steps"]
    stepcols = [common_config["depvar"]]
    for step in steps:
        stepcols.append("step_pred_" + str(step))
    
    
    df_calib = stepshifter_model_calib.predict("calib", "predict", dataset)
    df_test = stepshifter_model_test.predict("test", "predict", dataset)

    df_calib = df_calib.replace([np.inf, -np.inf], 0)[stepcols]
    df_test = df_test.replace([np.inf, -np.inf], 0)[stepcols]

    pred_cols = [f"step_pred_{str(i)}" for i in steps]
    df_calib["mse"] = df_calib.apply(lambda row: mean_squared_error([row["ged_sb_dep"]] * 36,
                                                        [row[col] for col in pred_cols]), axis=1)
    df_test["mse"] = df_test.apply(lambda row: mean_squared_error([row["ged_sb_dep"]] * 36,
                                                        [row[col] for col in pred_cols]), axis=1)
    
    wandb.log({'MSE_calib': df_calib['mse'].mean()})
    wandb.log({'MSE_test': df_test['mse'].mean()})

def stepshift_training(common_config, partition_name, model, dataset):
    steps = common_config["steps"]
    target = common_config["depvar"]
    partition = DataPartitioner({partition_name: common_config[f"{partition_name}_partitioner_dict"]})
    stepshifter_def = StepshiftedModels(model, steps, target)
    stepshifter_model = ViewsRun(partition, stepshifter_def)
    stepshifter_model.fit(partition_name, "train", dataset)
    return stepshifter_model
