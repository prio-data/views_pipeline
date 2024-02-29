import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_squared_error

import sys
src_path = f"{Path(__file__).parent.parent}"
sys.path.append(str(src_path)+"/utils")

# Remove this part after packaging views_stepshift
current_file_path = Path(__file__).resolve()
root_path = current_file_path.parent.parent.parent.parent.parent
sys.path.append(str(root_path))

from views_forecasts.extensions import *
from utils import get_artifacts_path, get_data_path


def evaluate_model(config):
    print("Evaluating...")

    stepshifter_model = pd.read_pickle(get_artifacts_path("future"))
    dataset = pd.read_parquet(get_data_path("raw"))

    steps = config["steps"]
    stepcols = [config["depvar"]]
    for step in steps:
        stepcols.append("step_pred_" + str(step))

    try:
        df = pd.DataFrame.forecasts.read_store(name=config["name"])
    except:
        df = stepshifter_model.predict("future", "predict", dataset)
        df.forecasts.to_store(name=config["name"])

    df = df.replace([np.inf, -np.inf], 0)[stepcols]

    pred_cols = [f"step_pred_{str(i)}" for i in steps]
    df["mse"] = df.apply(lambda row: mean_squared_error([row["ged_sb_dep"]] * 36,
                                                        [row[col] for col in pred_cols]), axis=1)
    print(df["mse"].mean())