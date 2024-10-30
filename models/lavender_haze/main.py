import wandb
import sys
import warnings

from pathlib import Path
PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths
setup_project_paths(PATH)

from utils_cli_parser import parse_args, validate_arguments
from utils_logger import setup_logging
from execute_model_runs import execute_sweep_run, execute_single_run

warnings.filterwarnings("ignore")
try:
    from common_utils.model_path import ModelPath
    from common_utils.global_cache import GlobalCache
    GlobalCache["current_model"] = ModelPath.get_model_name_from_path(Path(__file__))
except Exception:
    pass
logger = setup_logging("run.log")


if __name__ == "__main__":
    wandb.login()
    
    args = parse_args()
    validate_arguments(args)

    if args.sweep:
        execute_sweep_run(args)
    else:
        execute_single_run(args)
