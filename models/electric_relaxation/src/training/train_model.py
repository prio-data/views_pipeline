import sys
from pathlib import Path
import pandas as pd

from sklearn.ensemble import RandomForestClassifier

from stepshift.views import StepshiftedModels
from views_runs import DataPartitioner, ViewsRun

#import modules from model folder
model_path = Path(__file__).resolve().parents[2] 
sys.path.append(str(model_path))
print(sys.path)

from configs.config_data_partitions import get_data_partitions 
from configs.config_hyperparameters import get_hp_config
from configs.config_model import get_model_config
#from configs.config_sweep import get_sweep_config
from src.utils.set_paths import get_data_path

def train(model_config, hp_config, data_partitions): 
    """
    Train models using provided configurations.

    Args:
    - model_config (dict): Model configuration parameters.
    - hp_config (dict): Algorithm-specific hyperparameters.
    - data_partitions (dict): Data partitions for calibration, testing, forecasting

    Returns:
    - tuple: Trained models for calibration and future partitions.
    """

    print("Training...")

    # Load data
    dataset = pd.read_parquet(get_data_path("raw"))
    assert not dataset.empty, "Data loading failed."

    # Create data partitioners
    calib_partition = DataPartitioner({'calib': data_partitions["calib_partitioner_dict"]})
    future_partition = DataPartitioner({'future': data_partitions["future_partitioner_dict"]})

    # Extract hyperparameters
    n_estimators = hp_config["n_estimators"]
    n_jobs = hp_config["n_jobs"]

    # Instantiate base model
    base_model = RandomForestClassifier(n_estimators=n_estimators, n_jobs=n_jobs)

    # Define steps and target
    steps = model_config["steps"]
    target = model_config["depvar"]

    # Define stepshifter model
    stepshifter_def = StepshiftedModels(base_model, steps, target)

    # Fitting for calibration run, calibration partition
    stepshifter_model_calib = ViewsRun(calib_partition, stepshifter_def)
    stepshifter_model_calib.fit('calib', 'train', dataset)

    # Fitting for future run
    stepshifter_model_future = ViewsRun(future_partition, stepshifter_def)
    stepshifter_model_future.fit('future', 'train', dataset)

    assert stepshifter_model_calib is not None and stepshifter_model_future is not None, "Model training failed."

    print("Models trained!")

    return stepshifter_model_calib, stepshifter_model_future

#Run this script by itself:
if __name__ == "__main__": 
    # Load configuration data
    data_partitions = get_data_partitions()
    hyperparameters = get_hp_config()
    model_config = get_model_config()

    # Call the train function with configuration data
    stepshifter_model_calib, stepshifter_model_future = train(model_config, hyperparameters, data_partitions)


