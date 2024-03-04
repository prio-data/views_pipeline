from pathlib import Path
import pandas as pd

import sys
pipeline_path = f"{Path(__file__).parent.parent.parent.parent.parent}"
sys.path.append(str(pipeline_path)+"/common_utils")

from xgboost import XGBRegressor

from common_utils.set_path import get_artifacts_path, get_data_path
from views_partitioning.data_partitioner import DataPartitioner
from views_forecasts.extensions import *
from stepshift.views import StepshiftedModels
from common_utils.views_stepshift.run import ViewsRun


def train(common_config, para_config):
    print("Training...")
    if not common_config["sweep"]:
        model = globals()[common_config["algorithm"]](**para_config)
        dataset = pd.read_parquet(get_data_path(common_config["name"], "raw"))
        # Train partition
        try:
            stepshifter_model_calib = pd.read_pickle(get_artifacts_path(common_config["name"], "calib"))
        except:
            stepshifter_model_calib = stepshift_training(common_config, "calib", model, dataset)
            stepshifter_model_calib.save(get_artifacts_path(common_config["name"], "calib"))

        # Test partition
        try:
            stepshifter_model_test = pd.read_pickle(get_artifacts_path(common_config["name"], "test"))
        except:
            stepshifter_model_test = stepshift_training(common_config, "test", model, dataset)
            stepshifter_model_test.save(get_artifacts_path(common_config["name"], "test"))

        # Future partition
        try:
            stepshifter_model_future = pd.read_pickle(get_artifacts_path(common_config["name"], "forecast"))
        except:
            stepshifter_model_future = stepshift_training(common_config, "forecast", model, dataset)
            stepshifter_model_future.save(get_artifacts_path(common_config["name"], "forecast")) 


def stepshift_training(common_config, partition_name, model, dataset):
    steps = common_config["steps"]
    target = common_config["depvar"]
    partition = DataPartitioner({partition_name: common_config[f"{partition_name}_partitioner_dict"]})
    stepshifter_def = StepshiftedModels(model, steps, target)
    stepshifter_model = ViewsRun(partition, stepshifter_def)
    stepshifter_model.fit(partition_name, "train", dataset)
    return stepshifter_model