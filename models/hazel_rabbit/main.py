import time

import wandb

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_artifacts_paths
setup_project_paths(PATH)

from cli_parser_utils import parse_args, validate_arguments
#from artifacts_utils import get_latest_model_artifact

#from model_run_handlers import handle_sweep_run, handle_single_run
from execute_model_runs import execute_sweep_run, execute_single_run

#from mode_run_manager import model_run_manager

if __name__ == "__main__":

    # new argpars solution.
    args = parse_args()
    #print(args)

    # Validate the parsed arguments to ensure they conform to the required logic and combinations.
    validate_arguments(args)

    # wandb login
    wandb.login()

    start_t = time.time()

    # Test if and why a model_metadata_dict.py was saved in the artifacts folder..

    # first you need to check if you are running a sweep or not, because the sweep will overwrite the train and evaluate flags
    if args.sweep == True:

        #handle_sweep_run(args)
        execute_sweep_run(args)

    elif args.sweep == False:
        
        #handle_single_run(args)
        execute_single_run(args)

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


