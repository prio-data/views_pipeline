import numpy as np
from sklearn.metrics import mean_squared_error, average_precision_score, roc_auc_score, brier_score_loss
import wandb

# there are things in other utils that should be here...

def add_wandb_monthly_metrics():
        
    # Define "new" monthly metrics for WandB logging
    wandb.define_metric("monthly/out_sample_month")
    wandb.define_metric("monthly/*", step_metric="monthly/out_sample_month")

# not the monthly but the mean (and they are wrong... )
#def log_wandb_mean_metrics(config, mse_list, ap_list, auc_list, brier_list):
#    
#    """
#    Logs evaluation metrics to WandB.
#
#    This function computes the mean of provided metrics and logs them to WandB.
#    The metrics include mean squared error, average precision score, ROC AUC score, and Brier score loss.
#
#    Args:
#        config : Configuration object containing parameters and settings.
#        mse_list : List of monthly mean squared errors.
#        ap_list : List of monthly average precision scores.
#        auc_list : List of monthly ROC AUC scores.
#        brier_list : List of monthly Brier scores.
#
#    """
#
#    wandb.log({f"{config.time_steps}month_mean_squared_error": np.mean(mse_list)})
#    wandb.log({f"{config.time_steps}month_average_precision_score": np.mean(ap_list)})
#    wandb.log({f"{config.time_steps}month_roc_auc_score": np.mean(auc_list)})
#    wandb.log({f"{config.time_steps}month_brier_score_loss": np.mean(brier_list)})
#


def log_wandb_mean_metrics(config, df_eval):
    """
    Logs evaluation metrics to WandB.

    This function computes the mean of provided metrics and logs them to WandB for different targets.
    The metrics include mean squared error, average precision score, ROC AUC score, and Brier score loss.

    Args:
        config : Configuration object containing parameters and settings.
        df_eval (pd.DataFrame): DataFrame containing evaluation metrics with columns 
                                ['mean_squared_error_sb', 'average_precision_score_sb', 
                                 'roc_auc_score_sb', 'brier_score_loss_sb', 
                                 'mean_squared_error_ns', 'average_precision_score_ns', 
                                 'roc_auc_score_ns', 'brier_score_loss_ns', 
                                 'mean_squared_error_os', 'average_precision_score_os', 
                                 'roc_auc_score_os', 'brier_score_loss_os'].
    """
    # Drop NaN values before computing means
    metric_means = df_eval.mean(axis=0, skipna=True)

    metrics = ['mean_squared_error', 'average_precision_score', 'roc_auc_score', 'brier_score_loss']
    targets = ['sb', 'ns', 'os']

    # Log metrics for each target
    for target in targets:
        for metric in metrics:
            metric_name = f"{config.time_steps}month_{metric}_{target}"
            metric_value = metric_means.get(f"{metric}_{target}")
            #if pd.notna(metric_value):
            wandb.log({metric_name: metric_value})

    print(f"Logged metrics to WandB for targets: {targets}")




def generate_wandb_log_dict(log_dict, dict_of_eval_dicts, feature, step):
    
    for key, value in dict_of_eval_dicts[feature][step].__dict__.items():
        if value is not None:
            log_dict[f"monthly/{key}_{feature}"] = value

    return log_dict 


# old and I think deprecated... Or is this used???
def get_log_dict(i, mean_array, mean_class_array, std_array, std_class_array, out_of_sample_vol, config):

    """Return a dictionary of metrics for the monthly out-of-sample predictions for W&B."""

    log_dict = {}
    log_dict["monthly/out_sample_month"] = i


    #Fix in a sec when you see if it runs at all.... 
    for j in range(3): #(config.targets): # TARGETS IS & BUT THIS SHOULD BE 3!!!!!

        y_score = mean_array[i,j,:,:].reshape(-1) # make it 1d  # nu 180x180 
        y_score_prob = mean_class_array[i,j,:,:].reshape(-1) # nu 180x180 
        
        # do not really know what to do with these yet.
        y_var = std_array[i,j,:,:].reshape(-1)  # nu 180x180  
        y_var_prob = std_class_array[i,j,:,:].reshape(-1)  # nu 180x180 

        y_true = out_of_sample_vol[:,i,j,:,:].reshape(-1)  # nu 180x180 . dim 0 is time
        y_true_binary = (y_true > 0) * 1


        mse = mean_squared_error(y_true, y_score)
        ap = average_precision_score(y_true_binary, y_score_prob)
        auc = roc_auc_score(y_true_binary, y_score_prob)
        brier = brier_score_loss(y_true_binary, y_score_prob)

        log_dict[f"monthly/mean_squared_error{j}"] = mse
        log_dict[f"monthly/average_precision_score{j}"] = ap
        log_dict[f"monthly/roc_auc_score{j}"] = auc
        log_dict[f"monthly/brier_score_loss{j}"] = brier

    return log_dict
