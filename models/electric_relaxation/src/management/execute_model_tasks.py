import sys
import wandb

import logging
logging.basicConfig(filename='../../run.log', encoding='utf-8', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from pathlib import Path
PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths
setup_project_paths(PATH)

from evaluate_model import evaluate_model_artifact
from evaluate_sweep import evaluate_sweep
from generate_forecast import forecast_model_artifact
from train_model import train_model_artifact
from utils import get_model, split_hurdle_parameters
from utils_wandb import add_wandb_monthly_metrics


def execute_model_tasks(config=None, project=None, train=None, eval=None, forecast=None, artifact_name=None):
    """
        Executes various model-related tasks including training, evaluation, and forecasting.

    This function manages the execution of different tasks such as training the model,
    evaluating an existing model, or performing forecasting.
    It also initializes the WandB project.

    Args:
        config: Configuration object containing parameters and settings.
        project: The WandB project name.
        train: Flag to indicate if the model should be trained.
        eval: Flag to indicate if the model should be evaluated.
        forecast: Flag to indicate if forecasting should be performed.
        artifact_name (optional): Specific name of the model artifact to load for evaluation or forecasting.
    """

    # Initialize WandB
    with wandb.init(project=project, entity="views_pipeline",
                    config=config):  # project and config ignored when running a sweep

        # add the monthly metrics to WandB
        add_wandb_monthly_metrics()

        # Update config from WandB initialization above
        config = wandb.config

        # W&B does not directly support nested dictionaries for hyperparameters
        # This will make the sweep config super ugly, but we don't have to distinguish between sweep and single runs
        if config['sweep'] and config['algorithm'] == "HurdleRegression":
            config['parameters'] = {}
            config['parameters']['clf'], config['parameters']['reg'] = split_hurdle_parameters(config)

        model = get_model(config)
        # logger.info(model)

        if config['sweep']:
            logger.info(f"Sweeping model {config['name']}...")
            stepshift_model = train_model_artifact(config, model)
            logger.info(f"Evaluating model {config['name']}...")
            evaluate_sweep(config, stepshift_model)

        # Handle the single model runs: train and save the model as an artifact
        if train:
            logger.info(f"Training model {config['name']}...")
            train_model_artifact(config, model)

        # Handle the single model runs: evaluate a trained model (artifact)
        if eval:
            logger.info(f"Evaluating model {config['name']}...")
            evaluate_model_artifact(config, artifact_name)

        if forecast:
            logger.info(f"Forecasting model {config['name']}...")
            forecast_model_artifact(config, artifact_name)
