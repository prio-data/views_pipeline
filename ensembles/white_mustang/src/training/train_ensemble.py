import sys
import logging
from datetime import datetime

from pathlib import Path
PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths
setup_project_paths(PATH)

from model_path import ModelPath
from utils_log_files import create_log_file
from utils_run import get_model, get_single_model_config
from set_partition import get_partitioner_dict
from stepshift.views import StepshiftedModels
from views_forecasts.extensions import *
from views_partitioning.data_partitioner import DataPartitioner
from views_stepshift.run import ViewsRun

logger = logging.getLogger(__name__)       


def train_ensemble(config):
    # print(config)
    run_type = config["run_type"]

    for model_name in config["models"]:
        logger.info(f"Running single model {model_name}...")
        model_path = ModelPath(model_name, validate=False)

        df_viewser = pd.read_pickle(model_path.data_raw / f"{run_type}_viewser_df.pkl")
        model_config = get_single_model_config(model_name)
        model_config["run_type"] = run_type
        stepshift_model = stepshift_training(model_config, run_type, get_model(model_config), df_viewser)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_filename = f"{run_type}_model_{timestamp}.pkl"
        stepshift_model.save(model_path.artifacts / model_filename)
        create_log_file(model_path.data_generated, model_config, timestamp)
        


def stepshift_training(config, partition_name, model, dataset):
    steps = config["steps"]
    target = config["depvar"]
    partitioner_dict = get_partitioner_dict(partition_name)
    partition = DataPartitioner({partition_name: partitioner_dict})
    stepshift_def = StepshiftedModels(model, steps, target)
    stepshift_model = ViewsRun(partition, stepshift_def)
    stepshift_model.fit(partition_name, "train", dataset)
    return stepshift_model
