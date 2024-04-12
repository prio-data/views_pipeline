import sys
from pathlib import Path
import pandas as pd
import pickle

from sklearn.ensemble import RandomForestClassifier

from stepshift.views import StepshiftedModels
from views_runs import DataPartitioner, ViewsRun

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS
from set_path import setup_project_paths, setup_artifacts_paths, setup_data_paths
setup_project_paths(PATH) #adds all necessary paths to sys.path

from config_data_partitions import get_data_partitions #change to common_utils/set_partition.py
from config_hyperparameters import get_hp_config
from config_model import get_model_config
#from config_sweep import get_sweep_config

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

    Note:
    - The 'artifacts' directory must exist in the system path for saving and loading pickle files.
    - Ensure that the raw dataset is successfully loaded before proceeding with model training.
    """

    print("Training...")

    artifacts_path = setup_artifacts_paths(PATH)
    calib_pickle_path = artifacts_path / "model_calibration_partition.pkl"
    future_pickle_path = artifacts_path / "model_future_partition.pkl"
    
    if calib_pickle_path.exists() and future_pickle_path.exists():
        print("Pickle files already exist. Loading models from pickle files...")
        with open(calib_pickle_path, 'rb') as file:
            model_calibration_partition = pickle.load(file)
        with open(future_pickle_path, 'rb') as file:
            model_future_partition = pickle.load(file)
    
    else:
        setup_data_paths(Path(__file__))
        dataset = pd.read_parquet("raw") # Load from raw data path
        assert not dataset.empty, "Data loading failed."

        calib_partition = DataPartitioner({'calib': data_partitions["calib_partitioner_dict"]})
        future_partition = DataPartitioner({'future': data_partitions["future_partitioner_dict"]})
        base_model = [model_config["algorithm"]](n_estimators=hp_config["n_estimators"], n_jobs=hp_config["n_jobs"])
        stepshifter_def = StepshiftedModels(base_model, model_config["steps"], model_config["depvar"])

        model_calibration_partition = ViewsRun(calib_partition, stepshifter_def)
        model_calibration_partition.fit('calib', 'train', dataset)

        model_future_partition = ViewsRun(future_partition, stepshifter_def)
        model_future_partition.fit('future', 'train', dataset)

        assert model_calibration_partition is not None and model_future_partition is not None, "Model training failed."

        with open(calib_pickle_path, 'wb') as file:
            pickle.dump(model_calibration_partition, file)
        with open(future_pickle_path, 'wb') as file:
            pickle.dump(model_future_partition, file)
            
        print("Models trained and saved in artifacts folder!")

    return model_calibration_partition, model_future_partition

if __name__ == "__main__": 
    data_partitions = get_data_partitions()
    hp_config = get_hp_config()
    model_config = get_model_config()

    model_calibration_partition, model_future_partition = train(model_config, hp_config, data_partitions)


