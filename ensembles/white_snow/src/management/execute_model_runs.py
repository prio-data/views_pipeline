import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths
setup_project_paths(PATH)

from config_hyperparameters import get_hp_config
from execute_model_tasks import execute_model_tasks


def execute_single_run(args):
    hyperparameters = get_hp_config()
    hyperparameters['run_type'] = args.run_type
    hyperparameters['aggregation'] = args.aggregation

    project = f"{hyperparameters['name']}_{args.run_type}"

    if args.run_type in ['calibration', 'testing', 'forecasting']:
        execute_model_tasks(config=hyperparameters, project=project, eval=args.evaluate, forecast=args.forecast)

    else:
        raise ValueError(f"Invalid run type: {args.run_type}")

