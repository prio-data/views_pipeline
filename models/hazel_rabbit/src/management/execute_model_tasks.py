
import wandb

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_artifacts_paths, setup_data_paths

from ingester3.ViewsMonth import ViewsMonth
setup_project_paths(PATH)

from utils import get_raw_data
from utils_wandb import add_wandb_monthly_metrics


from evaluate_model import evaluate_model_artifact 
from generate_forecast import forecast_with_model_artifact



def execute_model_tasks(config = None, project = None, train = None, eval = None, forecast = None):

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
    """

    # Define the path for the artifacts
    PATH_ARTIFACTS = setup_artifacts_paths(PATH)

    #device = setup_device()

    # Initialize WandB
    with wandb.init(project=project, entity="views_pipeline", config=config): # project and config ignored when running a sweep 
        
        # add the monthly metrics to WandB
        add_wandb_monthly_metrics() 

        # Update config from WandB initialization above
        config = wandb.config

        # Retrieve raw data (partition) based on the configuration
        views_raw = get_raw_data(config) 
        

        # Handle the sweep runs
        if config.sweep:  

            pass

        # Handle the single model runs: train and save the model as an artifact
        if train:
        
            print('No need to train the zero baseline model. Exiting...')
            pass

        # Handle the single model runs: evaluate a trained model (artifact)
        if eval:
            #handle_evaluation(config, device, views_vol, PATH_ARTIFACTS, artifact_name)
            evaluate_model_artifact(config, views_raw)



        if forecast:
            #handle_forecasting(config, device, views_vol, PATH_ARTIFACTS, artifact_name)
            forecast_with_model_artifact(config, views_raw)

            
