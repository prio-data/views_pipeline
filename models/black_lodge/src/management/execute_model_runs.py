import wandb

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_artifacts_paths
setup_project_paths(PATH)

from config_sweep import get_sweep_config
from config_hyperparameters import get_hp_config
from execute_model_tasks import execute_model_tasks


def execute_sweep_run(args):
    """
    Function to execute a hyperparameter sweep of the model. This function is called when the user specifies a sweep in the command line.

    Args:
    - args (argparse.Namespace): Arguments parsed from the command line.

    Returns:
    - None

    Example:
    ```
    python main.py --sweep

    ```
    """
    print('Running sweep...')

    sweep_config = get_sweep_config()
    project = sweep_config['name']
    sweep_config['parameters']['run_type'] = {'value' : "calibration"} 
    sweep_config['parameters']['sweep'] = {'value' : True}

    sweep_id = wandb.sweep(sweep_config, project=project, entity='views_pipeline') # entity is the team name

    wandb.agent(sweep_id, execute_model_tasks, entity='views_pipeline') # entity is the team name - Seem like it needs to be botb in sweep_id and agent


def execute_single_run(args):
    """
    Function to execute a single run of the model. This function is called when the user specifies a single run in the command line.

    Args:
    - args (argparse.Namespace): Arguments parsed from the command line.

    Returns:
    - None

    Examples:
    ```
    python main.py --run_type calibration --train --evaluate --artifact_name my_model

    python main.py --run_type forecasting --artifact_name my_model

    python main.py --run_type testing --train --evaluate --artifact_name my_model
    ```
    
    """
    
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