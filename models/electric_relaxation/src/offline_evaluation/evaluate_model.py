import numpy as np
import pandas as pd
from pathlib import Path
import pickle
import sys

from sklearn.metrics import mean_squared_error, average_precision_score, roc_auc_score, brier_score_loss

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS
from set_path import setup_project_paths, setup_artifacts_paths, setup_data_paths
setup_project_paths(PATH) #adds all necessary paths to sys.path

from config_model import get_model_config


def evaluate_model(model_config):
    """
    Evaluate a model's performance from the calibration partition.

    This function loads a trained model from a pickle file, predicts outcomes for the calibration dataset,
    calculates mean squared error (MSE), average precision, and Brier score for the predictions,
    and saves the results as a dictionary in the artifacts folder.

    Args:
        model_config (dict): Configuration parameters for the model.

    Returns:
        None

    Notes:
    - There are 36 predictions for every true value (given 36 steps), so I am taking the mean value of them. Open to discuss this further
    - Code for area under ROC curve didn't work, but leaving in for future development
    - Should this also include test partition?
    - When running the script, I get the following error from sklearn.metrics: No positive class found in y_true, recall is set to one for all thresholds.
    - Instead of rewriting the code for metrics, it can be written as a loop or function in utils
    """
    print("Evaluating...")

    PATH_MODEL, PATH_RAW, PATH_PROCESSED, PATH_GENERATED = setup_data_paths(PATH)

    #df_calib = pd.read_parquet(model_path/"data"/"generated"/"calibration_predictions.parquet") 
    df_calib = pd.read_parquet(PATH_GENERATED / "calibration_predictions.parquet") 

    steps = model_config["steps"]
    depvar = [model_config["depvar"]] #formerly stepcols, changed to depvar to also use in true_values

    for step in steps: 
        depvar.append("step_pred_" + str(step))

    df_calib = df_calib.replace([np.inf, -np.inf], 0)[depvar] 

    pred_cols = [f"step_pred_{str(i)}" for i in steps] 
    
    df_calib["mse"] = df_calib.apply(lambda row: mean_squared_error([row[[model_config["depvar"]]]] * len(steps), #not sure why [model_config["depvar"]] works but depvar doesn't (I previously defined it)
                                                        [row[col] for col in pred_cols]), axis=1)
    
    mean_mse = df_calib["mse"].mean()

    df_calib["avg_precision"] = df_calib.apply(lambda row: average_precision_score([row[[model_config["depvar"]]]] * len(steps),
                                                                              [row[col] for col in pred_cols]), axis=1)
    
    mean_avg_precision = df_calib["avg_precision"].mean()


    df_calib["brier_score"] = df_calib.apply(lambda row: brier_score_loss([row[[model_config["depvar"]]]] * len(steps),
                                                                      [row[col] for col in pred_cols]), axis=1)
    mean_brier_score = df_calib["brier_score"].mean()

    metrics_dict_path = PATH_MODEL / "artifacts" / "evaluation_metrics.py"

    evaluation_metrics_calib = {
        "Mean Mean Squared Error": mean_mse,
        "Mean Average Precision": mean_avg_precision,
        "Mean Brier Score": mean_brier_score
    }

    with open(metrics_dict_path, 'w') as file:
        file.write("evaluation_metrics = ")
        file.write(repr(evaluation_metrics_calib))
    
    print("Evaluation metrics stored in artifacts folder!")

    #Doesn't work:
    #df_calib["roc_auc"] = df_calib.apply(lambda row: roc_auc_score([row["ged_sb_dep"]] * 36,
                                                               #[row[col] for col in pred_cols]), axis=1)
    #mean_roc_auc = df_calib["roc_auc"].mean()
    #print("Mean Area under ROC curve:", mean_roc_auc)

    
if __name__ == "__main__":
    model_config = get_model_config()

    evaluate_model(model_config)