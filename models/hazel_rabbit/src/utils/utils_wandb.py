import numpy as np
from sklearn.metrics import mean_squared_error, average_precision_score, roc_auc_score, brier_score_loss
import wandb

# there are things in other utils that should be here...

def add_wandb_monthly_metrics():
        
    # Define "new" monthly metrics for WandB logging
    wandb.define_metric("monthly/out_sample_month")
    wandb.define_metric("monthly/*", step_metric="monthly/out_sample_month")


def log_wandb_monthly_metrics(config, mse_list, ap_list, auc_list, brier_list):
    
    """
    Logs evaluation metrics to WandB.

    This function computes the mean of provided metrics and logs them to WandB.
    The metrics include mean squared error, average precision score, ROC AUC score, and Brier score loss.

    Args:
        config : Configuration object containing parameters and settings.
        mse_list : List of monthly mean squared errors.
        ap_list : List of monthly average precision scores.
        auc_list : List of monthly ROC AUC scores.
        brier_list : List of monthly Brier scores.

    """

    wandb.log({f"{config.time_steps}month_mean_squared_error": np.mean(mse_list)})
    wandb.log({f"{config.time_steps}month_average_precision_score": np.mean(ap_list)})
    wandb.log({f"{config.time_steps}month_roc_auc_score": np.mean(auc_list)})
    wandb.log({f"{config.time_steps}month_brier_score_loss": np.mean(brier_list)})