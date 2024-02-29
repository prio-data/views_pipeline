from pathlib import Path
import pandas as pd

import sys
src_path = f"{Path(__file__).parent.parent}"
sys.path.append(str(src_path)+"/utils")

# Remove this part after packaging views_stepshift
current_file_path = Path(__file__).resolve()
root_path = current_file_path.parent.parent.parent.parent.parent
sys.path.append(str(root_path))

from xgboost import XGBRegressor

from utils import get_artifacts_path, get_data_path
from views_partitioning.data_partitioner import DataPartitioner
from views_forecasts.extensions import *
from stepshift.views import StepshiftedModels
from views_stepshift.run import ViewsRun


def train(common_config, para_config):
    # suffix = ""
    # if common_config["sweep"]:
    #     for key, value in para_config.items():
    #         suffix += f"_{key}_{value}"
    
    print("Training...")
    model = globals()[common_config["algorithm"]](**para_config)
    dataset = pd.read_parquet(get_data_path("raw"))

    if not common_config["sweep"]:
        # Train partition
        try:
            stepshifter_model_train = pd.read_pickle(get_artifacts_path("train"))
        except:
            stepshifter_model_train = stepshift_training(common_config, "train", model, dataset)
            stepshifter_model_train.save(get_artifacts_path("train"))

        # Test partition
        try:
            stepshifter_model_test = pd.read_pickle(get_artifacts_path("test"))
        except:
            stepshifter_model_test = stepshift_training(common_config, "test", model, dataset)
            stepshifter_model_test.save(get_artifacts_path("test"))

        # Future partition
        try:
            stepshifter_model_future = pd.read_pickle(get_artifacts_path("future"))
        except:
            stepshifter_model_future = stepshift_training(common_config, "future", model, dataset)
            stepshifter_model_future.save(get_artifacts_path("future"))

    else:
        stepshifter_model_train = stepshift_training(common_config, "train", model, dataset)
        stepshifter_model_test = stepshift_training(common_config, "test", model, dataset)
        stepshifter_model_future = stepshift_training(common_config, "future", model, dataset)


def stepshift_training(common_config, partition_name, model, dataset):
    steps = common_config["steps"]
    target = common_config["depvar"]
    partition = DataPartitioner({partition_name: common_config[f"{partition_name}_partitioner_dict"]})
    stepshifter_def = StepshiftedModels(model, steps, target)
    stepshifter_model = ViewsRun(partition, stepshifter_def)
    stepshifter_model.fit(partition_name, "train", dataset)
    return stepshifter_model