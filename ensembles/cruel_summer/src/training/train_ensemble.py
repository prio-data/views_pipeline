import logging
import pandas as pd
from datetime import datetime
from model_path import ModelPath
from set_partition import get_partitioner_dict
from utils_log_files import create_log_file, read_log_file
from utils_run import get_model, get_single_model_config
from get_data import get_data
from views_forecasts.extensions import *

logger = logging.getLogger(__name__)   


def train_ensemble(config):
    # print(config)
    run_type = config["run_type"]

    for model_name in config["models"]:
        logger.info(f"Training single model {model_name}...")
        model_path = ModelPath(model_name)
        path_raw  = model_path.data_raw
        path_generated = model_path.data_generated
        path_artifacts = model_path.artifacts

        try:
            df_viewser = pd.read_pickle(path_raw / f"{run_type}_viewser_df.pkl")
        except FileNotFoundError:
            logger.warning(f"Data not found at {path_raw / f'{run_type}_viewser_df.pkl'}. Getting data...")
            get_data(model_name, run_type, config["saved"], False)
            df_viewser = pd.read_pickle(path_raw / f"{run_type}_viewser_df.pkl")

        model_config = get_single_model_config(model_name)
        model_config["run_type"] = run_type
        model_config["sweep"] = config["sweep"]
        stepshift_model = stepshift_training(model_config, run_type, df_viewser)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_filename = f"{run_type}_model_{timestamp}.pkl"
        stepshift_model.save(path_artifacts / model_filename)
        data_fetch_timestamp = read_log_file(path_raw / f"{run_type}_data_fetch_log.txt").get("Data Fetch Timestamp", None)
        create_log_file(path_generated, config, timestamp, None, data_fetch_timestamp)


def stepshift_training(config, partition_name, dataset):
    partitioner_dict = get_partitioner_dict(partition_name)
    stepshift_model = get_model(config, partitioner_dict)
    stepshift_model.fit(dataset)
    return stepshift_model