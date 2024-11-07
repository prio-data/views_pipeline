import wandb
from config_deployment import get_deployment_config
from config_hyperparameters import get_hp_config
from config_meta import get_meta_config
from config_sweep import get_sweep_config
from execute_model_tasks import execute_model_tasks
# from get_data import get_data
from utils_run import update_config, update_sweep_config
from dataloaders import DataLoader
from model_path import ModelPath
from pathlib import Path

def execute_sweep_run(args):

    sweep_config = get_sweep_config()
    meta_config = get_meta_config()
    update_sweep_config(sweep_config, args, meta_config)

    project = f"{sweep_config['name']}_sweep"  # we can name the sweep in the config file

    sweep_id = wandb.sweep(sweep_config, project=project, entity='views_pipeline')

    with wandb.init(project=f'{project}_fetch', entity="views_pipeline"):

        data_loader = DataLoader(model_path=ModelPath(Path(__file__)))
        data_loader.get_data(use_saved=args.saved, validate=True, self_test=args.drift_self_test, partition=args.run_type)

    wandb.finish()

    wandb.agent(sweep_id, execute_model_tasks, entity='views_pipeline')


def execute_single_run(args):
    hp_config = get_hp_config()
    meta_config = get_meta_config()
    dp_config = get_deployment_config()
    config = update_config(hp_config, meta_config, dp_config, args)

    project = f"{config['name']}_{args.run_type}"

    with wandb.init(project=f'{project}_fetch', entity="views_pipeline"):

        # get_data(args, config["name"], args.drift_self_test)
        data_loader = DataLoader(model_path=ModelPath(Path(__file__)))
        data_loader.get_data(use_saved=args.saved, validate=True, self_test=args.drift_self_test, partition=args.run_type)

    wandb.finish()

    if args.run_type == "calibration" or args.run_type == "testing":
        execute_model_tasks(config=config, project=project, train=args.train, eval=args.evaluate,
                            forecast=False, artifact_name=args.artifact_name)

    elif args.run_type == "forecasting":
        execute_model_tasks(config=config, project=project, train=args.train, eval=False,
                            forecast=args.forecast, artifact_name=args.artifact_name)
