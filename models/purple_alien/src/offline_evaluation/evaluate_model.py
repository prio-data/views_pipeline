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


from utils import choose_model, choose_loss, choose_sheduler, get_train_tensors, get_full_tensor, apply_dropout, execute_freeze_h_option, get_log_dict, train_log, init_weights, get_data
from utils_prediction import predict, sample_posterior
from artifacts_utils import get_latest_model_artifact
from config_sweep import get_swep_config
from config_hyperparameters import get_hp_config



# should be called evaluate_posterior.... 
def evaluate_posterior(model, views_vol, config, device):

    """
    Function to sample from and evaluate the posterior distribution of Hydranet.
    """

    posterior_list, posterior_list_class, out_of_sample_vol, full_tensor = sample_posterior(model, views_vol, config, device)

    # YOU ARE MISSING SOMETHING ABOUT FEATURES HERE WHICH IS WHY YOU REPORTED AP ON WandB IS BIASED DOWNWARDS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!RYRYRYRYERYERYR
    # need to check you "offline" evaluation script which is correctlly implemented before you use this function for forecasting.
    
    # Get mean and std
    mean_array = np.array(posterior_list).mean(axis = 0) # get mean for each month!
    std_array = np.array(posterior_list).std(axis = 0)

    mean_class_array = np.array(posterior_list_class).mean(axis = 0) # get mean for each month!
    std_class_array = np.array(posterior_list_class).std(axis = 0)

    out_sample_month_list = [] # only used for pickle...
    ap_list = []
    mse_list = []
    auc_list = []
    brier_list = []

    for i in range(mean_array.shape[0]): #  0 of mean array is the temporal dim

        y_score = mean_array[i].reshape(-1) # make it 1d  # nu 180x180
        y_score_prob = mean_class_array[i].reshape(-1) # nu 180x180

        # do not really know what to do with these yet.
        y_var = std_array[i].reshape(-1)  # nu 180x180
        y_var_prob = std_class_array[i].reshape(-1)  # nu 180x180

        y_true = out_of_sample_vol[:,i].reshape(-1)  # nu 180x180 . dim 0 is time
        y_true_binary = (y_true > 0) * 1

        mse = mean_squared_error(y_true, y_score)  
        ap = average_precision_score(y_true_binary, y_score_prob)
        auc = roc_auc_score(y_true_binary, y_score_prob)
        brier = brier_score_loss(y_true_binary, y_score_prob)

        log_dict = get_log_dict(i, mean_array, mean_class_array, std_array, std_class_array, out_of_sample_vol, config)# so at least it gets reported sep.

        wandb.log(log_dict)

        out_sample_month_list.append(i) # only used for pickle...
        mse_list.append(mse)
        ap_list.append(ap) # add to list.
        auc_list.append(auc)
        brier_list.append(brier)


    if not config.sweep:
            
        _ , _, PATH_GENERATED = setup_data_paths(PATH)

        # if the path does not exist, create it
        if not os.path.exists(PATH_GENERATED):
            os.makedirs(PATH_GENERATED)

        # print for debugging
        print(f'PATH to generated data: {PATH_GENERATED}')

        # pickle the posterior dict, metric dict, and test vol
        # Should be time_steps and run_type in the name....

        posterior_dict = {'posterior_list' : posterior_list, 'posterior_list_class': posterior_list_class, 'out_of_sample_vol' : out_of_sample_vol}

        metric_dict = {'out_sample_month_list' : out_sample_month_list, 'mse_list': mse_list,
                        'ap_list' : ap_list, 'auc_list': auc_list, 'brier_list' : brier_list}


        # Note: we are using the model_time_stamp from the model artifact to denote the time stamp for the pkl files
        # This is to ensure that the pkl files are easily identifiable and associated with the correct model artifact
        # But it also means that running evaluation on the same model artifact multiple times will overwrite the pkl files
        # I think this is fine, but we should think about cases where we might want to evaluate the same model artifact multiple times - maybe for robustiness checks or something for publication. 

        with open(f'{PATH_GENERATED}/posterior_dict_{config.time_steps}_{config.run_type}_{config.model_time_stamp}.pkl', 'wb') as file:
            pickle.dump(posterior_dict, file)       

        with open(f'{PATH_GENERATED}/metric_dict_{config.time_steps}_{config.run_type}_{config.model_time_stamp}.pkl', 'wb') as file:
            pickle.dump(metric_dict, file)

        with open(f'{PATH_GENERATED}/test_vol_{config.time_steps}_{config.run_type}_{config.model_time_stamp}.pkl', 'wb') as file: # make it numpy
            pickle.dump(full_tensor.cpu().numpy(), file)

        print('Posterior dict, metric dict and test vol pickled and dumped!')


    else:
        print('Running sweep. NO posterior dict, metric dict, or test vol pickled+dumped')

    # could be a function in utils_wandb....
    wandb.log({f"{config.time_steps}month_mean_squared_error": np.mean(mse_list)})
    wandb.log({f"{config.time_steps}month_average_precision_score": np.mean(ap_list)})
    wandb.log({f"{config.time_steps}month_roc_auc_score": np.mean(auc_list)})
    wandb.log({f"{config.time_steps}month_brier_score_loss":np.mean(brier_list)})


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
        
        # If it lacks the file extension, add it
        if not artifact_name.endswith('.pt'):
            artifact_name += '.pt'
        
        # Define the full (model specific) path for the artifact
        PATH_MODEL_ARTIFACT = os.path.join(PATH_ARTIFACTS, artifact_name)
    
    else:
        # use the latest model artifact based on the run type
        print(f"Using latest (default) run type ({config.run_type}) specific artifact")
        
        # Get the latest model artifact based on the run type and the (models specific) artifacts path
        PATH_MODEL_ARTIFACT = get_latest_model_artifact(PATH_ARTIFACTS, config.run_type)

    # Check if the model artifact exists - if not, raise an error
    if not os.path.exists(PATH_MODEL_ARTIFACT):
        raise FileNotFoundError(f"Model artifact not found at {PATH_MODEL_ARTIFACT}")

    # load the model
    model = torch.load(PATH_MODEL_ARTIFACT)
    
    # get the exact model date_time stamp for the pkl files made in the evaluate_posterior from evaluation.py
    model_time_stamp = os.path.basename(PATH_MODEL_ARTIFACT)[-18:-3] # 18 is the length of the timestamp string, and -3 is to remove the .pt file extension. a bit hardcoded, but very simple and should not change.

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