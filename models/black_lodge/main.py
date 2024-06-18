import time

import wandb

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_artifacts_paths
setup_project_paths(PATH)

from cli_parser_utils import parse_args, validate_arguments #change once PR30 is merged

from execute_model_runs import execute_sweep_run, execute_single_run

#from mode_run_manager import model_run_manager

if __name__ == "__main__":

    args = parse_args()
    #print(args) #use for debugging

    validate_arguments(args)

    wandb.login()

    start_t = time.time()

    
    if args.sweep == True:
        # need to check if you are running a sweep or not, because the sweep will overwrite the train and evaluate flags
        execute_sweep_run(args)

    elif args.sweep == False:
        execute_single_run(args)


    end_t = time.time()
    minutes = (end_t - start_t)/60
    print(f'Done. Runtime: {minutes:.3f} minutes')