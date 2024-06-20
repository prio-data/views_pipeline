import numpy as np
import pickle
import time
import os
import functools
from datetime import datetime
import torch
import torch.nn as nn
import torch.nn.functional as F

import wandb

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_artifacts_paths
setup_project_paths(PATH)

from utils import choose_model, choose_loss, choose_sheduler, get_train_tensors, get_full_tensor, apply_dropout, execute_freeze_h_option, train_log, init_weights, get_data
#from config_sweep import get_swep_config
from config_hyperparameters import get_hp_config

print('Imports done...')

def make(config, device):

    model = choose_model(config, device)

    # Create a partial function with the initialization function and the config parameter
    init_fn = functools.partial(init_weights, config=config)

    # Apply the initialization function to the modelrawi
    model.apply(init_fn)

    # choose loss function
    criterion = choose_loss(config, device) # this is a touple of the reg and the class criteria

    # choose sheduler - the optimizer is always AdamW right now
    optimizer, scheduler = choose_sheduler(config, model)

    return(model, criterion, optimizer, scheduler) #, dataloaders, dataset_sizes)


def train(model, optimizer, scheduler, criterion_reg, criterion_class, multitaskloss_instance, views_vol, sample, config, device): # views vol and sample

    wandb.watch(model, [criterion_reg, criterion_class], log= None, log_freq=2048)

    avg_loss_reg_list = []
    avg_loss_class_list = []
    avg_loss_list = []
    total_loss = 0

    model.train()  # train mode
    multitaskloss_instance.train() # meybe another place...


    # Batch loops:
    for batch in range(config.batch_size):

        # Getting the train_tensor
        train_tensor = get_train_tensors(views_vol, sample, config, device)
        seq_len = train_tensor.shape[1]
        window_dim = train_tensor.shape[-1] # the last dim should always be a spatial dim (H or W)

        # initialize a hidden state
        h = model.init_h(hidden_channels = model.base, dim = window_dim).float().to(device)

        # Sequens loop rnn style
        for i in range(seq_len-1): # so your sequnce is the full time len - last month.
            print(f'\t\t month: {i+1}/{seq_len}...', end='\r')

            t0 = train_tensor[:, i, :, :, :]

            t1 = train_tensor[:, i+1, :, :, :]
            t1_binary = (t1.clone().detach().requires_grad_(True) > 0) * 1.0 # 1.0 to ensure float. Should avoid cloning warning now.

            # forward-pass
            t1_pred, t1_pred_class, h = model(t0, h.detach())
        
            losses_list = []

            for j in range(t1_pred.shape[1]): # first each reggression loss. Should be 1 channel, as I conccat the reg heads on dim = 1

                losses_list.append(criterion_reg(t1_pred[:,j,:,:], t1[:,j,:,:])) # index 0 is batch dim, 1 is channel dim (here pred), 2 is H dim, 3 is W dim

            for j in range(t1_pred_class.shape[1]): # then each classification loss. Should be 1 channel, as I conccat the class heads on dim = 1

                losses_list.append(criterion_class(t1_pred_class[:,j,:,:], t1_binary[:,j,:,:])) # index 0 is batch dim, 1 is channel dim (here pred), 2 is H dim, 3 is W dim

            losses = torch.stack(losses_list)
            loss = multitaskloss_instance(losses)

            total_loss += loss

            # traning output
            loss_reg = losses[:t1_pred.shape[1]].sum() # sum the reg losses
            loss_class = losses[-t1_pred.shape[1]:].sum() # assuming 

            avg_loss_reg_list.append(loss_reg.detach().cpu().numpy().item())
            avg_loss_class_list.append(loss_class.detach().cpu().numpy().item())
            avg_loss_list.append(loss.detach().cpu().numpy().item())


    # log each sequence/timeline/batch
    train_log(avg_loss_list, avg_loss_reg_list, avg_loss_class_list) # FIX!!!

    # Backpropagation and optimization - after a full sequence... 
    optimizer.zero_grad()
    total_loss.backward()

    # Gradient Clipping
    if config.clip_grad_norm == True:
        clip_value = 1.0
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=clip_value)

    else:
        pass

    # optimize
    optimizer.step()

    # Adjust learning rate based on the loss
    scheduler.step()


def training_loop(config, model, criterion, optimizer, scheduler, views_vol, device):

    # # add spatail transformer

    criterion_reg, criterion_class, multitaskloss_instance = criterion

    np.random.seed(config.np_seed)
    torch.manual_seed(config.torch_seed)
    print(f'Training initiated...')

    for sample in range(config.samples):

        print(f'Sample: {sample+1}/{config.samples}', end = '\r')

        train(model, optimizer, scheduler , criterion_reg, criterion_class, multitaskloss_instance, views_vol, sample, config, device)

    print('training done...')

def train_model_artifact(config, device, views_vol, PATH_ARTIFACTS):
#def handle_training(config, device, views_vol, PATH_ARTIFACTS):
    
    """
    Creates, trains, and saves a model artifact.

    This function creates the model, criterion, optimizer, and scheduler. It then trains the model
    using the provided training loop and saves the trained model with a timestamp and run type as an artifact
    in the specified artifacts path.

    Args:
        config: Configuration object containing parameters and settings.
        device: The device (torch.device) to run the model on (CPU or GPU).
        views_vol: The tensor containing the input data for training.
        PATH_ARTIFACTS: The path where model artifacts are stored.
    """

    # Create the model, criterion, optimizer and scheduler
    model, criterion, optimizer, scheduler = make(config, device)
    
    # Train the model
    training_loop(config, model, criterion, optimizer, scheduler, views_vol, device)
    print('Done training')

    # just in case the artifacts folder does not exist
    os.makedirs(PATH_ARTIFACTS, exist_ok=True)

    # Define the path for the artifacts with a timestamp and a run type
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f"{config.run_type}_model_{timestamp}.pt"
    PATH_MODEL_ARTIFACT = os.path.join(PATH_ARTIFACTS, model_filename)
    
    # save the model
    torch.save(model, PATH_MODEL_ARTIFACT)
    
    # done
    print(f"Model saved as: {PATH_MODEL_ARTIFACT}")

