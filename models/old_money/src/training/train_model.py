from datetime import datetime
import pandas as pd
from model_path import ModelPath
from utils_log_files import create_log_file
from utils_run import get_model
from set_partition import get_partitioner_dict
from views_forecasts.extensions import *


def train_model_artifact(config):
    # print(config)
    model_path = ModelPath(config["name"], validate=False)
    path_raw  = model_path.data_raw
    path_generated = model_path.data_generated
    path_artifacts = model_path.artifacts
    run_type = config["run_type"]
    df_viewser = pd.read_pickle(path_raw / f"{run_type}_viewser_df.pkl")

    stepshift_model = stepshift_training(config, run_type, df_viewser)
    if not config["sweep"]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_filename = f"{run_type}_model_{timestamp}.pkl"
        stepshift_model.save(path_artifacts / model_filename)
        create_log_file(path_generated, config, timestamp)
    return stepshift_model


def stepshift_training(config, partition_name, dataset):
    partitioner_dict = get_partitioner_dict(partition_name)
    stepshift_model = get_model(config, partitioner_dict)
    stepshift_model.fit(dataset)
    return stepshift_model
