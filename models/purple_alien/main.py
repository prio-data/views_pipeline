import numpy as np
import pickle
import time
import os
import functools

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

from utils import choose_model, choose_loss, choose_sheduler, get_train_tensors, get_test_tensor, apply_dropout, execute_freeze_h_option, get_log_dict, train_log, init_weights, get_data
#from config_sweep import get_swep_config
from config_hyperparameters import get_hp_config
from train_model import make, training_loop


print('Imports done...')


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

    # model type is still a vary bad name here - it should be something like run_type... Change later!
    # Also, can you even choose testing and forecasting here?
    run_type_dict = {'a' : 'calibration', 'b' : 'testing', 'c' : 'forecasting'}
    run_type = run_type_dict[input("a) Calibration\nb) Testing\nc) Forecasting\n")]
    print(f'Run type: {run_type}\n')

    project = f"imp_new_structure_{run_type}" # temp. also a bad name. Change later!

    hyperparameters = get_hp_config()

    hyperparameters['run_type'] = run_type # bad name... ! Change later!
    hyperparameters['sweep'] = False

    start_t = time.time()

    model = model_pipeline(config = hyperparameters, project = project)

    PATH_ARTIFACTS = setup_artifacts_paths(PATH)

    # create the artifacts folder if it does not exist
    os.makedirs(PATH_ARTIFACTS, exist_ok=True)

    # save the model
    PATH_MODEL_ARTIFACT = os.path.join(PATH_ARTIFACTS, f"{run_type}_model.pt")
    torch.save(model, PATH_MODEL_ARTIFACT)

    print(f"Model saved as: {PATH_MODEL_ARTIFACT}")
    
    end_t = time.time()
    minutes = (end_t - start_t)/60
    print(f'Done. Runtime: {minutes:.3f} minutes')




