#V1 - not great

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from stepshift.views import StepshiftedModels
from views_runs import DataPartitioner, ViewsRun

from src.utils import get_artifacts_path, get_data_path
from src.dataloaders import data
from configs.config_common import common_config #contains data partition dictionaries
from configs.config_hyperparameters import hp_config

def train_model(): 
    """
    Trains a machine learning model and stepshifter for calibration and future predictions.

    Returns:
    - base_model (RandomForestClassifier): The trained base machine learning model.
    - stepshifter_model_calib (ViewsRun): The stepshifter model trained on the calibration partition.
    - stepshifter_model_future (ViewsRun): The stepshifter model trained on the future partition.

    Notes:
    - The function loads data from a Parquet file.
    - The function extracts configurations and hyperparameters from `common_config` and `hp_config`.
    - The base model is trained using RandomForestClassifier with specified hyperparameters.
    - StepshiftedModels are created using the base model, steps, and target extracted from common_config.
    - Two ViewsRun instances are created and trained on the calibration and future partitions respectively.
    """
    print("Training model...")

    # Define configs (TBD: integrate more elegantly into code)
    calib_partitioner_dict = common_config["calib_partitioner_dict"]
    future_partitioner_dict = common_config["future_partitioner_dict"]
    steps = common_config["steps"]
    target = common_config["target"]

    # Extract hyperparameters (TBD: integrate more elegantly into code)
    #learning_rate = hp_config["learning_rate"]
    n_estimators = hp_config["n_estimators"]
    n_jobs = hp_config["n_jobs"]

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

    return base_model, stepshifter_model_calib, stepshifter_model_future

if __name__ == "__main__":

    # Call the train_model function
    train_model()
