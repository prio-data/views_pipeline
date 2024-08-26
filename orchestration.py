from pathlib import Path
from prefect import flow, task
import subprocess

def initialize():
    # Define paths to main.py files for each model
    MODEL_DIR = Path(__file__).parent / "models"
    MODEL_MAIN_FILES = list(MODEL_DIR.rglob('main.py')) 

    return MODEL_MAIN_FILES


@task(task_run_name="{name}")
def execute_main(main_file, name):
    # Prefect task to execute a main.py file
    subprocess.run(["python", str(main_file)])

@flow(log_prints=True)
def model_execution_flow():
    # Define Prefect Flow
    MODEL_MAIN_FILES = initialize()
    tasks = [execute_main(main_file, main_file.parent.name) for main_file in MODEL_MAIN_FILES] # Execute each model in parallel

# Execute Prefect workflow
model_execution_flow()

if __name__ == "__main__":
    model_execution_flow.run()