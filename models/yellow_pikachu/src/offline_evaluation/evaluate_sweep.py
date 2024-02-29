import numpy as np
import pandas as pd
import wandb
from pathlib import Path
from sklearn.metrics import mean_squared_error

import sys
src_path = f"{Path(__file__).parent.parent}"
sys.path.append(str(src_path)+"/utils")

from utils import get_artifacts_path, get_data_path

def evaluate_sweep(config):
    print('Evaluating...')
    # Not sure how to save the sweep model, so temporarily loading it from the artifacts
    model = pd.read_pickle(get_artifacts_path("future"))
    dataset = pd.read_parquet(get_data_path("raw"))

    steps = config["steps"]
    stepcols = [config["depvar"]]
    for step in steps:
        stepcols.append("step_pred_" + str(step))
    
    
    df = model.predict("future", "test", dataset)
    df = df.replace([np.inf, -np.inf], 0)[stepcols]

    pred_cols = [f"step_pred_{str(i)}" for i in steps]
    df["mse"] = df.apply(lambda row: mean_squared_error([row["ged_sb_dep"]] * 36,
                                                        [row[col] for col in pred_cols]), axis=1)
    
    wandb.log({'mse': df['mse'].mean()})
