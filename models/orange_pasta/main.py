import wandb
from pathlib import Path

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
            evaluate_sweep(common_config)
        else:
            evaluate_model(common_config)

        predictions = forecast()

if __name__ == "__main__":
    wandb.login()
    parque_path = Path(__file__).parent/"data/raw/raw.parquet"
    if not parque_path.exists():
        data = get_data()
    common_config = get_common_config()
    sweep_config = get_swep_config()
    hp_config = get_hp_config()

    do_sweep = input(f'a) Do sweep \nb) Do one run \n')

    if do_sweep == 'a':
        common_config['sweep'] = True
        sweep_id = wandb.sweep(sweep_config, project=common_config["name"]+"_sweep")
        wandb.agent(sweep_id, function=model_pipeline)
    
    elif do_sweep == 'b':
        common_config['sweep'] = False
        model_pipeline(hp_config, project=common_config["name"])
