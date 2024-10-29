from pathlib import Path
from prefect import flow, task
from prefect_shell import ShellOperation 
import subprocess
import sys

PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from utils_cli_parser import parse_args, validate_arguments
from model_path import ModelPath
from ensemble_path import EnsemblePath
# from utils_logger import setup_logging

MODEL_DIR = ModelPath.get_models()
ENSEMBLE_DIR = EnsemblePath.get_models()


def initialize():
    # Define paths to main.py files for each model and ensemble
    model_main_files = list(MODEL_DIR.rglob('main.py')) 
    ensemble_main_files = list(ENSEMBLE_DIR.rglob('main.py'))

    return model_main_files, ensemble_main_files


@task(task_run_name="{name}")
def run_model_script(script_path, name, run_type, sweep, train, evaluate, forecast, saved, override_month):
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
    if saved:
        cli_args.append("--saved")
    if override_month:
        cli_args.extend(["--override_month", int(override_month)])

    # command = ["python", script_path] + cli_args
    # # print(command)
    # result = subprocess.run(command, capture_output=True, text=True)
    # if result.returncode != 0:
    #     raise Exception(f"Script {script_path} failed: {result.stderr}")

    command = f"python {script_path} " + ' '.join(cli_args)
    ShellOperation(commands=[command]).run()


@task(task_run_name="{name}")
def run_ensemble_script(script_path, name, run_type, train, evaluate, forecast):
    cli_args = []
    cli_args.extend(["--run_type", run_type])
    cli_args.append("--ensemble")
    
    if train:
        cli_args.append("--train")
    if evaluate:
        cli_args.append("--evaluate")
    if forecast:
        cli_args.append("--forecast")

    # command = ["python", script_path] + cli_args
    # # print(command)
    # result = subprocess.run(command, capture_output=True, text=True)
    # if result.returncode != 0:
    #     raise Exception(f"Script {script_path} failed: {result.stderr}")

    command = f"python {script_path} " + ' '.join(cli_args)
    ShellOperation(commands=[command]).run()


@flow(log_prints=True)
def model_execution_flow(run_type, sweep, train, evaluate, forecast, ensemble, saved, override_month):
    model_main_files, ensemble_main_files = initialize()
    if not ensemble:
        for main_file in model_main_files:
            # These two models don't fit the current orchestration
            if main_file.parent.name in ['abundant_abyss', 'purple_alien']:
                continue
            run_model_script(main_file, main_file.parent.name,
                             run_type, sweep, train, evaluate, forecast,
                             saved, override_month)
    else:
        for ensemble_file in ensemble_main_files:
            run_ensemble_script(ensemble_file, ensemble_file.parent.name, run_type, train, evaluate, forecast)


if __name__ == "__main__":
    args = parse_args()
    validate_arguments(args)

    model_execution_flow(run_type=args.run_type,
                         sweep=args.sweep,
                         train=args.train,
                         evaluate=args.evaluate,
                         forecast=args.forecast,
                         ensemble=args.ensemble,
                         saved=args.saved,
                         override_month=args.override_month)
