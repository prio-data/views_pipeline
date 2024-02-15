from ..blue_sea.src.dataloaders.fetch_data_run_query import fetch_data
from ..blue_sea.src.forecasting.true_future_36m import forecast
from ..blue_sea.src.evaluation.evaluation_mse import evaluate_mse
from ..blue_sea.configs import config

from .src.utils.utils import wandb_init, wandb_finish
from .configs import wandb_config
from ..blue_sea.src.visualization.visual import visualize_forecasts_in_maps

def main():
    wandb_init(
        wandb_config.project_config['project'], wandb_config.project_config['entity'])
    data_for_training = fetch_data()
    start_month, end_month = config.common_config['future_partitioner_dict']['predict']
    forecasts = forecast(data_for_training.loc[start_month:end_month])
    print(forecasts)
    visualize_forecasts_in_maps(12)
    evaluate_mse()
    wandb_finish()
    print(config.common_config)
    
if __name__ == "__main__":
    data_for_training = fetch_data()
    start_month, end_month = config.common_config['future_partitioner_dict']['predict']
    forecasts = forecast(data_for_training.loc[start_month:end_month])    
    print(forecasts)
    evaluate_mse()
    print(config.common_config)

