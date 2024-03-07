#Issue: for every true value there are 36 predicted values


import numpy as np
import pandas as pd
from pathlib import Path
import pickle
import sys

model_path = Path(__file__).resolve().parents[2] 
sys.path.append(str(model_path))
print(sys.path)

from sklearn.metrics import mean_squared_error, average_precision_score, roc_auc_score, brier_score_loss

from views_forecasts.extensions import *

from src.utils.set_paths import get_raw_data_path, get_generated_data_path, get_artifacts_path
from configs.config_model import get_model_config
from src.training.train_model import train 


def evaluate_model(model_config):
    """
    Evaluate a model's performance using the calibration dataset (not yet present: test dataset).

    This function loads a trained model from a pickle file, predicts outcomes for the calibration dataset,
    calculates mean squared error (MSE), average precision, area under ROC curve, and Brier score for the predictions,
    and prints the results.

    Args:
        model_config (dict): Configuration parameters for the model.

    Returns:
        None
    """
    print("Evaluating...")

    ######
    df_calib = pd.read_parquet(model_path/"data"/"generated"/"calibration_predictions.parquet") #doesn't work
    ######

    steps = model_config["steps"]
    depvar = [model_config["depvar"]] #formerly stepcols, changed to depvar to also use in Line 58

    for step in steps: #new addition: don't hardcode 36
        depvar.append("step_pred_" + str(step))

    df_calib = df_calib.replace([np.inf, -np.inf], 0)[depvar] 

    #changed Xiaolong's MSE code to accommodate other evaluation metrics
    pred_cols = [f"step_pred_{str(i)}" for i in steps]
    true_values = [row[depvar] for _, row in df_calib.iterrows()] #formetly hardcoded ged_sb_dep
    predicted_values = [row[col] for col in pred_cols for _, row in df_calib.iterrows()]

    mse = mean_squared_error(true_values, predicted_values)
    avg_precision = average_precision_score(true_values, predicted_values)
    roc_auc = roc_auc_score(true_values, predicted_values)
    brier_score = brier_score_loss(true_values, predicted_values)

    print("MSE:", mse)
    print("Average Precision:", avg_precision)
    print("Area under ROC curve:", roc_auc)
    print("Brier Score:", brier_score)

if __name__ == "__main__":
    # Define model configuration
    model_config = get_model_config()

    # Call the evaluate_model function with the model configuration
    evaluate_model(model_config)