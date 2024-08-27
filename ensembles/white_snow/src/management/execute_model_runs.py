import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths
setup_project_paths(PATH)

from config_hyperparameters import get_hp_config
from config_meta import get_meta_config
from execute_model_tasks import execute_model_tasks


def execute_single_run(args):
    hp_config = get_hp_config()
    meta_config = get_meta_config()

    hp_config['run_type'] = args.run_type
    hp_config['aggregation'] = args.aggregation
    hp_config['name'] = meta_config['name']
    hp_config['models'] = meta_config['models']
    hp_config['depvar'] = meta_config['depvar']

    project = f"{hp_config['name']}_{args.run_type}"

    if args.run_type in ['calibration', 'testing', 'forecasting']:
        execute_model_tasks(config=hp_config, project=project, eval=args.evaluate, forecast=args.forecast)

    else:
        raise ValueError(f"Invalid run type: {args.run_type}")

