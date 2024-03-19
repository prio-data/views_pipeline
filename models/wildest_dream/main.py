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
from train_model import train
from generate_forecast import forecast
from evaluate_model import evaluate_model
from evaluate_sweep import evaluate_sweep
from get_data import get_data
from utils import split_hurdle_parameters


def model_pipeline(config=None, project=None):
    
    with wandb.init(project=project, entity="views_pipeline", config=config): 

        config = wandb.config

        # W&B does not directly support nested dictionaries for hyperparameters 
        if model_config['sweep'] and model_config['algorithm'] == "HurdleRegression":
            config['clf'], config['reg'] = split_hurdle_parameters(config)

        train(model_config, config)

        if model_config['sweep']:
            evaluate_sweep(model_config, config)
        else:
            evaluate_model(model_config)
            forecast(model_config)

if __name__ == "__main__":
    wandb.login()

    sweep_config = get_swep_config()
    hp_config = get_hp_config()
    model_config = get_model_config()
    model_config['calib_partitioner_dict'] = get_partitioner_dict("calibration")
    model_config['test_partitioner_dict'] = get_partitioner_dict("testing")
    model_config['forecast_partitioner_dict'] = get_partitioner_dict("forecasting")

    data = get_data()

    do_sweep = input(f'a) Do sweep \nb) Do one run \n')

    if do_sweep == 'a':
        model_config['sweep'] = True
        sweep_id = wandb.sweep(sweep_config, project=model_config["name"]+"_sweep")
        wandb.agent(sweep_id, function=model_pipeline)
    
    elif do_sweep == 'b':
        model_config['sweep'] = False
        model_pipeline(hp_config, project=model_config["name"])
