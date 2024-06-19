import sys
from pathlib import Path
import pandas as pd

PATH = Path(__file__) 
from set_path import setup_project_paths, setup_data_paths, setup_artifacts_paths
setup_project_paths(PATH)

from lightgbm import LGBMRegressor

from views_partitioning.data_partitioner import DataPartitioner
from views_forecasts.extensions import *
from stepshift.views import StepshiftedModels
from views_stepshift.run import ViewsRun
from hurdle_model import HurdleRegression
from get_data import get_partition_data


def get_model(model_config, para_config):
    if model_config["algorithm"] == "HurdleRegression":
        model = HurdleRegression(clf_name=model_config["clf_name"], reg_name=model_config["reg_name"],
                                 clf_params=para_config["clf"], reg_params=para_config["reg"])
    else:
        model = globals()[model_config["algorithm"]](**para_config)
    # print(model)
    return model

def train_model(model, model_config):
    PATH_RAW, _, _ = setup_data_paths(PATH)
    PATH_ARTIFACTS = setup_artifacts_paths(PATH)
    dataset = pd.read_parquet(PATH_RAW / 'raw_calibration.parquet')
    run_type = model_config['run_type']

    if model_config["sweep"]:
        stepshift_model = stepshift_training(model_config, run_type, model, get_partition_data(dataset, run_type))
    else:
        try:
            stepshift_model = pd.read_pickle(PATH_ARTIFACTS / f"model_{run_type}_partition.pkl")
        except:
            stepshift_model = stepshift_training(model_config, run_type, model, get_partition_data(dataset, run_type))
            stepshift_model.save(PATH_ARTIFACTS / f"model_{run_type}_partition.pkl")
    return stepshift_model


def stepshift_training(model_config, partition_name, model, dataset):
    steps = model_config["steps"]
    target = model_config["depvar"]
    partition = DataPartitioner({partition_name: model_config[f"{partition_name}_partitioner_dict"]})
    stepshift_def = StepshiftedModels(model, steps, target)
    stepshift_model = ViewsRun(partition, stepshift_def)
    stepshift_model.fit(partition_name, "train", dataset)
    return stepshift_model