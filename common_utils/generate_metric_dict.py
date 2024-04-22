# KLD and Jeffreys divergence are measures used to quantify the difference between two probability distributions. Why do we calculate these metrics in the context of forecasting?
# There are negative values, so errors occur when calculating MSLE
# Brier score is used for binary and categorical outcomes that can be structured as true or false
# There are no classes in data, so we cannot calculate roc_auc_score, ap_score
import properscoring as ps
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_squared_log_error, brier_score_loss, average_precision_score, roc_auc_score
from utils_evaluation_metrics import EvaluationMetrics
from views_forecasts.extensions import *

def generate_metric_dict(df, steps, depvar):
    evaluation_dict = EvaluationMetrics.make_evaluation_dict(steps=steps[-1])
    for step in steps:
        evaluation_dict[f"step{str(step).zfill(2)}"].MSE = mean_squared_error(df[depvar], df[f"step_pred_{step}"])
        evaluation_dict[f"step{str(step).zfill(2)}"].MAE = mean_absolute_error(df[depvar], df[f"step_pred_{step}"])
        # evaluation_dict[f"step{str(step).zfill(2)}"].MSLE = mean_squared_log_error(df[depvar], df[f"step_pred_{step}"])
        evaluation_dict[f"step{str(step).zfill(2)}"].CRPS = ps.crps_ensemble(df[depvar], df[f"step_pred_{step}"]).mean()
        # evaluation_dict[f"step{str(step).zfill(2)}"].Brier = brier_score_loss(df[depvar], df[f"step_pred_{step}"])
        # evaluation_dict[f"step{str(step).zfill(2)}"].AUC = roc_auc_score(df[depvar], df[f"step_pred_{step}"])
        # evaluation_dict[f"step{str(step).zfill(2)}"].AP = average_precision_score(df[depvar], df[f"step_pred_{step}"])
    evaluation_dict = EvaluationMetrics.output_metrics(evaluation_dict)
    df_evaluation_dict = EvaluationMetrics.evaluation_dict_to_dataframe(evaluation_dict)  
    return evaluation_dict, df_evaluation_dict
