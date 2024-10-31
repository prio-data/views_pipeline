from datetime import datetime
import pandas as pd
import pickle
import logging  
from pathlib import Path
from model_path import ModelPath
from ensemble_path import EnsemblePath
from set_partition import get_partitioner_dict
from utils_log_files import create_log_file, read_log_file
from utils_outputs import save_predictions
from utils_run import get_standardized_df, get_aggregated_df, get_single_model_config
from utils_artifacts import get_latest_model_artifact

logger = logging.getLogger(__name__)


def forecast_ensemble(config):
    ensemble_path = EnsemblePath(config["name"])
    path_generated_e = ensemble_path.data_generated
    run_type = config["run_type"]
    steps = config["steps"]
    dfs = []
    timestamp = ""

    for model_name in config["models"]:
        logger.info(f"Forecasting single model {model_name}...")
        model_path = ModelPath(model_name)    
        path_raw = model_path.data_raw
        path_generated = model_path.data_generated
        path_artifacts = model_path.artifacts
        path_artifact = get_latest_model_artifact(path_artifacts, run_type)

        ts = path_artifact.stem[-15:]
        timestamp += model_name + ts + "_"

        pkl_path = f"{path_generated}/predictions_{steps[-1]}_{run_type}_{ts}.pkl"
        if Path(pkl_path).exists():
            logger.info(f"Loading existing {run_type} predictions from {pkl_path}")
            with open(pkl_path, "rb") as file:
                df = pickle.load(file)
        else:
            logger.info(f"No existing {run_type} predictions found. Generating new {run_type} predictions...")
            model_config = get_single_model_config(model_name)
            model_config["timestamp"] = ts
            model_config["run_type"] = run_type
            df_viewser = pd.read_pickle(path_raw / f"{run_type}_viewser_df.pkl")

            try:
                stepshift_model = pd.read_pickle(path_artifact)
            except FileNotFoundError:
                logger.exception(f"Model artifact not found at {path_artifact}")

            partition = get_partitioner_dict(run_type)["predict"]
            df = stepshift_model.future_point_predict(partition[0]-1, df_viewser, keep_specific=True)
            df = get_standardized_df(df, model_config)

            data_generation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            date_fetch_timestamp = read_log_file(path_raw / f"{run_type}_data_fetch_log.txt").get("Data Fetch Timestamp", None)
            save_predictions(df, path_generated, model_config)
            create_log_file(path_generated, model_config, ts, data_generation_timestamp, date_fetch_timestamp)

        dfs.append(df)

    df_prediction = get_aggregated_df(dfs, config["aggregation"])
    data_generation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Timestamp of single models is more important than ensemble model timestamp
    config["timestamp"] = timestamp[:-1]
    save_predictions(df_prediction, path_generated_e, config)

    # How to define an ensemble model timestamp? Currently set as data_generation_timestamp.

    create_log_file(path_generated_e, config, data_generation_timestamp, data_generation_timestamp, date_fetch_timestamp=None,
                    model_type="ensemble", models=config["models"])
    