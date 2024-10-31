from utils import utils_script_gen
from pathlib import Path


def generate(script_dir: Path) -> bool:
    """
    Generates a script that sets up the project paths, parses command-line arguments,
    sets up logging, and executes a single model run.

    Parameters:
        script_dir (Path):
            The directory where the generated script will be saved.
            This should be a valid writable path.

    Returns:
        bool:
            True if the script was written and compiled successfully, False otherwise.
    """
    code = """import wandb
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
from execute_model_runs import execute_single_run

warnings.filterwarnings("ignore")
try:
    from common_utils.ensemble_path import EnsemblePath
    from common_utils.global_cache import GlobalCache
    model_name = EnsemblePath.get_model_name_from_path(PATH)
    GlobalCache["current_model"] = model_name
except ImportError as e:
    warnings.warn(f"ImportError: {e}. Some functionalities (model separated log files) may not work properly.", ImportWarning)
except Exception as e:
    warnings.warn(f"An unexpected error occurred: {e}.", RuntimeWarning)
logger = setup_logging("run.log")


if __name__ == "__main__":
    wandb.login()

    args = parse_args()
    validate_arguments(args)

    execute_single_run(args)
"""
    return utils_script_gen.save_script(script_dir, code)