from sklearn.metrics import mean_squared_error, average_precision_score, roc_auc_score, brier_score_loss
import pandas as pd
import matplotlib.pyplot as plt

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)

from utils_model_outputs import ModelOutputs
from utils_evaluation_metrics import EvaluationMetrics

def output_to_df(dict_of_outputs_dicts):
    
    """
    Converts the dictionary of model outputs into a consolidated pandas DataFrame, formatted for HydraNet.

    This function takes dictionaries of model outputs for different target variables ('sb', 'ns', 'os'), 
    converts them into separate DataFrames, renames columns to distinguish between different targets, 
    and then merges them into a single DataFrame. The merged DataFrame excludes ocean cells (where `c_id == 0`).

    Args:
        dict_of_outputs_dicts (dict): A dictionary containing sub-dictionaries of model outputs 
                                      for different targets ('sb', 'ns', 'os'). Each sub-dictionary 
                                      should be structured with keys as steps and values as `ModelOutputs` instances.

    Returns:
        df_all (pd.DataFrame): A DataFrame where columns from different targets are suffixed with '0', '1', or '2' 
                      respectively. The DataFrame is cleaned to exclude ocean cells and has columns 
                      properly typed for use in HydraNet.

    Example:
        >>> dict_of_outputs_dicts = {
                'sb': {'step01': ModelOutputs(...), ...},
                'ns': {'step01': ModelOutputs(...), ...},
                'os': {'step01': ModelOutputs(...), ...}
            }
        >>> df_full = output_to_df(dict_of_outputs_dicts)
        >>> print(df_full.head())
    """

     # Example usage with 'sb', 'ns', 'os'
    df_sb = ModelOutputs.output_dict_to_dataframe(dict_of_outputs_dicts["sb"])
    df_ns = ModelOutputs.output_dict_to_dataframe(dict_of_outputs_dicts["ns"])
    df_os = ModelOutputs.output_dict_to_dataframe(dict_of_outputs_dicts["os"])

    # SO FROM HERE IT GETS VERY HydraNet SPECIFIC. 
    common_cols = ["pg_id", "c_id", "month_id", "step"]

    # rename the columns so that the onse in df_test2 ends with a 0 and the ones in df_test3 ends with a 1. don't change the common columns
    df_sb.columns = [f"{i}_sb" if i not in common_cols else i for i in df_sb.columns]
    df_ns.columns = [f"{i}_ns" if i not in common_cols else i for i in df_ns.columns]
    df_os.columns = [f"{i}_os" if i not in common_cols else i for i in df_os.columns]

    # drop the pg_id and c_id columns from df_ns and df_os - bc concat is faster than merge when they are sorted the same way.
    df_sb = df_sb.drop(columns=common_cols)
    df_ns = df_ns.drop(columns=common_cols)

    # merge the dataframes
    df_all = pd.concat([df_sb, df_ns, df_os], axis=1)

    # drop ocean cells, i.e. where c_id == 0
    df_all = df_all[df_all["c_id"] != 0]

    # no you can just drop it
    df_all = df_all.reset_index(drop=True)

    # change all columns to float
    df_all = df_all.astype(float)

    # make the binary columns integers
    df_all = df_all.astype({"y_true_binary_sb": int, "y_true_binary_ns": int, "y_true_binary_os": int, "month_id" : int, "step" : int})

    # print the df
    #df_all

    return df_all


def evaluation_to_df(dict_of_eval_dicts):

    """
    Converts a dictionary of evaluation metric dictionaries into a consolidated DataFrame.

    This function takes a dictionary containing evaluation metric dictionaries for different features
    ('sb', 'ns', 'os'), converts each evaluation dictionary to a DataFrame, renames the columns to 
    reflect their respective feature, and merges them into a single DataFrame.

    Args:
        dict_of_eval_dicts (Dict[str, Dict[str, EvaluationMetrics]]): A dictionary where keys are feature 
            identifiers ('sb', 'ns', 'os') and values are dictionaries of evaluation metrics per time step 
            for each feature. Each evaluation metric dictionary is expected to contain instances of `EvaluationMetrics`.

    Returns:
        pd.DataFrame: A consolidated DataFrame containing evaluation metrics for all features. The DataFrame 
        includes columns for each metric with suffixes '_sb', '_ns', and '_os' to denote the feature they belong to.
        Each row corresponds to a specific time step across the different features.

    Example:
        >>> dict_of_eval_dicts = {
        ...     'sb': {'step01': EvaluationMetrics(MSE=0.1, AP=0.2, AUC=0.3, Brier=0.4), ...},
        ...     'ns': {'step01': EvaluationMetrics(MSE=0.5, AP=0.6, AUC=0.7, Brier=0.8), ...},
        ...     'os': {'step01': EvaluationMetrics(MSE=0.9, AP=1.0, AUC=1.1, Brier=1.2), ...}
        ... }
        >>> df_all_eval = evaluation_to_df(dict_of_eval_dicts)
        >>> print(df_all_eval.head())
           MSE_sb  AP_sb  AUC_sb  Brier_sb  ...  MSE_os  AP_os  AUC_os  Brier_os
        0     0.1    0.2     0.3       0.4  ...     0.9    1.0     1.1       1.2
        ...
    """

    df_sb_eval = EvaluationMetrics.evaluation_dict_to_dataframe(dict_of_eval_dicts['sb'])
    df_ns_eval = EvaluationMetrics.evaluation_dict_to_dataframe(dict_of_eval_dicts['sb'])
    df_os_eval = EvaluationMetrics.evaluation_dict_to_dataframe(dict_of_eval_dicts['sb'])

    df_sb_eval.columns = [f"{i}_sb" for i in df_os_eval.columns]
    df_ns_eval.columns = [f"{i}_ns" for i in df_os_eval.columns]
    df_os_eval.columns = [f"{i}_os" for i in df_os_eval.columns]

    # merge the dataframes
    df_all_eval = pd.concat([df_sb_eval, df_ns_eval, df_os_eval], axis=1)

    return df_all_eval


def plot_metrics(df_all, feature = 0):

    """
    Plots MSE, Average Precision, ROC AUC, and Brier Score for each month from log_dict_list.

    Args:
        log_dict_list (list of dict): List of dictionaries with monthly metrics.
        num_months (int): Number of months to plot.
    """

    # Initialize lists to store metrics for each month
    mse_list = []
    ap_list = []
    auc_list = []
    brier_list = []

    df_all["month"] = df_all["step"] #super quick fix, super lazy


    # Iterate over the log_dict_list and extract the metrics
    for i in df_all["month"].unique():

        y_score = df_all[df_all["month"] == i][f"y_score_{feature}"]
        y_score_prob = df_all[df_all["month"] == i][f"y_score_prob_{feature}"]
        y_true = df_all[df_all["month"] == i][f"y_true_{feature}"]
        y_true_binary = df_all[df_all["month"] == i][f"y_true_binary_{feature}"]

        mse = mean_squared_error(y_true, y_score)
        ap = average_precision_score(y_true_binary, y_score_prob)
        auc = roc_auc_score(y_true_binary, y_score_prob)
        brier = brier_score_loss(y_true_binary, y_score_prob)


        mse_list.append(mse)
        ap_list.append(ap)
        auc_list.append(auc)
        brier_list.append(brier)

    # Create subplots
    fig, axs = plt.subplots(2, 2, figsize=(20, 10))

    # Plot MSE
    axs[0, 0].plot(range(1, len(mse_list) + 1), mse_list, marker='o', color='b', label='MSE')
    axs[0, 0].set_title('Mean Squared Error')
    axs[0, 0].set_xlabel('Month')
    axs[0, 0].set_ylabel('MSE')
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # Plot Average Precision
    axs[0, 1].plot(range(1, len(ap_list) + 1), ap_list, marker='o', color='g', label='Average Precision')
    axs[0, 1].set_title('Average Precision Score')
    axs[0, 1].set_xlabel('Month')
    axs[0, 1].set_ylabel('AP Score')
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # Plot ROC AUC
    axs[1, 0].plot(range(1, len(auc_list) + 1), auc_list, marker='o', color='r', label='ROC AUC')
    axs[1, 0].set_title('ROC AUC Score')
    axs[1, 0].set_xlabel('Month')
    axs[1, 0].set_ylabel('AUC Score')
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # Plot Brier Score
    axs[1, 1].plot(range(1, len(brier_list) + 1), brier_list, marker='o', color='m', label='Brier Score')
    axs[1, 1].set_title('Brier Score Loss')
    axs[1, 1].set_xlabel('Month')
    axs[1, 1].set_ylabel('Brier Score')
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    # add a title
    plt.suptitle(f'Metrics for Feature {feature} Over {df_all["month"].max()} Months', fontsize=16)

    # Adjust layout
    plt.tight_layout()

    # Show plots
    plt.show()
