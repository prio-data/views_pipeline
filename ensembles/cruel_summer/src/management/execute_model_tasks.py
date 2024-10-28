import sys
import wandb
import logging
import time

from pathlib import Path
PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths
setup_project_paths(PATH)

from evaluate_ensemble import evaluate_ensemble
from generate_forecast import forecast_ensemble
from utils_wandb import add_wandb_monthly_metrics

logger = logging.getLogger(__name__)


def execute_model_tasks(config=None, project=None, eval=None, forecast=None):
    """
        Executes various model-related tasks including training, evaluation, and forecasting.

    This function manages the execution of different tasks such as training the model,
    evaluating an existing model, or performing forecasting.
    It also initializes the WandB project.

    Args:
        config: Configuration object containing parameters and settings.
        project: The WandB project name.
        eval: Flag to indicate if the model should be evaluated.
        forecast: Flag to indicate if forecasting should be performed.
        artifact_name (optional): Specific names of the model artifact to load for evaluation or forecasting.
    """

    start_t = time.time()

    # Initialize WandB
    with wandb.init(project=project, entity="views_pipeline",
                    config=config):  # project and config ignored when running a sweep

        # add the monthly metrics to WandB
        add_wandb_monthly_metrics()

        # Update config from WandB initialization above
        config = wandb.config

        # Handle the single model runs: evaluate a trained model (artifact)
        if eval:
            logger.info(f"Evaluating ensemble model {config['name']}...")
            evaluate_ensemble(config)

        if forecast:
            logger.info(f"Forecasting ensemble model {config['name']}...")
            forecast_ensemble(config)

        end_t = time.time()
        minutes = (end_t - start_t) / 60
        logger.info(f'Done. Runtime: {minutes:.3f} minutes.\n')
