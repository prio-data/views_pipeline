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
from cli_parser_utils import parse_args, validate_arguments

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
            get_posterior(model, views_vol, config, device) # actually since you give config now you do not need: time_steps, run_type, is_sweep,
            print('Done testing')

        else:
            return(model) 


if __name__ == "__main__":

    # new argpars solution.
    args = parse_args()
    print(args)

    # validate arguments to ensure that only correct combinations of flags are set
    validate_arguments(args)

    # wandb login
    wandb.login()

    start_t = time.time()
    # can you even choose testing and forecasting here?
    #run_type_dict = {'a' : 'calibration', 'b' : 'testing', 'c' : 'forecasting'}
    #run_type = run_type_dict[input("a) Calibration\nb) Testing\nc) Forecasting\n")]
    #print(f'Run type: {run_type}\n')


    # first you need to check if you are running a sweep or not, because the sweep will overwrite the train and evaluate flags
    if args.sweep == True:
        
        print('Running sweep...')

        project = f"purple_alien_sweep" # check naming convention

        sweep_config = get_swep_config()
        sweep_config['parameters']['run_type'] = {'value' : "calibration"} # I see no reason to run the other types in the sweep
        sweep_config['parameters']['sweep'] = {'value' : True}

        sweep_id = wandb.sweep(sweep_config, project=project) # and then you put in the right project name

        wandb.agent(sweep_id, model_pipeline)

 
    elif args.sweep == False:
        print('Running single model operation...')
        run_type = args.run_type
        project = f"purple_alien_{run_type}"
        hyperparameters = get_hp_config()
        hyperparameters['run_type'] = run_type
        hyperparameters['sweep'] = False
        
        if args.train:
            print(f"Training one model for run type: {run_type} and saving it as an artifact...")
            model = model_pipeline(config = hyperparameters, project = project)
            PATH_ARTIFACTS = setup_artifacts_paths(PATH)

            # create the artifacts folder if it does not exist
            os.makedirs(PATH_ARTIFACTS, exist_ok=True)

            # save the model
            PATH_MODEL_ARTIFACT = os.path.join(PATH_ARTIFACTS, f"{run_type}_model.pt")
            torch.save(model, PATH_MODEL_ARTIFACT)

            print(f"Model saved as: {PATH_MODEL_ARTIFACT}")

        if args.evaluate:
            print(f"Evaluating model for run type: {run_type}...")
            print('not implemented yet...') # you need to implement this part.
            
            #model = torch.load(PATH_MODEL_ARTIFACT)
            #model.eval()
            #get_posterior(model, views_vol, config, device)
    
    end_t = time.time()
    minutes = (end_t - start_t)/60
    print(f'Done. Runtime: {minutes:.3f} minutes')




