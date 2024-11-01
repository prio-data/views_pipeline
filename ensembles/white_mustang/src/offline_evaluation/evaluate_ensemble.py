import logging
import pickle
import pandas as pd
import datetime
from pathlib import Path
from model_path import ModelPath
from ensemble_path import EnsemblePath
from utils_log_files import create_log_file, read_log_file
from utils_outputs import save_model_outputs, save_predictions
from utils_run import get_standardized_df, get_aggregated_df, get_single_model_config
from utils_evaluation_metrics import generate_metric_dict
from utils_model_outputs import generate_output_dict
from utils_artifacts import get_latest_model_artifact
from utils_wandb import log_wandb_log_dict
from views_forecasts.extensions import *

logger = logging.getLogger(__name__)


def evaluate_ensemble(config):
    ensemble_path = EnsemblePath(config["name"])
    path_generated_e = ensemble_path.data_generated
    run_type = config["run_type"]
    steps = config["steps"]
    dfs = []
    timestamp = ""

    for model_name in config["models"]:
        logger.info(f"Evaluating single model {model_name}...")
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

            df = stepshift_model.predict(run_type, "predict", df_viewser)
            df = get_standardized_df(df, model_config)
            data_generation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            date_fetch_timestamp = read_log_file(path_raw / f"{run_type}_data_fetch_log.txt").get("Data Fetch Timestamp", None)

            _, df_output = generate_output_dict(df, model_config)
            evaluation, df_evaluation = generate_metric_dict(df, model_config)
            save_model_outputs(df_evaluation, df_output, path_generated, model_config)
            save_predictions(df, path_generated, model_config)
            create_log_file(path_generated, model_config, ts, data_generation_timestamp, date_fetch_timestamp)

        dfs.append(df)

    df_agg = get_aggregated_df(dfs, config["aggregation"])
    data_generation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    

    _, df_output = generate_output_dict(df_agg, config)
    evaluation, df_evaluation = generate_metric_dict(df_agg, config)
    log_wandb_log_dict(config, evaluation)

    # Timestamp of single models is more important than ensemble model timestamp
    config["timestamp"] = timestamp[:-1]
    save_model_outputs(df_evaluation, df_output, path_generated_e, config)
    save_predictions(df_agg, path_generated_e, config)

    # How to define an ensemble model timestamp? Currently set as data_generation_timestamp.

    create_log_file(path_generated_e, config, data_generation_timestamp, data_generation_timestamp, data_fetch_timestamp=None,
                    model_type="ensemble", models=config["models"])
