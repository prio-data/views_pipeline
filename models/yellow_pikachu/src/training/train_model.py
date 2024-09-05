from datetime import datetime
import pandas as pd
from pathlib import Path
PATH = Path(__file__)
from set_path import setup_project_paths, setup_data_paths, setup_artifacts_paths
setup_project_paths(PATH)

from utils import create_log_file
from set_partition import get_partitioner_dict
from stepshift.views import StepshiftedModels
from views_forecasts.extensions import *
from views_partitioning.data_partitioner import DataPartitioner
from views_stepshift.run import ViewsRun


def train_model_artifact(config, model):
    # print(config)
    PATH_RAW, _, PATH_GENERATED = setup_data_paths(PATH)
    PATH_ARTIFACTS = setup_artifacts_paths(PATH)
    run_type = config['run_type']
    df_viewser = pd.read_pickle(PATH_RAW / f"{run_type}_viewser_df.pkl")

    stepshift_model = stepshift_training(config, run_type, model, df_viewser)
    if not config["sweep"]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_filename = f"{run_type}_model_{timestamp}.pkl"
        stepshift_model.save(PATH_ARTIFACTS / model_filename)
        create_log_file(PATH_GENERATED, config, timestamp)
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
