import wandb
from pathlib import Path
import sys
PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths
setup_project_paths(PATH)

from set_partition import get_partitioner_dict
from config_hyperparameters import get_hp_config
from config_sweep import get_swep_config
from config_model import get_model_config
from train_model import train_model, get_model
from generate_forecast import forecast_model
from evaluate_model import evaluate_model
from evaluate_sweep import evaluate_sweep
from get_data import get_data
from utils import split_hurdle_parameters
from cli_parser_utils import parse_args, validate_arguments


def model_pipeline(config=None, project=None, train=None, eval=None, forecast=None):
    
    with wandb.init(project=project, entity="views_pipeline", config=config):

        config = wandb.config

        # W&B does not directly support nested dictionaries for hyperparameters 
        if model_config['sweep'] and model_config['algorithm'] == "HurdleRegression":
            config['clf'], config['reg'] = split_hurdle_parameters(config)

        model = get_model(model_config, config)
        if model_config['sweep']:
            print("Sweeping...")
            stepshift_model = train_model(model, model_config)
            evaluate_sweep(stepshift_model, model_config)
        else:
            print("Training...")
            if train:
                stepshift_model = train_model(model, model_config)
            if eval:
                evaluate_model(model_config)
            if forecast:
                forecast_model(model_config)

if __name__ == "__main__":
    args = parse_args()
    validate_arguments(args)

    wandb.login()

    sweep_config = get_swep_config()
    hp_config = get_hp_config()
    model_config = get_model_config()
    model_config['calibration_partitioner_dict'] = get_partitioner_dict("calibration")
    model_config['testing_partitioner_dict'] = get_partitioner_dict("testing")
    model_config['forecasting_partitioner_dict'] = get_partitioner_dict("forecasting")
    model_config['run_type'] = args.run_type

    data = get_data()

    if args.sweep:
        model_config['sweep'] = True
        sweep_id = wandb.sweep(sweep_config, project=model_config["name"]+"_sweep")
        wandb.agent(sweep_id, function=model_pipeline)
    
    else:
        model_config['sweep'] = False
        if args.run_type == 'forecasting':
            forecast = True
        else:
            forecast = False
        model_pipeline(hp_config, project=model_config["name"], train=args.train, eval=args.evaluate, forecast=forecast)

