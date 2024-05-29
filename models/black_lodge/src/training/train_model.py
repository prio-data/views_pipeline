import sys
from pathlib import Path
import pandas as pd

PATH = Path(__file__) 
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils"))
from set_path import setup_project_paths, setup_data_paths, setup_artifacts_paths
setup_project_paths(PATH)

from xgboost import XGBRFRegressor

from views_partitioning.data_partitioner import DataPartitioner
from views_forecasts.extensions import *
from stepshift.views import StepshiftedModels
from views_stepshift.run import ViewsRun
from hurdle_model import HurdleRegression
from get_data import get_partition_data

from config_model import get_model_config
from config_hyperparameters import get_hp_config


def train(model_config, para_config):
    print("Training...")
    if not model_config["sweep"]:
        PATH_RAW, _, _ = setup_data_paths(PATH)
        PATH_ARTIFACTS = setup_artifacts_paths(PATH)
        dataset = pd.read_parquet(PATH_RAW / 'raw.parquet')
        if model_config["algorithm"] == "HurdleRegression":
            model = HurdleRegression(clf_name=model_config["clf_name"], reg_name=model_config["reg_name"], clf_params=para_config["clf"], reg_params=para_config["reg"])
        else:
            model = globals()[model_config["algorithm"]](**para_config)
        # print(model)
            
        # Train partition
        try:
            stepshifter_model_calib = pd.read_pickle(PATH_ARTIFACTS / "model_calib_partition.pkl")
        except:
            stepshifter_model_calib = stepshift_training(model_config, "calib", model, get_partition_data(dataset, "calibration"))
            stepshifter_model_calib.save(PATH_ARTIFACTS /"model_calib_partition.pkl")

        # Test partition
        try:
            stepshifter_model_test = pd.read_pickle(PATH_ARTIFACTS / "model_test_partition.pkl")
        except:
            stepshifter_model_test = stepshift_training(model_config, "test", model, get_partition_data(dataset, "testing"))
            stepshifter_model_test.save(PATH_ARTIFACTS / "model_test_partition.pkl")

        # Future partition
        try:
            stepshifter_model_future = pd.read_pickle(PATH_ARTIFACTS / "model_forecast_partition.pkl")
        except:
            stepshifter_model_future = stepshift_training(model_config, "forecast", model, get_partition_data(dataset, "forecasting"))
            stepshifter_model_future.save(PATH_ARTIFACTS / "model_forecast_partition.pkl")


def stepshift_training(model_config, partition_name, model, dataset):
    steps = model_config["steps"]
    target = model_config["depvar"]
    partition = DataPartitioner({partition_name: model_config[f"{partition_name}_partitioner_dict"]})
    stepshifter_def = StepshiftedModels(model, steps, target)
    stepshifter_model = ViewsRun(partition, stepshifter_def)
    stepshifter_model.fit(partition_name, "train", dataset)
    return stepshifter_model

if __name__ == "__main__":
    model_config = get_model_config()
    para_config = get_hp_config()
    train(model_config, para_config)