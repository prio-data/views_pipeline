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

from utils import choose_model, choose_loss, choose_sheduler, get_train_tensors, get_full_tensor, apply_dropout, execute_freeze_h_option, get_log_dict, train_log, init_weights, get_data
from utils_wandb import add_wandb_monthly_metrics
from utils_device import setup_device
from config_sweep import get_swep_config
from config_hyperparameters import get_hp_config
from train_model import make, training_loop, handle_training
# from evaluate_sweep import evaluate_posterior # see if it can be more genrel to a single model as well... 
from evaluate_model import evaluate_posterior
from cli_parser_utils import parse_args, validate_arguments
from artifacts_utils import get_latest_model_artifact


#def setup_device(): 
#    # set the device
#    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#    print(f"Using device: {device}")
#
#def add_wandb_monthly_metrics():
#        
#    # Define "new" monthly metrics for WandB logging
#    wandb.define_metric("monthly/out_sample_month")
#    wandb.define_metric("monthly/*", step_metric="monthly/out_sample_month")
                

def handle_sweep_run(args):
    print('Running sweep...')

    project = f"purple_alien_sweep" # check naming convention
    sweep_config = get_swep_config()
    sweep_config['parameters']['run_type'] = {'value' : "calibration"} # I see no reason to run the other types in the sweep
    sweep_config['parameters']['sweep'] = {'value' : True}

    sweep_id = wandb.sweep(sweep_config, project=project) # and then you put in the right project name

    wandb.agent(sweep_id, model_pipeline)


def handle_single_run(args):
    
    # get hyperparameters. IS THE ISSUE UP HERE?
    hyperparameters = get_hp_config()
    hyperparameters['run_type'] = args.run_type
    hyperparameters['sweep'] = False

    # get run type and denoting project name - check convention!
    project = f"purple_alien_{args.run_type}"

    if args.run_type == 'calibration' or args.run_type == 'testing':

        model_pipeline(config = hyperparameters, project = project, train = args.train, eval = args.evaluate, forecast = False, artifact_name = args.artifact_name)        

    elif args.run_type == 'forecasting':

        #print('True forecasting ->->->->')
        model_pipeline(config = hyperparameters, project = project, train = False, eval = False, forecast=True, artifact_name = args.artifact_name)     

    else:
        raise ValueError(f"Invalid run type: {args.run_type}")


#def handle_training(config, device, views_vol, PATH_ARTIFACTS):
#    
#    # Create the model, criterion, optimizer and scheduler
#    model, criterion, optimizer, scheduler = make(config, device)
#    
#    # Train the model
#    training_loop(config, model, criterion, optimizer, scheduler, views_vol, device)
#    print('Done training')
#
#    # just in case the artifacts folder does not exist
#    os.makedirs(PATH_ARTIFACTS, exist_ok=True)
#
#    # Define the path for the artifacts with a timestamp and a run type
#    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#    model_filename = f"{config.run_type}_model_{timestamp}.pt"
#    PATH_MODEL_ARTIFACT = os.path.join(PATH_ARTIFACTS, model_filename)
#    
#    # save the model
#    torch.save(model, PATH_MODEL_ARTIFACT)
#    
#    # done
#    print(f"Model saved as: {PATH_MODEL_ARTIFACT}")
#

#def handle_evaluation(config, device, views_vol, PATH_ARTIFACTS, artifact_name=None):
#
#    # if an artifact name is provided through the CLI, use it. Otherwise, get the latest model artifact based on the run type
#    if artifact_name:
#        print(f"Using (non-default) artifact: {artifact_name}")
#        
#        # If it lacks the file extension, add it
#        if not artifact_name.endswith('.pt'):
#            artifact_name += '.pt'
#        
#        # Define the full (model specific) path for the artifact
#        PATH_MODEL_ARTIFACT = os.path.join(PATH_ARTIFACTS, artifact_name)
#    
#    else:
#        # use the latest model artifact based on the run type
#        print(f"Using latest (default) run type ({config.run_type}) specific artifact")
#        
#        # Get the latest model artifact based on the run type and the (models specific) artifacts path
#        PATH_MODEL_ARTIFACT = get_latest_model_artifact(PATH_ARTIFACTS, config.run_type)
#
#    # Check if the model artifact exists - if not, raise an error
#    if not os.path.exists(PATH_MODEL_ARTIFACT):
#        raise FileNotFoundError(f"Model artifact not found at {PATH_MODEL_ARTIFACT}")
#
#    # load the model
#    model = torch.load(PATH_MODEL_ARTIFACT)
#    
#    # get the exact model date_time stamp for the pkl files made in the evaluate_posterior from evaluation.py
#    model_time_stamp = os.path.basename(PATH_MODEL_ARTIFACT).split('.')[0]
#
#    # print for debugging
#    print(f"model_time_stamp: {model_time_stamp}")
#
#    # add to config for logging and conciseness
#    config.model_time_stamp = model_time_stamp
#
#    # evaluate the model posterior distribution
#    evaluate_posterior(model, views_vol, config, device)
#    
#    # done. 
#    print('Done testing') 
#

# could be better...
#def handle_forecasting(config, device, views_vol, PATH_ARTIFACTS, artifact_name=None):
#
#    raise NotImplementedError('Forecasting not implemented yet')
#


def model_pipeline(config = None, project = None, train = None, eval = None, forecast = None, artifact_name = None):

    # Define the path for the artifacts
    PATH_ARTIFACTS = setup_artifacts_paths(PATH)

    device = setup_device()

    # Initialize WandB
    with wandb.init(project=project, entity="views_pipeline", config=config): # project and config ignored when running a sweep
        
        # add the monthly metrics to WandB
        add_wandb_monthly_metrics() 

        # Update config from WandB initialization above
        config = wandb.config

        # Retrieve data (partition) based on the configuration
        views_vol = get_data(config)

        # Handle the sweep runs
        if config.sweep:  # If we are running a sweep, always train and evaluate

            model, criterion, optimizer, scheduler = make(config, device)
            training_loop(config, model, criterion, optimizer, scheduler, views_vol, device)
            print('Done training')

            evaluate_posterior(model, views_vol, config, device)
            print('Done testing')

        # Handle the single model runs: train and save the model as an artifact
        if train:
            handle_training(config, device, views_vol, PATH_ARTIFACTS)

        # Handle the single model runs: evaluate a trained model (artifact)
        if eval:
            handle_evaluation(config, device, views_vol, PATH_ARTIFACTS, artifact_name)

        if forecast:
            handle_forecasting(config, device, views_vol, PATH_ARTIFACTS, artifact_name)


if __name__ == "__main__":

    # new argpars solution.
    args = parse_args()
    #print(args)

    # Validate the parsed arguments to ensure they conform to the required logic and combinations.
    validate_arguments(args)

    # wandb login
    wandb.login()

    start_t = time.time()

    # first you need to check if you are running a sweep or not, because the sweep will overwrite the train and evaluate flags
    if args.sweep == True:

        handle_sweep_run(args)
 

    elif args.sweep == False:
        
        handle_single_run(args)
    
    end_t = time.time()
    minutes = (end_t - start_t)/60
    print(f'Done. Runtime: {minutes:.3f} minutes')


    # notes on stepshifted models:
    # There will be some thinking here in regards to how we store, denote (naming convention), and retrieve the model artifacts from stepshifted models.
    # It is not a big issue, but it is something to consider os we don't do something headless. 
    # A possible format could be: <run_type>_model_s<step>_<timestamp>.pt example: calibration_model_s00_20210831_123456.pt, calibration_model_s01_20210831_123456.pt, etc.
    # And the rest of the code maded in a way to handle this naming convention without any issues. Could be a simple fix.
    # Alternatively, we could store the model artifacts in a subfolder for each stepshifted model. This would make it easier to handle the artifacts, but it would also make it harder to retrieve the latest artifact for a given run type.
    # Lastly, the solution Xiaolong is working on might allow us the store multiple models (steps) in one artifact, which would make this whole discussion obsolete and be the best solution.


