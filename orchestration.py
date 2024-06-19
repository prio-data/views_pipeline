from pathlib import Path
import sys

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_model_paths
setup_project_paths(PATH)
#setup_model_paths(PATH)
#model_dir = PATH_MODEL
model_dir = Path(__file__).parent/ "models" # TBD: add PATH_MODEL to seth_path.py
ensemble_dir = Path(__file__).parent/ "ensembles" # TBD: add PATH_ENSEMBLE to seth_path.py

from config_monthly import get_monthly_config

from prefect import flow, task
import subprocess


def initialize():
    #Define run id from common_configs/config_monthly.py
    monthly_config = get_monthly_config()
    run_id = monthly_config["run_id"]

    # Define paths to main.py files for each model
    MODEL_MAIN_FILES = list(model_dir.rglob('main.py')) + list(ensemble_dir.rglob('main.py'))

    return run_id, MODEL_MAIN_FILES


@task(task_run_name="{name}")
def execute_main(main_file, name):
    # Prefect task to execute a main.py file
    subprocess.run(["python", str(main_file)])

@flow(log_prints=True)
def model_execution_flow():
    # Define Prefect Flow
    #run_id, MODEL_MAIN_FILES = initialize()
    tasks = [execute_main(main_file, main_file.parent.name) for main_file in MODEL_MAIN_FILES] # Execute each model in parallel

# Execute Prefect workflow
model_execution_flow()

if __name__ == "__main__":
    model_execution_flow.run()
