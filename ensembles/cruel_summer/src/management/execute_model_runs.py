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

    project = f"{config['name']}_{args.run_type}"
    
    if args.train:
        execute_model_tasks(config=config, project=project, train=args.train, eval=args.evaluate, forecast=args.forecast)
    else:
        ensemble_model_check(config)
        execute_model_tasks(config=config, project=project, train=args.train, eval=args.evaluate, forecast=args.forecast)