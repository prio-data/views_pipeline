import time
import wandb
import sys
import logging
logging.basicConfig(filename='run.log', encoding='utf-8', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
from pathlib import Path
# Set up the path to include common_utils module
PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
# Import necessary functions for project setup and model execution
from set_path import setup_project_paths
setup_project_paths(PATH)
from utils_cli_parser import parse_args, validate_arguments
from execute_model_runs import execute_sweep_run, execute_single_run

if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()
    
    # Validate the arguments to ensure they are correct
    validate_arguments(args)
    # Log in to Weights & Biases (wandb)
    wandb.login()
    # Record the start time
    start_t = time.time()
    # Execute the model run based on the sweep flag
    if args.sweep:
        execute_sweep_run(args)  # Execute sweep run
    else:
        execute_single_run(args)  # Execute single run
    # Record the end time
    end_t = time.time()
    
    # Calculate and print the runtime in minutes
    minutes = (end_t - start_t) / 60
    logger.info(f'Done. Runtime: {minutes:.3f} minutes')
