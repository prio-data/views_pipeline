#orchestration of model

import sys
from pathlib import Path
import pandas as pd
import wandb

print(sys.path)

from src.dataloaders import get_data
from src.training import train
from src.forecasting import generate_forecast
from configs.config_data_partitions import get_data_partitions
from configs.config_hyperparameters import get_hp_config
from configs.config_model import get_model_config
from configs.config_sweep import get_sweep_config
from src.utils.set_paths import get_data_path

def model_pipeline(config=None, project=None):
    
    with wandb.init(project=project, entity="views_pipeline", config=config): 

        config = wandb.config        

        stepshifter_model_calib, stepshifter_model_future = train(model_config, hyperparameters, data_partitions)

        if model_config['sweep']:
            evaluate_sweep(model_config, config)
        else:
            evaluate_model(model_config)
            generate_forecast(data_partitions, stepshifter_model_calib, stepshifter_model_future)

if __name__ == "__main__":
    wandb.login()

    data_partitions = get_data_partitions()
    hyperparameters = get_hp_config()
    model_config = get_model_config()

    sweep_config = get_sweep_config()
    hp_config = get_hp_config()
    model_config = get_model_config()

    data = pd.read_parquet(get_data_path("raw"))

    do_sweep = input(f'a) Do sweep \nb) Do one run \n')

    if do_sweep == 'a':
        model_config['sweep'] = True
        sweep_id = wandb.sweep(sweep_config, project=common_config["name"]+"_sweep")
        wandb.agent(sweep_id, function=model_pipeline)
    
    elif do_sweep == 'b':
        model_config['sweep'] = False
        model_pipeline(hp_config, project=model_config["name"])
