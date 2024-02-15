from pathlib import Path
# from prefect import Flow, task
import subprocess

root_dir = Path(__file__).parent/ "models"

main_py_files = list(root_dir.rglob('main.py'))
print(main_py_files)

# Define paths to main.py files for each model
MODEL_MAIN_FILES = [
    "models/orange_pasta/main.py",
    "models/yellow_pikachu/main.py",
    # Add paths for additional main.py files as needed
]

# Prefect task to execute a main.py file
@task
def execute_main(main_file):
    subprocess.run(["python", main_file])

# Define Prefect Flow
with Flow("Model_Execution_Flow") as flow:
    # Create Prefect tasks for executing main.py files
    tasks = [execute_main(main_file) for main_file in MODEL_MAIN_FILES]

# Execute Prefect workflow
flow.run()