import sys
from pathlib import Path
import numpy as np
import pandas as pd
import wandb
from sklearn.metrics import mean_squared_error

PATH = Path(__file__)  
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)

from get_data import get_partition_data

def evaluate_sweep(config, stepshift_model):
    PATH_RAW, _, _ = setup_data_paths(PATH)

    run_type = config["run_type"]
    steps = config["steps"]
    stepcols = [config["depvar"]]
    for step in steps:
        stepcols.append("step_pred_" + str(step))

    dataset = pd.read_parquet(PATH_RAW / f'raw_{run_type}.parquet')

    df = stepshift_model.predict(run_type, "predict", get_partition_data(dataset, run_type))
    df = df.replace([np.inf, -np.inf], 0)[stepcols]
    df = df.mask(df < 0, 0)

    pred_cols = [f"step_pred_{str(i)}" for i in steps]
    df["mse"] = df.apply(lambda row: mean_squared_error([row[config["depvar"]]] * 36,
                                                        [row[col] for col in pred_cols]), axis=1)

    wandb.log({'MSE': df['mse'].mean()})

