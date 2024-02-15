from pathlib import Path
from prefect import flow, task
import subprocess

root_dir = Path(__file__).parent/ "models"


# Define paths to main.py files for each model
MODEL_MAIN_FILES = list(root_dir.rglob('main.py'))

# Prefect task to execute a main.py file
@task
def execute_main(main_file):
    subprocess.run(["python", str(main_file)])

# Define Prefect Flow
@flow(log_prints=True)
def model_execution_flow():
    MODEL_MAIN_FILES = list(root_dir.rglob('main.py'))
    tasks = [execute_main(main_file) for main_file in MODEL_MAIN_FILES]

# Execute Prefect workflow
model_execution_flow()