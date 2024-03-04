#TBD: clean up repetitions, add wandb

import sys
from pathlib import Path
import pandas as pd

from sklearn.ensemble import RandomForestClassifier

from stepshift.views import StepshiftedModels
from views_runs import DataPartitioner, ViewsRun

#import modules from model folder
model_path = Path(__file__).resolve().parents[2] 
sys.path.append(str(model_path))
from configs.config_data_partition import get_data_partitions #TBD: change to common_config
from configs.config_hyperparameters import get_hyperparameters
from configs.config_model import get_model_config
from configs.config_sweep import sweep_config
from src.utils.set_paths import get_data_path

def train_model(): 
    """
    Trains a machine learning model and stepshifter for calibration and future predictions.

    Returns:
    - base_model (RandomForestClassifier): The trained base machine learning model.
    - stepshifter_model_calib (ViewsRun): The stepshifter model trained on the calibration partition.
    - stepshifter_model_future (ViewsRun): The stepshifter model trained on the future partition.

    Notes:
    - The function loads data from a Parquet file.
    - The base model is trained using RandomForestClassifier with specified hyperparameters.
    - StepshiftedModels are created using the base model, steps, and target extracted from common_config.
    - Two ViewsRun instances are created and trained on the calibration and future partitions respectively.
    """
    print("Training models...")

    # Define configs (TBD: integrate more elegantly into code)
    data_partitions = get_data_partitions()
    model_config = get_model_config()
    calib_partitioner_dict = data_partitions["calib_partitioner_dict"]
    future_partitioner_dict = data_partitions["future_partitioner_dict"]
    steps = data_partitions["steps"] #steps can also go into model_config
    target = model_config["target"]

    # Extract hyperparameters (TBD: integrate more elegantly into code)
    #learning_rate = hp_config["learning_rate"]
    hyperparameters = get_hyperparameters()
    n_estimators = hyperparameters["n_estimators"]
    n_jobs = hyperparameters["n_jobs"]

    # Load data
    data = pd.read_parquet(get_data_path("raw"))

    #Below we have the original code from the Jupyter notebook:

    # Create data partitioners
    calib_partition = DataPartitioner({'calib': calib_partitioner_dict})
    future_partition = DataPartitioner({'future': future_partitioner_dict})

    # Fitting base model and stepshifter
    base_model = RandomForestClassifier(n_estimators=n_estimators, n_jobs=n_jobs) #TBD: write this more elegantly
    stepshifter_def = StepshiftedModels(base_model, steps, target) #TBD: write this more elegantly

    # Fitting for calibration run, calibration partition
    stepshifter_model_calib = ViewsRun(calib_partition, stepshifter_def)
    stepshifter_model_calib.fit('calib', 'train', data)

    # Fitting for future run
    stepshifter_model_future = ViewsRun(future_partition, stepshifter_def)
    stepshifter_model_future.fit('future', 'train', data)

    print("Models trained!")


    return stepshifter_model_calib, stepshifter_model_future



if __name__ == "__main__":

    # Call the train_model function
    train_model()
