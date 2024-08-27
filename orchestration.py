from pathlib import Path
from prefect import flow, task
import subprocess
from common_utils.utils_cli_parser import parse_args, validate_arguments

MODEL_DIR = Path(__file__).parent / "models"
ENSEMBLE_DIR = Path(__file__).parent / "ensembles"


def initialize():
    # Define paths to main.py files for each model and ensemble
    model_main_files = list(MODEL_DIR.rglob('main.py')) 
    ensemble_main_files = list(ENSEMBLE_DIR.rglob('main.py'))

    return model_main_files, ensemble_main_files


@task(task_run_name="{name}")
def run_model_script(script_path, name, run_type, sweep, train, evaluate, forecast):
    cli_args = []
    cli_args.append("--run_type")
    cli_args.append(run_type)

    if sweep:
        cli_args.append("--sweep")
    if train:
        cli_args.append("--train")
    if evaluate:
        cli_args.append("--evaluate")
    if forecast:
        cli_args.append("--forecast")

    command = ["python", script_path] + cli_args
    # print(command)
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Script {script_path} failed: {result.stderr}")
    print(result.stdout)


@task(task_run_name="{name}")
def run_ensemble_script(script_path, name, run_type, evaluate, forecast, aggregation):
    cli_args = []
    cli_args.extend(["--run_type", run_type])
    cli_args.extend(["--aggregation", aggregation])
    
    if evaluate:
        cli_args.append("--evaluate")
    if forecast:
        cli_args.append("--forecast")

    command = ["python", script_path] + cli_args
    # print(command)
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Script {script_path} failed: {result.stderr}")
    # print(result.stdout)


@flow(log_prints=True)
def model_execution_flow(run_type, sweep, train, evaluate, forecast, aggregation):
    model_main_files, ensemble_main_files = initialize()
    if not aggregation:
        for main_file in model_main_files:
            run_model_script(main_file, main_file.parent.name, run_type, sweep, train, evaluate, forecast)
    else:
        for ensemble_file in ensemble_main_files:
            run_ensemble_script(ensemble_file, ensemble_file.parent.name, run_type, evaluate, forecast, aggregation)


if __name__ == "__main__":
    args = parse_args()
    validate_arguments(args)

    model_execution_flow(run_type=args.run_type, 
               sweep=args.sweep, 
               train=args.train, 
               evaluate=args.evaluate, 
               forecast=args.forecast,
               aggregation=args.aggregation)

