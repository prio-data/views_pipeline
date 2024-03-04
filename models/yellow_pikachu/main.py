import wandb
from pathlib import Path
import sys
pipeline_path = f"{Path(__file__).parent.parent.parent}"
sys.path.append(str(pipeline_path))
sys.path.append(str(pipeline_path)+"/common_utils")

from common_utils.set_partition import get_partitioner_dict
from configs.config_hyperparameters import get_hp_config
from configs.config_sweep import get_swep_config
from configs.config_common import get_common_config
from src.training.train_model import train
from src.forecasting.generate_forecast import forecast
from src.offline_evaluation.evaluate_model import evaluate_model
from src.offline_evaluation.evaluate_sweep import evaluate_sweep
from src.dataloaders.get_data import get_data


def model_pipeline(config=None, project=None):
    
    with wandb.init(project=project, entity="views_pipeline", config=config): 

        config = wandb.config
        train(common_config, config)

        if common_config['sweep']:
            evaluate_sweep(common_config, config)
        else:
            evaluate_model(common_config)
            forecast(common_config)

if __name__ == "__main__":
    wandb.login()

    sweep_config = get_swep_config()
    hp_config = get_hp_config()
    common_config = get_common_config()
    common_config['calib_partitioner_dict'] = get_partitioner_dict("calibration")
    common_config['test_partitioner_dict'] = get_partitioner_dict("testing")
    common_config['forecast_partitioner_dict'] = get_partitioner_dict("forecasting")

    data = get_data(common_config)

    do_sweep = input(f'a) Do sweep \nb) Do one run \n')

    if do_sweep == 'a':
        common_config['sweep'] = True
        sweep_id = wandb.sweep(sweep_config, project=common_config["name"]+"_sweep")
        wandb.agent(sweep_id, function=model_pipeline)
    
    elif do_sweep == 'b':
        common_config['sweep'] = False
        model_pipeline(hp_config, project=common_config["name"])
