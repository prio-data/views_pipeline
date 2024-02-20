import numpy as np
import pickle
import time
import sys
import os
import functools

import torch
import torch.nn as nn
import torch.nn.functional as F

import wandb

# Set the base path relative to the current script location
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(f'working int {base_path}')

# Add the required directories to the system path
sys.path.insert(0, os.path.join(base_path, "architectures"))
sys.path.insert(0, os.path.join(base_path, "configs"))
sys.path.insert(0, os.path.join(base_path, "utils"))  


from utils import choose_model, choose_loss, choose_sheduler, get_train_tensors, get_test_tensor, apply_dropout, execute_freeze_h_option, get_log_dict, train_log, init_weights, get_data
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


def model_pipeline(config = None, project = None):

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)

    # tell wandb to get started
    with wandb.init(project=project, entity="nornir", config=config): # project and config ignored when runnig a sweep

        wandb.define_metric("monthly/out_sample_month")
        wandb.define_metric("monthly/*", step_metric="monthly/out_sample_month")

        # access all HPs through wandb.config, so logging matches execution!
        config = wandb.config

        views_vol = get_data(config)

        # make the model, data, and optimization problem
        model, criterion, optimizer, scheduler = make(config, device)

        training_loop(config, model, criterion, optimizer, scheduler, views_vol, device)
        print('Done training')

        return(model)


if __name__ == "__main__":

    wandb.login()

    model_type_dict = {'a' : 'calibration', 'b' : 'testing', 'c' : 'forecasting'}
    model_type = model_type_dict[input("a) Calibration\nb) Testing\nc) Forecasting\n")]
    print(f'Run type: {model_type}\n')

    project = f"imp_new_structure_{model_type}" # temp.

    hyperparameters = get_hp_config()

    hyperparameters['model_type'] = model_type
    hyperparameters['sweep'] = False

    start_t = time.time()

    model = model_pipeline(config = hyperparameters, project = project)

    # save the model - should prolly use the state_dict instead of the model object... 
    
    # for computerome
    # artifacts_path = f"/home/projects/ku_00017/people/simpol/scripts/conflictNet/artifacts"
    
    # for fimbulthul
#    artifacts_path = f"/home/simmaa/HydraNet_001/artifacts"

    #artifacts_path = f"{hyperparameters['path_repo']}/artifacts"
    artifacts_path = base_path.replace('src', 'artifacts')

    os.makedirs(artifacts_path, exist_ok=True)

    model = torch.save(model, f"{artifacts_path}/{model_type}_model.pt")
    print("Model saved as: ", f"{artifacts_path}/{model_type}_model.pt")

    end_t = time.time()
    minutes = (end_t - start_t)/60
    print(f'Done. Runtime: {minutes:.3f} minutes')
