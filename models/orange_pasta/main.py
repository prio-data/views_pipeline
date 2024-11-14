import wandb
import sys
import warnings

from pathlib import Path
PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
# from set_path import setup_project_paths
# setup_project_paths(PATH)

from utils_cli_parser import parse_args, validate_arguments
from utils_logger import setup_logging
# from execute_model_runs import execute_sweep_run, execute_single_run

warnings.filterwarnings("ignore")
try:
    from views_pipeline.managers.path_manager import ModelPath
    from views_pipeline.cache.global_cache import GlobalCache
    model_name = ModelPath.get_model_name_from_path(PATH)
    GlobalCache["current_model"] = model_name
except ImportError as e:
    warnings.warn(f"ImportError: {e}. Some functionalities (model seperated log files) may not work properly.", ImportWarning)
except Exception as e:
    warnings.warn(f"An unexpected error occurred: {e}.", RuntimeWarning)
logger = setup_logging("run.log")

from stepshifter_manager import StepshifterManager

if __name__ == "__main__":
    wandb.login()

    args = parse_args()
    validate_arguments(args)

    if args.sweep:
        StepshifterManager(model_path=ModelPath(PATH)).execute_sweep_run(args)
        # execute_sweep_run(args)
    else:
        StepshifterManager(model_path=ModelPath(PATH)).execute_single_run(args)
