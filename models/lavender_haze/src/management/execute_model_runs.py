import wandb

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths, setup_artifacts_paths

setup_project_paths(PATH)

from config_sweep import get_sweep_config
from config_hyperparameters import get_hp_config
from execute_model_tasks import execute_model_tasks


def execute_sweep_run(args):
    print('Running sweep...')

    sweep_config = get_sweep_config()
    project = f"{sweep_config['name']}_sweep" # we can name the sweep in the config file

    sweep_config['parameters']['run_type'] = {'value': "calibration"}
    sweep_config['parameters']['sweep'] = {'value': True}

    sweep_id = wandb.sweep(sweep_config, project=project, entity='views_pipeline')

    wandb.agent(sweep_id, execute_model_tasks, entity='views_pipeline')


def execute_single_run(args):
    hyperparameters = get_hp_config()
    hyperparameters['run_type'] = args.run_type
    hyperparameters['sweep'] = False

    project = f"{hyperparameters['name']}_{args.run_type}"

    if args.run_type == 'calibration' or args.run_type == 'testing':
        execute_model_tasks(config=hyperparameters, project=project, train=args.train, eval=args.evaluate,
                            forecast=False, artifact_name=args.artifact_name)

    elif args.run_type == 'forecasting':
        execute_model_tasks(config=hyperparameters, project=project, train=args.train, eval=False, forecast=True,
                            artifact_name=args.artifact_name)

    else:
        raise ValueError(f"Invalid run type: {args.run_type}")

