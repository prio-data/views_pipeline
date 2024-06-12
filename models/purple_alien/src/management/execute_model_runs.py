import wandb

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_artifacts_paths
setup_project_paths(PATH)

from config_sweep import get_swep_config
from config_hyperparameters import get_hp_config
#from model_run_manager import model_run_manager
from execute_model_tasks import execute_model_tasks


def execute_sweep_run(args):
    print('Running sweep...')

    project = f"purple_alien_sweep" # check naming convention
    sweep_config = get_swep_config()
    sweep_config['parameters']['run_type'] = {'value' : "calibration"} # I see no reason to run the other types in the sweep
    sweep_config['parameters']['sweep'] = {'value' : True}

    sweep_id = wandb.sweep(sweep_config, project=project, entity='views_pipeline') # entity is the team name

    wandb.agent(sweep_id, execute_model_tasks, entity='views_pipeline') # entity is the team name - Seem like it needs to be botb in sweep_id and agent


def execute_single_run(args):
    
    # get hyperparameters. IS THE ISSUE UP HERE?
    hyperparameters = get_hp_config()
    hyperparameters['run_type'] = args.run_type
    hyperparameters['sweep'] = False

    # get run type and denoting project name - check convention!
    project = f"purple_alien_{args.run_type}"

    if args.run_type == 'calibration' or args.run_type == 'testing':

        #model_run_manager(config = hyperparameters, project = project, train = args.train, eval = args.evaluate, forecast = False, artifact_name = args.artifact_name)        
        execute_model_tasks(config = hyperparameters, project = project, train = args.train, eval = args.evaluate, forecast = False, artifact_name = args.artifact_name)

    elif args.run_type == 'forecasting':

        #print('True forecasting ->->->->')
        #model_run_manager(config = hyperparameters, project = project, train = False, eval = False, forecast=True, artifact_name = args.artifact_name)     
        execute_model_tasks(config = hyperparameters, project = project, train = False, eval = False, forecast=True, artifact_name = args.artifact_name)

    else:
        raise ValueError(f"Invalid run type: {args.run_type}")

