import sys
from pathlib import Path
PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths
setup_project_paths(PATH)

from config_deployment import get_deployment_config
from config_hyperparameters import get_hp_config
from config_meta import get_meta_config
from execute_model_tasks import execute_model_tasks
from utils_run import update_config
from utils_checks import ensemble_model_check


def execute_single_run(args):
    dp_config = get_deployment_config()
    hp_config = get_hp_config()
    meta_config = get_meta_config()
    config = update_config(hp_config, meta_config, dp_config, args)

    ensemble_model_check(config)

    project = f"{config['name']}_{args.run_type}"
    execute_model_tasks(config=config, project=project, eval=args.evaluate, forecast=args.forecast)


