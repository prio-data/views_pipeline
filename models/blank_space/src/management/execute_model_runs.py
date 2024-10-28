import sys
import wandb

from pathlib import Path
PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths
setup_project_paths(PATH)

from config_deployment import get_deployment_config
from config_hyperparameters import get_hp_config
from config_meta import get_meta_config
from config_sweep import get_sweep_config
from execute_model_tasks import execute_model_tasks
from get_data import get_data
from utils_run import update_config, update_sweep_config


def execute_sweep_run(args):
    get_data(args)

    sweep_config = get_sweep_config()
    meta_config = get_meta_config()
    update_sweep_config(sweep_config, args, meta_config)

    project = f"{sweep_config['name']}_sweep" # we can name the sweep in the config file
    sweep_id = wandb.sweep(sweep_config, project=project, entity='views_pipeline')
    wandb.agent(sweep_id, execute_model_tasks, entity='views_pipeline')


def execute_single_run(args):

    hp_config = get_hp_config()
    meta_config = get_meta_config()
    dp_config = get_deployment_config()
    config = update_config(hp_config, meta_config, dp_config, args)
    
    project = f"{config['name']}_{args.run_type}"

    self_test = True

    get_data(args, project, self_test)

    if args.run_type == 'calibration' or args.run_type == 'testing':
        execute_model_tasks(config=config, project=project, train=args.train, eval=args.evaluate,
                            forecast=False, artifact_name=args.artifact_name)

    elif args.run_type == 'forecasting':
        execute_model_tasks(config=config, project=project, train=args.train, eval=False,
                            forecast=args.forecast, artifact_name=args.artifact_name)
