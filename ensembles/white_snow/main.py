import sys
import time
import argparse
import wandb
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths
setup_project_paths(PATH)

from execute_model_runs import execute_single_run
from utils_cli_parser import parse_args, validate_arguments


if __name__ == "__main__":
    args = parse_args()
    validate_arguments(args)

    # if args.run_type in ['calibration', 'testing']:
    #     args.evaluate = True
    #     args.forecast = False
    # elif args.run_type == 'forecasting':
    #     args.evaluate = False
    #     args.forecast = True

    # wandb login
    wandb.login()

    start_t = time.time()

    execute_single_run(args)

    end_t = time.time()
    minutes = (end_t - start_t) / 60
    print(f'Done. Runtime: {minutes:.3f} minutes')