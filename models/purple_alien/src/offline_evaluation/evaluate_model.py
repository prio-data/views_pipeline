import os

import numpy as np
import pickle
import time
import functools

import torch
import torch.nn as nn
import torch.nn.functional as F

#from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import average_precision_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import brier_score_loss

import wandb

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)


from utils import choose_model, choose_loss, choose_sheduler, get_train_tensors, get_full_tensor, apply_dropout, execute_freeze_h_option, train_log, init_weights, get_data
from utils_prediction import predict, sample_posterior
from utils_artifacts import get_latest_model_artifact
from utils_wandb import generate_wandb_log_dict, generate_wandb_mean_metrics_log_dict
from config_sweep import get_sweep_config
from config_hyperparameters import get_hp_config
from utils_hydranet_outputs import output_to_df, evaluation_to_df, save_model_outputs, update_output_dict, retrieve_metadata, reshape_vols_to_arrays


from utils_model_outputs import ModelOutputs
from utils_evaluation_metrics import EvaluationMetrics


# so if this is mand more general and the if evals in activated then it should be in the utils_prediction.py file.
# also it could 100% be multiple functions...
def evaluate_posterior(model, views_vol, config, device): # is eval in config?

    """
    Evaluates the posterior predictions from a given model on the provided views_vol, calculates evaluation metrics,
    and logs the results using WandB. Optionally saves the results and generated tensors if not running a sweep.

    Args:
        model (torch.nn.Module): The model used for generating predictions.
        views_vol (np.ndarray): The input volume data used by the model for predictions.
        config (object): Configuration object containing attributes like `time_steps`, `run_type`, and `model_time_stamp`.
        device (torch.device): The device to run the model on (e.g., 'cuda' or 'cpu').

    Returns:
        None
    """ 

    posterior_list, posterior_list_class, out_of_sample_vol, out_of_sample_meta_vol, full_tensor, metadata_tensor = sample_posterior(model, views_vol, config, device)

    # if eval:
    dict_of_eval_dicts = {}
    dict_of_eval_dicts = {k: EvaluationMetrics.make_evaluation_dict(steps=config.time_steps) for k in ["sb", "ns", "os"]}

    dict_of_outputs_dicts = {}
    dict_of_outputs_dicts = {k: ModelOutputs.make_output_dict(steps=config.time_steps) for k in ["sb", "ns", "os"]}

    # Get mean and std
    mean_array = np.array(posterior_list).mean(axis = 0) # get mean for each month!
    std_array = np.array(posterior_list).std(axis = 0)

    mean_class_array = np.array(posterior_list_class).mean(axis = 0) # get mean for each month!
    std_class_array = np.array(posterior_list_class).std(axis = 0)


    for t in range(mean_array.shape[0]): #  0 of mean array is the temporal dim    

        log_dict = {}
        log_dict["monthly/out_sample_month"] = t +1 # 1 indexed, bc the first step is 1 month ahead

        for i, j in enumerate(dict_of_eval_dicts.keys()): # this is the same as the above but with the dict keys

            step = f"step{str(t+1).zfill(2)}"

            # get the scores
            # y_score = mean_array[t,i,:,:].reshape(-1) # make it 1d  # nu 180x180 
            # y_score_prob = mean_class_array[t,i,:,:].reshape(-1) # nu 180x180 

            # do not really know what to do with these yet.
            # y_var = std_array[t,i,:,:].reshape(-1)  # nu 180x180  
            # y_var_prob = std_class_array[t,i,:,:].reshape(-1)  # nu 180x180 

            y_score, y_score_prob, y_var, y_var_prob = reshape_vols_to_arrays(t, i, mean_array, mean_class_array, std_array, std_class_array)

            # see this is the out of sample vol - fine for evaluation but not for forecasting
            # but also the place where you get the pgm.. 

            #if eval:
            y_true = out_of_sample_vol[:,t,i,:,:].reshape(-1)  # nu 180x180 . dim 0 is time     THE TRICK IS NOW TO USE A df -> vol and not out_of_sample_vol...
            y_true_binary = (y_true > 0) * 1

            # in theorty you could just use the metadata tensor to get pg and c id here
            # pg_id = out_of_sample_meta_vol[:,t,0,:,:].reshape(-1)  # nu 180x180, dim 1 is time . dim 2 is feature. feature 0 is pg_id
            # c_id = out_of_sample_meta_vol[:,t,4,:,:].reshape(-1)  # nu 180x180, dim 1 is time . dim 2 is feature. feature 4 is c_id
            # month_id = out_of_sample_meta_vol[:,t,3,:,:].reshape(-1)  # nu 180x180, dim 1 is time . dim 2 is feature. feature 3 is month_id

            # So, using the metadata tensor, you can get the pg_id, c_id, and month_id for each prediction.
            # It is similar to the out_of_sample_meta_vol, but not the specific subset of months
            # What you of course need is the extent the metadata tensor 36 months ahead in time on the right dimensions
            # But then you good, right?

            # if eval
            dict_of_outputs_dicts[j][step].y_true = y_true
            dict_of_outputs_dicts[j][step].y_true_binary = y_true_binary

            #else: # you need to make sure this works for forecasting
                # in theorty you could just use the metadata tensor to get pg and c id here
            #pg_id = out_of_sample_meta_vol[:,t,0,:,:].reshape(-1)  # nu 180x180, dim 1 is time . dim 2 is feature. feature 0 is pg_id
            #c_id = out_of_sample_meta_vol[:,t,4,:,:].reshape(-1)  # nu 180x180, dim 1 is time . dim 2 is feature. feature 4 is c_id
            #month_id = out_of_sample_meta_vol[:,t,3,:,:].reshape(-1)  # nu 180x180, dim 1 is time . dim 2 is feature. feature 3 is month_id

            pg_id, c_id, month_id =  retrieve_metadata(t, out_of_sample_meta_vol = out_of_sample_meta_vol, forecast = False)

            # dict_of_outputs_dicts[j][step].y_score = y_score
            # dict_of_outputs_dicts[j][step].y_score_prob = y_score_prob
            # dict_of_outputs_dicts[j][step].y_var = y_var
            # dict_of_outputs_dicts[j][step].y_var_prob = y_var_prob
            # dict_of_outputs_dicts[j][step].pg_id = pg_id # in theory this should be in the right order
            # dict_of_outputs_dicts[j][step].c_id = c_id # in theory this should be in the right order
            # dict_of_outputs_dicts[j][step].step = t +1 # 1 indexed, bc the first step is 1 month ahead
            # dict_of_outputs_dicts[j][step].month_id = month_id

            dict_of_outputs_dicts = update_output_dict(dict_of_outputs_dicts, t, j, step, y_score, y_score_prob, y_var, y_var_prob, pg_id, c_id, month_id)

            #if eval:   
            dict_of_eval_dicts[j][step].MSE = mean_squared_error(y_true, y_score)
            dict_of_eval_dicts[j][step].AP = average_precision_score(y_true_binary, y_score_prob)
            dict_of_eval_dicts[j][step].AUC = roc_auc_score(y_true_binary, y_score_prob)
            dict_of_eval_dicts[j][step].Brier = brier_score_loss(y_true_binary, y_score_prob)

            # note that this actually upates the dict of eval dicts with new stepwise metric values
            log_dict = generate_wandb_log_dict(log_dict, dict_of_eval_dicts, j, step)

        # if eval:
        wandb.log(log_dict)

    mean_metric_log_dict = generate_wandb_mean_metrics_log_dict(dict_of_eval_dicts)
    wandb.log(mean_metric_log_dict)

    # it should prolly return the stuff below, and then save outside the function.... 
    if not config.sweep:

        posterior_dict = {'posterior_list' : posterior_list, 'posterior_list_class': posterior_list_class, 'out_of_sample_vol' : out_of_sample_vol}
        save_model_outputs(PATH, config, posterior_dict, dict_of_outputs_dicts, dict_of_eval_dicts, full_tensor, metadata_tensor)

    else:
        print('Running sweep. NO posterior dict, metric dict, or test vol pickled+dumped')


def evaluate_model_artifact(config, device, views_vol, PATH_ARTIFACTS, artifact_name=None):
#def handle_evaluation(config, device, views_vol, PATH_ARTIFACTS, artifact_name=None):

    """
    Loads a model artifact and evaluates it given the respective trian and eval set within each data partition (Calibration, Testing).

    This function handles the loading of a model artifact either by using a specified artifact name
    or by selecting the latest model artifact based on the run type (default). It then evaluates the model's
    posterior distribution and prints the result.

    Args:
        config: Configuration object containing parameters and settings.
        device: The device to run the model on (CPU or GPU).
        views_vol: The tensor containing the input data for evaluation.
        PATH_ARTIFACTS: The path where model artifacts are stored.
        artifact_name (optional): The specific name of the model artifact to load. Defaults to None.

    Raises:
        FileNotFoundError: If the specified or default model artifact cannot be found.

    """

    # if an artifact name is provided through the CLI, use it. Otherwise, get the latest model artifact based on the run type
    if artifact_name:
        print(f"Using (non-default) artifact: {artifact_name}")
        
        # If the pytorch artifact lacks the file extension, add it. This is obviously specific to pytorch artifacts, but we are deep in the model code here, so it is fine.
        if not artifact_name.endswith('.pt'):
            artifact_name += '.pt'
        
        # Define the full (model specific) path for the artifact
        #PATH_MODEL_ARTIFACT = os.path.join(PATH_ARTIFACTS, artifact_name)

        # pathlib alternative as per sara's comment
        PATH_MODEL_ARTIFACT = PATH_ARTIFACTS / artifact_name # PATH_ARTIFACTS is already a Path object
    
    else:
        # use the latest model artifact based on the run type
        print(f"Using latest (default) run type ({config.run_type}) specific artifact")
        
        # Get the latest model artifact based on the run type and the (models specific) artifacts path
        PATH_MODEL_ARTIFACT = get_latest_model_artifact(PATH_ARTIFACTS, config.run_type)

    # Check if the model artifact exists - if not, raise an error
    #if not os.path.exists(PATH_MODEL_ARTIFACT):
    #    raise FileNotFoundError(f"Model artifact not found at {PATH_MODEL_ARTIFACT}")
    
    # Pathlib alternative as per sara's comment
    if not PATH_MODEL_ARTIFACT.exists(): # PATH_MODEL_ARTIFACT is already a Path object
        raise FileNotFoundError(f"Model artifact not found at {PATH_MODEL_ARTIFACT}")

    # load the model
    model = torch.load(PATH_MODEL_ARTIFACT)
    
    # get the exact model date_time stamp for the pkl files made in the evaluate_posterior from evaluation.py
    #model_time_stamp = os.path.basename(PATH_MODEL_ARTIFACT)[-18:-3] # 18 is the length of the timestamp string + ".pt", and -3 is to remove the .pt file extension. a bit hardcoded, but very simple and should not change.


    # Pathlib alternative as per sara's comment
    model_time_stamp = PATH_MODEL_ARTIFACT.stem[-15:] # 15 is the length of the timestamp string. This is more robust than the os.path.basename solution above since it does not rely on the file extension.

    # print for debugging
    print(f"model_time_stamp: {model_time_stamp}")

    # add to config for logging and conciseness
    config.model_time_stamp = model_time_stamp

    # evaluate the model posterior distribution
    evaluate_posterior(model, views_vol, config, device)
    
    # done. 
    print('Done testing') 



# note:
# Going with the argparser, there is less of a clear reason to have to separate .py files for evaluation sweeps and single models. I think. Let me know if you disagree.
# naturally its a question of generalization and reusability, and i could see I had a lot of copy paste code between the two scripts.