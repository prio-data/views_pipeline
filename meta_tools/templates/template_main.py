from utils import utils_script_gen
from pathlib import Path


def generate(script_dir: Path) -> bool:
    """
    Generates a Python script that sets up and executes model runs with Weights & Biases (WandB) integration.

    This function creates a script that imports necessary modules, sets up project paths, and defines the 
    main execution logic for running either a single model run or a sweep of model configurations. The 
    generated script includes command-line argument parsing, validation, and runtime logging.

    Parameters:
        script_dir (Path): 
            The directory where the generated Python script will be saved. This should be a valid writable 
            path that exists within the project structure.

    Returns:
        bool: 
            True if the script was successfully written to the specified directory, False otherwise.

    The generated script includes the following features:
    - Imports required libraries and sets up the path to include the `common_utils` module.
    - Initializes project paths using the `setup_project_paths` function.
    - Parses command-line arguments with `parse_args`.
    - Validates arguments to ensure correctness with `validate_arguments`.
    - Logs into Weights & Biases using `wandb.login()`.
    - Executes a model run based on the provided command-line flags, either initiating a sweep or a single run.
    - Calculates and prints the runtime of the execution in minutes.

    Note:
        - Ensure that the `common_utils` module and all other imported modules are accessible from the 
          specified script directory.
        - The generated script is designed to be executed as a standalone Python script.
    """
    code = """import time
import wandb
import sys
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
    print(f'Done. Runtime: {minutes:.3f} minutes')
"""
    return utils_script_gen.save_script(script_dir, code)
