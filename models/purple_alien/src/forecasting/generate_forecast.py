import os

import numpy as np
import pickle
import time
import functools

import torch
import torch.nn as nn
import torch.nn.functional as F

import wandb

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)


from utils import choose_model, choose_loss, choose_sheduler, get_train_tensors, get_full_tensor, apply_dropout, execute_freeze_h_option, get_log_dict, train_log, init_weights, get_data
from utils_prediction import predict, sample_posterior
from config_hyperparameters import get_hp_config


def generate_forecast(model, views_vol, config, device, PATH):
    """
    Function to generate forecast using the provided model and views_vol.
    It saves the generated posterior distributions and out-of-sample volumes.
    
    Args:
        model: The trained model used for forecasting.
        views_vol: The input data tensor for forecasting.
        config: Configuration object containing settings.
        device: The device (CPU or GPU) to run the predictions on.
        PATH: The base path where generated data will be saved.
    
    Returns:
        None
    """
    # Ensure the model is in evaluation mode
    model.eval()
    model.apply(apply_dropout)

    # Generate posterior samples and out-of-sample volumes
    posterior_list, posterior_list_class, out_of_sample_vol, _ = sample_posterior(model, views_vol, config, device) # the _ is the full tensor. 
    
    # I suspect you'll need the out_of_sample_vol to create the df (it has pg and ocean info)
    # However, I see in the test_prediction_store notebook in "conflictnet" repo that I load the "calibration_vol" from the pickle file.... Investigate... 


    # Set up paths for storing generated data
    _, _, PATH_GENERATED = setup_data_paths(PATH)

    # Create the directory if it does not exist
    os.makedirs(PATH_GENERATED, exist_ok=True)

    # Print the path for debugging
    print(f'PATH to generated data: {PATH_GENERATED}')

    # Create a dictionary to store posterior data
    posterior_dict = {
        'posterior_list': posterior_list,
        'posterior_list_class': posterior_list_class,
        'out_of_sample_vol': out_of_sample_vol          # you might need this for the df creation before predstore. Experiments in notebook test_to_prediction_store.ipynb
    }

    # Save the posterior data to a pickle file
    filename = f'posterior_dict_{config.time_steps}_{config.run_type}_{config.model_time_stamp}.pkl'
    with open(os.path.join(PATH_GENERATED, filename), 'wb') as file:
        pickle.dump(posterior_dict, file)

    print('Posterior dict and test vol pickled and dumped!')


def forecast_with_model_artifact(config, device, views_vol, PATH_ARTIFACTS, artifact_name=None):
#def handle_forecasting(config, device, views_vol, PATH_ARTIFACTS, artifact_name=None):

    """
    ...
    """

    # the thing above might work, but it needs to be tested thoroughly....
    raise NotImplementedError('Forecasting not implemented yet')




# Ensure utils_prediction.py and any other dependencies are imported correctly
# from utils_prediction import sample_posterior, apply_dropout
# from utils_data import setup_data_paths


















## you always load an artifact for forecasting - like with the evaluate you take the latest artifact unless you specify another one
## But that is done in main.py - just passed to here as an argument
#
## Then the load the offical forescasting partition
## And the first steps must be usign the function from utils_prediction.py to get the predictions and the posetrior
#
## model, views_vol, config, device should be passed as arguments to this function
#
#def generate_forecast(model, views_vol, config, device):
#
#
#    # THIS IS ALL PURE MESS RIGHT NOW!!! 
#
#
#    posterior_list, posterior_list_class, out_of_sample_vol, full_tensor = sample_posterior(model, views_vol, config, device)
#
## then to prediction store I guess? Or perhaps just the generated data for now... 
#
#    _ , _, PATH_GENERATED = setup_data_paths(PATH)
#
#    # if the path does not exist, create it
#
#    if not os.path.exists(PATH_GENERATED):
#
#        os.makedirs(PATH_GENERATED)
#
#    # print for debugging
#    print(f'PATH to generated data: {PATH_GENERATED}')
#
#    # pickle the posterior dict, metric dict, and test vol
#
#    # Should be time_steps and run_type in the name....
#    posterior_dict = {'posterior_list' : posterior_list, 'posterior_list_class': posterior_list_class, 'out_of_sample_vol' : out_of_sample_vol}
#
#
#    with open(f'{PATH_GENERATED}/posterior_dict_{config.time_steps}_{config.run_type}_{config.model_time_stamp}.pkl', 'wb') as file:
#
#        pickle.dump(posterior_dict, file)       
#
#
#    print('Posterior dict, metric dict and test vol pickled and dumped!')
#
#