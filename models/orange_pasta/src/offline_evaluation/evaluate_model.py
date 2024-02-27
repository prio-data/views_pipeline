import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_squared_error

from views_forecasts.extensions import *
from ..training.train_model import *


def evaluate_model(config):
    print("Evaluating...")

    stepshifter_model = pd.read_pickle(Path(__file__).parent.parent.parent / "artifacts/model_forecasting.pkl")
    dataset = pd.read_parquet(f"{Path(__file__).parent.parent.parent}/data/raw/raw.parquet")


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