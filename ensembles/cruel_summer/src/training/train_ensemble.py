import logging
from datetime import datetime
from model_path import ModelPath
from set_partition import get_partitioner_dict
from utils_log_files import create_log_file
from utils_run import get_model, get_single_model_config
from views_stepshift.run import ViewsRun
from stepshift.views import StepshiftedModels
from views_forecasts.extensions import *
from views_partitioning.data_partitioner import DataPartitioner

logger = logging.getLogger(__name__)   


def train_ensemble(config):
    # print(config)
    run_type = config["run_type"]

    for model_name in config["models"]:
        logger.info(f"Training single model {model_name}...")
        
        model_path = ModelPath(model_name, validate=False)
        path_raw  = model_path.data_raw
        path_generated = model_path.data_generated
        path_artifacts = model_path.artifacts

        df_viewser = pd.read_pickle(path_raw / f"{run_type}_viewser_df.pkl")
        model_config = get_single_model_config(model_name)
        model_config["run_type"] = run_type
        stepshift_model = stepshift_training(model_config, run_type, get_model(model_config), df_viewser)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_filename = f"{run_type}_model_{timestamp}.pkl"
        stepshift_model.save(path_artifacts / model_filename)
        create_log_file(path_generated, model_config, timestamp)


def stepshift_training(config, partition_name, model, dataset):
    steps = config["steps"]
    target = config["depvar"]
    partitioner_dict = get_partitioner_dict(partition_name)
    partition = DataPartitioner({partition_name: partitioner_dict})
    stepshift_def = StepshiftedModels(model, steps, target)
    stepshift_model = ViewsRun(partition, stepshift_def)
    stepshift_model.fit(partition_name, "train", dataset)
    return stepshift_model