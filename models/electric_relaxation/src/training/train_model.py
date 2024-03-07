import sys
from pathlib import Path
import pandas as pd
import pickle

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
from src.utils.set_paths import get_raw_data_path, get_artifacts_path

def train(model_config, hp_config, data_partitions): 
    """
    Train models using provided configurations.

    This function trains models for calibration and future partitions based on the provided configurations. If pickle
    files containing the trained models already exist, it loads the models from the files. Otherwise, it trains the
    models from scratch, saves them as pickle files, and returns the trained models.

    Args:
    - model_config (dict): Model configuration parameters.
    - hp_config (dict): Algorithm-specific hyperparameters.
    - data_partitions (dict): Data partitions for calibration, testing, forecasting

    Returns:
    - tuple: Trained models for calibration and future partitions.
    """

    print("Training...")

    #calib_pickle_path = get_artifacts_path("calibration") #not sure why code doesn't run well with these
    #future_pickle_path = get_artifacts_path("forecast")
    calib_pickle_path = model_path / "artifacts" / "model_calibration_partition.pkl"
    future_pickle_path = model_path / "artifacts" / "model_future_partition.pkl"
    print(calib_pickle_path)
    print(future_pickle_path)
    
    if calib_pickle_path.exists() and future_pickle_path.exists():
        print("Pickle files already exist. Loading models from pickle files...")
        with open(calib_pickle_path, 'rb') as file:
            model_calibration_partition = pickle.load(file)
        with open(future_pickle_path, 'rb') as file:
            model_future_partition = pickle.load(file)
    
    else:
        dataset = pd.read_parquet(get_raw_data_path("raw"))
        assert not dataset.empty, "Data loading failed."

        calib_partition = DataPartitioner({'calib': data_partitions["calib_partitioner_dict"]})
        future_partition = DataPartitioner({'future': data_partitions["future_partitioner_dict"]})
        n_estimators = hp_config["n_estimators"]
        n_jobs = hp_config["n_jobs"]
        base_model = RandomForestClassifier(n_estimators=n_estimators, n_jobs=n_jobs)
        steps = model_config["steps"]
        target = model_config["depvar"]
        stepshifter_def = StepshiftedModels(base_model, steps, target)

        model_calibration_partition = ViewsRun(calib_partition, stepshifter_def)
        model_calibration_partition.fit('calib', 'train', dataset)

        model_future_partition = ViewsRun(future_partition, stepshifter_def)
        model_future_partition.fit('future', 'train', dataset)

        assert model_calibration_partition is not None and model_future_partition is not None, "Model training failed."

        with open(calib_pickle_path, 'wb') as file:
            pickle.dump(stepshifter_model_calib, file)
        with open(future_pickle_path, 'wb') as file:
            pickle.dump(stepshifter_model_future, file)
            
        print("Models trained and saved!")

    return model_calibration_partition, model_future_partition

#Run this script by itself:
if __name__ == "__main__": 
    # Load configuration data
    data_partitions = get_data_partitions()
    hyperparameters = get_hp_config()
    model_config = get_model_config()

    # Call the train function with configuration data
    model_calibration_partition, model_future_partition = train(model_config, hyperparameters, data_partitions)


