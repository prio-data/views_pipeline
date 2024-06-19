import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

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
from set_partition import get_partitioner_dict
from utils import get_parameters

def get_model(config):
    if config["algorithm"] == "HurdleRegression":
        model = HurdleRegression(clf_name=config["model_clf"], reg_name=config["model_reg"],
                                 clf_params=config["clf"], reg_params=config["reg"])
    else:
        parameters = get_parameters(config)
        model = globals()[config["algorithm"]](**parameters)
    return model

def train_model_artifact(config, model):
    # print(config)
    PATH_RAW, _, _ = setup_data_paths(PATH)
    PATH_ARTIFACTS = setup_artifacts_paths(PATH)

    run_type = config['run_type']
    dataset = pd.read_parquet(PATH_RAW / f'raw_{run_type}.parquet')

    stepshift_model = stepshift_training(config, run_type, model, get_partition_data(dataset, run_type))
    if not config["sweep"]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_filename = f"{config.run_type}_model_{timestamp}.pkl"
        stepshift_model.save(PATH_ARTIFACTS / model_filename)
    return stepshift_model


def stepshift_training(config, partition_name, model, dataset):
    steps = config["steps"]
    target = config["depvar"]
    partitioner_dict = get_partitioner_dict(partition_name)
    partition = DataPartitioner({partition_name: partitioner_dict})
    stepshift_def = StepshiftedModels(model, steps, target)
    stepshift_model = ViewsRun(partition, stepshift_def)
    stepshift_model.fit(partition_name, "train", dataset)
    return stepshift_model