from pathlib import Path
import pandas as pd
import wandb

from configs.config_data_partitions import get_data_partitions #currently model own, not common_configs
from configs.config_hyperparameters import get_hp_config
from configs.config_model import get_model_config
from configs.config_sweep import get_sweep_config
from src.utils.set_paths import get_data_path #currently model own, not common_utils

from src.dataloaders.get_data import get_data #alternatively, import from data/raw
from src.training.train_model import train #alternatively, import from artifacts
from src.forecasting.generate_forecast import forecast #alternatively, import from data/generated
from src.offline_evaluation.evaluate_model import evaluate_model
#from src.offline_evaluation.evaluate_sweep import evaluate_sweep #not written yet


def run_model(config=None, project=None):
    """
    Runs the model training, forecasting, and evaluation scripts using the provided configuration and project name. Initializes and log on Weights & Biases.

    Args:
        config (dict, optional): A dictionary containing configuration parameters for the model.
                                 Default is None.
        project (str, optional): The name of the project to log results to in Weights & Biases (WandB).
                                 Default is None.

    Returns:
        None

    """
    
    with wandb.init(project=project, entity="views_pipeline", config=config): 

        config = wandb.config 

        data = get_data()

        model_calibration_partition, model_future_partition = train(model_config, hp_config, data_partitions)

        if model_config['sweep']:
            evaluate_sweep(model_config, config)
        else:
            forecast(data_partitions, model_calibration_partition, model_future_partition)
            evaluate_model(model_config)


if __name__ == "__main__":
    wandb.login()

    data_partitions = get_data_partitions()
    model_config = get_model_config()
    sweep_config = get_sweep_config()
    hp_config = get_hp_config()

    do_sweep = input(f'a) Do sweep \nb) Do one run \n')

    if do_sweep == 'a':
        model_config['sweep'] = True
        sweep_id = wandb.sweep(sweep_config, project=model_config["name"]+"_sweep")
        wandb.agent(sweep_id, function=run_model)
    
    elif do_sweep == 'b':
        model_config['sweep'] = False
        run_model(hp_config, project=model_config["name"])
