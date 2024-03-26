import pandas as pd
from pathlib import Path


def training(data_for_training):
    '''
    This function is used to train the model.
    
    Args:
    data_for_training: The data to be used for training.
    '''
    for i in range(1, 37):
        data_for_forecasting[f"step_pred_{i}"] = 0
    print(data_for_forecasting)
    data_for_forecasting.to_parquet(
        f"{Path(__file__).parent.parent.parent}/data/processed/forecasts.parquet")
    return data_for_forecasting
