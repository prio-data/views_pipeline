import sys
from pathlib import Path
import wandb

PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths
setup_project_paths(PATH)

from config_hyperparameters import get_hp_config
from config_meta import get_meta_config
from config_sweep import get_sweep_config
from execute_model_tasks import execute_model_tasks


def execute_sweep_run(args):
    sweep_config = get_sweep_config()
    meta_config = get_meta_config()
    project = f"{sweep_config['name']}_sweep" # we can name the sweep in the config file

    sweep_config['parameters']['run_type'] = {'value': args.run_type}
    sweep_config['parameters']['sweep'] = {'value': True}
    sweep_config['parameters']['depvar'] = {'value': meta_config['depvar']}
    sweep_config['parameters']['algorithm'] = {'value': meta_config['algorithm']}
    if meta_config['algorithm'] == 'HurdleRegression':
        sweep_config['parameters']['model_clf'] = {'value': meta_config['model_clf']}
        sweep_config['parameters']['model_reg'] = {'value': meta_config['model_reg']}

    sweep_id = wandb.sweep(sweep_config, project=project, entity='views_pipeline')

    wandb.agent(sweep_id, execute_model_tasks, entity='views_pipeline')


def execute_single_run(args):
    hp_config = get_hp_config()
    meta_config = get_meta_config()

    hp_config['run_type'] = args.run_type
    hp_config['sweep'] = False
    hp_config['name'] = meta_config['name']
    hp_config['depvar'] = meta_config['depvar']
    hp_config['algorithm'] = meta_config['algorithm']
    if meta_config['algorithm'] == 'HurdleRegression':
        hp_config['model_clf'] = meta_config['model_clf']
        hp_config['model_reg'] = meta_config['model_reg']

    project = f"{hp_config['name']}_{args.run_type}"

    if args.run_type == 'calibration' or args.run_type == 'testing':
        execute_model_tasks(config=hp_config, project=project, train=args.train, eval=args.evaluate,
                            forecast=False, artifact_name=args.artifact_name)

    elif args.run_type == 'forecasting':
        execute_model_tasks(config=hp_config, project=project, train=args.train, eval=False, forecast=args.forecast,
                            artifact_name=args.artifact_name)

    else:
        raise ValueError(f"Invalid run type: {args.run_type}")

