from pathlib import Path
from prefect import flow, task
import subprocess

model_dir = Path(__file__).parent/ "models"
ensemble_dir = Path(__file__).parent/ "ensembles"

# Define paths to main.py files for each model
MODEL_MAIN_FILES = list(model_dir.rglob('main.py')) + list(ensemble_dir.rglob('main.py'))

def generate_run_name(main_file):
    return main_file.stem

# Prefect task to execute a main.py file
@task(task_run_name="{name}")
def execute_main(main_file, name):
    subprocess.run(["python", str(main_file)])

# Define Prefect Flow
@flow(log_prints=True)
def model_execution_flow():
    
    tasks = [execute_main(main_file, main_file.parent.name) for main_file in MODEL_MAIN_FILES]

# Execute Prefect workflow
model_execution_flow()