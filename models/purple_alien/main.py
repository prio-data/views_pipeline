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
from config_sweep import get_swep_config
from config_hyperparameters import get_hp_config
from train_model import make, training_loop
from evaluate_sweep import get_posterior # see if it can be more genrel to a single model as well... 

print('Imports done...')


def model_pipeline(config = None, project = None):

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)

    # tell wandb to get started
    with wandb.init(project=project, entity="views_pipeline", config=config): # project and config ignored when runnig a sweep

        # for the monthly metrics
        wandb.define_metric("monthly/out_sample_month")
        wandb.define_metric("monthly/*", step_metric="monthly/out_sample_month")

        # access all HPs through wandb.config, so logging matches execution!
        config = wandb.config

        views_vol = get_data(config)

        # make the model, data, and optimization problem
        model, criterion, optimizer, scheduler = make(config, device)

        training_loop(config, model, criterion, optimizer, scheduler, views_vol, device)
        print('Done training')

        if config.sweep:
            get_posterior(unet, views_vol, config, device) # actually since you give config now you do not need: time_steps, run_type, is_sweep,
            print('Done testing')

        else:
            return(model) 

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Run model pipeline with specified run type.')

    parser.add_argument('--run_type',
                        choices=['calibration', 'testing', 'forecasting'],
                        type=str,
                        default='calibration',
                        help='Choose the run type for the model: calibration, testing, or forecasting. Default is calibration.')

    parser.add_argument('--sweep',
                        choices=[True, False],
                        type=bool,
                        default=False,
                        help='Choose whether to run the model pipeline as part of a sweep. Default is False.')

    return parser.parse_args()


if __name__ == "__main__":

    wandb.login()

    # can you even choose testing and forecasting here?
    #run_type_dict = {'a' : 'calibration', 'b' : 'testing', 'c' : 'forecasting'}
    #run_type = run_type_dict[input("a) Calibration\nb) Testing\nc) Forecasting\n")]
    #print(f'Run type: {run_type}\n')

    # new argpars solution.
    args = parse_args()

    if args.sweep:
        
        print('Running sweep...')

        project = f"purple_alien_sweep" # check naming convention

        sweep_config = get_swep_config()
        sweep_config['parameters']['run_type'] = {'value' : "calibration"} # I see no reason to run the other types in the sweep
        sweep_config['parameters']['sweep'] = {'value' : True}

        sweep_id = wandb.sweep(sweep_config, project=project) # and then you put in the right project name

        start_t = time.time()
        wandb.agent(sweep_id, model_pipeline)
            
    else:

        print('Train one model and save it as an artifact...')

        # Extract run_type from parsed arguments
        run_type = args.run_type
        print(f'Run type: {run_type}\n')


        project = f"purple_alien_{run_type}" # check naming convention

        hyperparameters = get_hp_config()

        hyperparameters['run_type'] = run_type 
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




