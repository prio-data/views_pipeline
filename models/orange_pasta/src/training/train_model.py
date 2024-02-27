from pathlib import Path

# Remove this part after packaging views_stepshift
import sys
current_file_path = Path(__file__).resolve()
root_path = current_file_path.parent.parent.parent.parent.parent
sys.path.append(str(root_path))


from lightgbm import LGBMRegressor


from views_partitioning.data_partitioner import DataPartitioner
from views_forecasts.extensions import *
from stepshift.views import StepshiftedModels
from views_stepshift.run import ViewsRun
from ..dataloaders.get_data import *


def train(common_config, para_config):
    # suffix = ""
    # if common_config["sweep"]:
    #     for key, value in para_config.items():
    #         suffix += f"_{key}_{value}"
    
    print("Training...")
    model = globals()[common_config["algorithm"]](**para_config)
    dataset = pd.read_parquet(f"{Path(__file__).parent.parent.parent}/data/raw/raw.parquet")

    if not common_config["sweep"]:
        # Train partition
        try:
            stepshifter_model_train = pd.read_pickle(f"{Path(__file__).parent.parent.parent}/artifacts/model_train_partition.pkl")
        except:
            stepshifter_model_train = stepshift_training(common_config, "train", model, dataset)
            stepshifter_model_train.save(f"{Path(__file__).parent.parent.parent}/artifacts/model_train_partition.pkl")

        # Test partition
        try:
            stepshifter_model_test = pd.read_pickle(f"{Path(__file__).parent.parent.parent}/artifacts/model_test_partition.pkl")
        except:
            stepshifter_model_test = stepshift_training(common_config, "test", model, dataset)
            stepshifter_model_test.save(f"{Path(__file__).parent.parent.parent}/artifacts/model_test_partition.pkl")

        # Future partition
        try:
            stepshifter_model_future = pd.read_pickle(f"{Path(__file__).parent.parent.parent}/artifacts/model_forecasting.pkl")
        except:
            stepshifter_model_future = stepshift_training(common_config, "future", model, dataset)
            stepshifter_model_future.save(f"{Path(__file__).parent.parent.parent}/artifacts/model_forecasting.pkl")

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