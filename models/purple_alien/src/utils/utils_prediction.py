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
from config_sweep import get_swep_config
from config_hyperparameters import get_hp_config


def predict(model, full_tensor, config, device, is_evalutaion = True):

    """
    Function to create predictions for the Hydranet model.
    The function takes the model, the test tensor, the number of time steps to predict, the config, and the device as input.
    The function returns **two lists of numpy arrays**. One list of the predicted magnitudes and one list of the predicted probabilities.
    Each array is of the shap **fx180x180**, where f is the number of features (currently 3 types of violence).
    """

    # Set the model to evaluation mode
    model.eval() 

    # Apply dropout which is otherwise not applied during eval mode
    model.apply(apply_dropout)

    # create empty lists to store the predictions both counts and probabilities
    pred_np_list = []
    pred_class_np_list = []

    # initialize the hidden state
    h_tt = model.init_hTtime(hidden_channels = model.base, H = 180, W  = 180).float().to(device) # coul auto the...

    # get the sequence length   
    seq_len = full_tensor.shape[1] # get the sequence length 
    
    if is_evalutaion:

        full_seq_len = seq_len -1 # we loop over the full sequence. you need -1 because you are predicting the next month.
        in_sample_seq_len = seq_len - 1 - config.time_steps # but retain the last time_steps for hold-out evaluation

        # These print staments are informative while the model is running, but the implementation is not optimal....
        print(f'\t\t\t\t\t\t\t Evaluation mode. retaining hold out set. Full sequence length: {full_seq_len}', end= '\r')
    
    else:

        full_seq_len = seq_len - 1 + config.time_steps # we loop over the entire sequence plus the additional time_steps for forecasting
        in_sample_seq_len = seq_len - 1 # the in-sample part is now the entire sequence

        print(f'\t\t\t\t\t\t\t Forecasting mode. No hold out set. Full sequence length: {full_seq_len}', end= '\r')

    for i in range(full_seq_len): 

        if i < in_sample_seq_len: # This is the in-sample part and where the out sample part is defined (seq_len-1-time_steps)

            print(f'\t\t\t in sample. month: {i+1}', end= '\r')

            # get the tensor for the current month
            t0 = full_tensor[:, i, :, :, :].to(device) # This is all you need to put on device.
            
            # predict the next month, both the magnitudes and the probabilities and get the updated hidden state (which both cell and hidden state concatenated)
            t1_pred, t1_pred_class, h_tt = model(t0, h_tt)


        else: # take the last t1_pred. This is the out-of-sample part.
            print(f'\t\t\t Out of sample. month: {i+1}', end= '\r')
            t0 = t1_pred.detach()

            # Execute  whatever freeze option you have set in the config out of sample
            t1_pred, t1_pred_class, h_tt = execute_freeze_h_option(config, model, t0, h_tt)

            # Only save the out-of-sample predictions
            t1_pred_class = torch.sigmoid(t1_pred_class) # there is no sigmoid in the model (the loss takes logits) so you need to do it here.
            pred_np_list.append(t1_pred.cpu().detach().numpy().squeeze()) # squeeze to remove the batch dim. So this is a list of 3x180x180 arrays
            pred_class_np_list.append(t1_pred_class.cpu().detach().numpy().squeeze()) # squeeze to remove the batch dim. So this is a list of 3x180x180 arrays

    # return the lists of predictions
    return pred_np_list, pred_class_np_list


def sample_posterior(model, views_vol, config, device): 

    """
    Samples from the posterior distribution of Hydranet.

    Args:
    - model: HydraNet
    - views_vol (torch.Tensor): Input views data.
    - config: Configuration file
    - device: Device for computations.

    Returns:
    - tuple: (posterior_magnitudes, posterior_probabilities, out_of_sample_data)
    """

    print(f'Drawing {config.test_samples} posterior samples...', end = '\r')

    # REALLY BAD NAME!!!!
    # Why do you put this test tensor on device here??!? 
    full_tensor = get_full_tensor(views_vol, config, device) # better cal this evel tensor
    out_of_sample_vol = full_tensor[:,-config.time_steps:,:,:,:].cpu().numpy() # From the test tensor get the out-of-sample time_steps. 

    posterior_list = []
    posterior_list_class = []

    for i in range(config.test_samples): # number of posterior samples to draw - just set config.test_samples, no? 

        # full_tensor is need on device here, but maybe just do it inside the test function? 
        pred_np_list, pred_class_np_list = predict(model, full_tensor, config, device) # Returns two lists of numpy arrays (shape 3/180/180). One list of the predicted magnitudes and one list of the predicted probabilities.
        posterior_list.append(pred_np_list)
        posterior_list_class.append(pred_class_np_list)

        #if i % 10 == 0: # print steps 10
        print(f'Posterior sample: {i}/{config.test_samples}', end = '\r')

    return posterior_list, posterior_list_class, out_of_sample_vol, full_tensor

