from datetime import datetime
import pandas as pd
from pathlib import Path
PATH = Path(__file__) 
from set_path import setup_project_paths, setup_data_paths, setup_artifacts_paths
setup_project_paths(PATH)

from utils import create_log_file
from set_partition import get_partitioner_dict
from views_forecasts.extensions import *
from views_stepshifter_darts.stepshifter_darts import StepshifterModel


def train_model_artifact(config):
    # print(config)
    PATH_RAW, _, _ = setup_data_paths(PATH)
    PATH_ARTIFACTS = setup_artifacts_paths(PATH)
    run_type = config['run_type']
    df_viewser = pd.read_pickle(PATH_RAW / f"{run_type}_viewser_df.pkl")

    stepshift_model = stepshift_training(config, run_type, df_viewser)
    if not config["sweep"]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_filename = f"{run_type}_model_{timestamp}.pkl"
        stepshift_model.save(PATH_ARTIFACTS / model_filename)
        create_log_file(PATH_ARTIFACTS, config, timestamp)
    return stepshift_model


def stepshift_training(config, partition_name, dataset):
    partitioner_dict = get_partitioner_dict(partition_name)
    stepshift_model = StepshifterModel(config, partitioner_dict)
    stepshift_model.fit(dataset)
    return stepshift_model
