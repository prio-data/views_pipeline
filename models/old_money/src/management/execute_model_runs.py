import wandb
from config_deployment import get_deployment_config
from config_hyperparameters import get_hp_config
from config_meta import get_meta_config
from config_sweep import get_sweep_config
from execute_model_tasks import execute_model_tasks
from get_data import get_data
from utils_run import update_config, update_sweep_config


def execute_sweep_run(args):
    sweep_config = get_sweep_config()
    meta_config = get_meta_config()
    update_sweep_config(sweep_config, args, meta_config)

    get_data(args, sweep_config["name"])

    project = f"{sweep_config['name']}_sweep"  # we can name the sweep in the config file
    sweep_id = wandb.sweep(sweep_config, project=project, entity="views_pipeline")
    wandb.agent(sweep_id, execute_model_tasks, entity="views_pipeline")


def execute_single_run(args):
    hp_config = get_hp_config()
    meta_config = get_meta_config()
    dp_config = get_deployment_config()
    config = update_config(hp_config, meta_config, dp_config, args)

    get_data(args, config["name"])

    project = f"{config['name']}_{args.run_type}"

    if args.run_type == "calibration" or args.run_type == "testing":
        execute_model_tasks(config=config, project=project, train=args.train, eval=args.evaluate,
                            forecast=False, artifact_name=args.artifact_name)

    elif args.run_type == "forecasting":
        execute_model_tasks(config=config, project=project, train=args.train, eval=False,
                            forecast=args.forecast, artifact_name=args.artifact_name)
