import time
import wandb
import sys
import logging
from pathlib import Path
PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths
setup_project_paths(PATH)

from utils_cli_parser import parse_args, validate_arguments
from execute_model_runs import execute_sweep_run, execute_single_run

logging.basicConfig(filename='run.log', encoding='utf-8', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    args = parse_args()
    validate_arguments(args)

    # wandb login
    wandb.login()

    start_t = time.time()

    if args.sweep:
        execute_sweep_run(args)
    else:
        execute_single_run(args)

    end_t = time.time()
    minutes = (end_t - start_t) / 60
    logger.info(f'Done. Runtime: {minutes:.3f} minutes.\n')
