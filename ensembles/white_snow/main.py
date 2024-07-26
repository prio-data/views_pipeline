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


def parse_arguments():
    parser = argparse.ArgumentParser(description='Model run settings')

    parser.add_argument('-r', '--run_type',
                        choices=['calibration', 'testing', 'forecasting'],
                        type=str,
                        default='calibration',
                        help='Choose the run type for the model: calibration, testing, or forecasting. Default is calibration.')


    parser.add_argument('-a', '--aggregation',
                        # To do: considering weighted average
                        choices=['mean', 'median'],
                        default='mean',
                        help='Method to aggregate the model outputs to produce an ensemble. '
                             'Options are: mean or median. Default is mean.')

    args = parser.parse_args()

    if args.run_type in ['calibration', 'testing']:
        args.evaluate = True
        args.forecast = False
    elif args.run_type == 'forecasting':
        args.evaluate = False
        args.forecast = True

    return args


if __name__ == "__main__":
    args = parse_arguments()

    # wandb login
    wandb.login()

    start_t = time.time()

    execute_single_run(args)

    end_t = time.time()
    minutes = (end_t - start_t) / 60
    print(f'Done. Runtime: {minutes:.3f} minutes')

