from datetime import datetime
import pandas as pd
import pickle
import logging
from pathlib import Path
from set_path import setup_data_paths, setup_artifacts_paths, setup_root_paths
from set_partition import get_partitioner_dict
from utils_log_files import create_log_file
from utils_outputs import save_predictions
from utils_run import get_standardized_df, get_aggregated_df, get_single_model_config
from utils_artifacts import get_latest_model_artifact

logger = logging.getLogger(__name__)
PATH = Path(__file__)


def forecast_ensemble(config):
    run_type = config["run_type"]
    steps = config["steps"]
    _, _, PATH_GENERATED_E = setup_data_paths(PATH)
    dfs = []
    timestamp = ''

    for model_name in config["models"]:
        logger.info(f"Running single model {model_name}...")

        PATH_MODEL = setup_root_paths(PATH) / "models" / model_name
        PATH_RAW, _, PATH_GENERATED = setup_data_paths(PATH_MODEL)
        PATH_ARTIFACTS = setup_artifacts_paths(PATH_MODEL)
        PATH_ARTIFACT = get_latest_model_artifact(PATH_ARTIFACTS, run_type)

        ts = PATH_ARTIFACT.stem[-15:]
        timestamp += model_name + ts + '_'

        pkl_path = f'{PATH_GENERATED}/predictions_{steps[-1]}_{run_type}_{ts}.pkl'
        if Path(pkl_path).exists():
            logger.info(f"Loading existing {run_type} predictions from {pkl_path}")
            with open(pkl_path, 'rb') as file:
                df = pickle.load(file)
        else:
            logger.info(f"No existing {run_type} predictions found. Generating new {run_type} predictions...")
            model_config = get_single_model_config(model_name)
            model_config["timestamp"] = ts
            model_config["run_type"] = run_type
            df_viewser = pd.read_pickle(PATH_RAW / f"{run_type}_viewser_df.pkl")

            try:
                stepshift_model = pd.read_pickle(PATH_ARTIFACT)
            except FileNotFoundError:
                logger.exception(f"Model artifact not found at {PATH_ARTIFACT}")

            partition = get_partitioner_dict(run_type)['predict']
            df = stepshift_model.future_point_predict(partition[0]-1, df_viewser, keep_specific=True)
            df = get_standardized_df(df, model_config)

            data_generation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_predictions(df, PATH_GENERATED, model_config)
            create_log_file(PATH_GENERATED, model_config, ts, data_generation_timestamp)

        dfs.append(df)

    df_prediction = get_aggregated_df(dfs, config["aggregation"])
    data_generation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # I don't think current timestamp is useful here because timestamp of single models is more important.
    config["timestamp"] = timestamp[:-1]
    save_predictions(df_prediction, PATH_GENERATED_E, config)

    # How to define an ensemble model timestamp? Currently set as data_generation_timestamp.
    create_log_file(PATH_GENERATED_E, config, data_generation_timestamp, data_generation_timestamp, 
                    model_type="ensemble", models=config["models"])
    