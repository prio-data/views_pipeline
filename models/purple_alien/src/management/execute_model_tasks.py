
import wandb

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_artifacts_paths
setup_project_paths(PATH)

from utils import choose_model, choose_loss, choose_sheduler, get_train_tensors, get_full_tensor, apply_dropout, execute_freeze_h_option, get_log_dict, train_log, init_weights, get_data
from utils_wandb import add_wandb_monthly_metrics
from utils_device import setup_device
from train_model import make, training_loop, train_model_artifact #handle_training
# from evaluate_sweep import evaluate_posterior # see if it can be more genrel to a single model as well... 
from evaluate_model import evaluate_posterior, evaluate_model_artifact #handle_evaluation
from generate_forecast import forecast_with_model_artifact #handle_forecasting


def execute_model_tasks(config = None, project = None, train = None, eval = None, forecast = None, artifact_name = None):

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

    # Define the path for the artifacts
    PATH_ARTIFACTS = setup_artifacts_paths(PATH)

    device = setup_device()

    # Initialize WandB
    with wandb.init(project=project, entity="views_pipeline", config=config): # project and config ignored when running a sweep
        
        # add the monthly metrics to WandB
        add_wandb_monthly_metrics() 

        # Update config from WandB initialization above
        config = wandb.config

        # Retrieve data (partition) based on the configuration
        views_vol = get_data(config) # a bit HydraNet specific, but it is fine for now. If statment or move to handle_training, handle_evaluation, and handle_forecasting?

        # Handle the sweep runs
        if config.sweep:  # If we are running a sweep, always train and evaluate

            model, criterion, optimizer, scheduler = make(config, device)
            training_loop(config, model, criterion, optimizer, scheduler, views_vol, device)
            print('Done training')

            evaluate_posterior(model, views_vol, config, device)
            print('Done testing')

        # Handle the single model runs: train and save the model as an artifact
        if train:
            #handle_training(config, device, views_vol, PATH_ARTIFACTS)
            train_model_artifact(config, device, views_vol, PATH_ARTIFACTS)

        # Handle the single model runs: evaluate a trained model (artifact)
        if eval:
            #handle_evaluation(config, device, views_vol, PATH_ARTIFACTS, artifact_name)
            evaluate_model_artifact(config, device, views_vol, PATH_ARTIFACTS, artifact_name)

        if forecast:
            #handle_forecasting(config, device, views_vol, PATH_ARTIFACTS, artifact_name)
            forecast_with_model_artifact(config, device, views_vol, PATH_ARTIFACTS, artifact_name)


