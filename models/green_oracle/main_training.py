from .src.training import training
from .src.forecasting import true_future_36m as forecast
from .src.visualization.visual import visualize_forecasts_in_maps
from .src.evaluation.evaluation_mse import evaluate_mse
from .src.utils.utils import wandb_init, wandb_finish
from .configs import wandb_config

def main():
    # training.training()
    wandb_init(wandb_config.project_config['project'], wandb_config.project_config['entity'])
    forecast.forecast()
    visualize_forecasts_in_maps(12)
    evaluate_mse()
    wandb_finish()
    
if __name__ == "__main__":
    main()