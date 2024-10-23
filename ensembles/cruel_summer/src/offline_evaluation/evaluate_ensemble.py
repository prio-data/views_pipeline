import logging
import pickle
from pathlib import Path
from set_path import setup_data_paths, setup_artifacts_paths, setup_root_paths
from utils_log_files import create_log_file
from utils_outputs import save_model_outputs, save_predictions
from utils_run import get_standardized_df, get_aggregated_df, get_single_model_config
from utils_evaluation_metrics import generate_metric_dict
from utils_model_outputs import generate_output_dict
from utils_artifacts import get_latest_model_artifact
from utils_wandb import log_wandb_log_dict
from views_forecasts.extensions import *

logger = logging.getLogger(__name__)
PATH = Path(__file__)


def evaluate_ensemble(config):
    run_type = config['run_type']
    steps = config["steps"]
    PATH_MODELS = setup_root_paths(PATH) / "models"
    _, _, PATH_GENERATED_E = setup_data_paths(PATH)
    dfs = []
    timestamp = ''

    for model_name in config["models"]:
        logger.info(f"Running single model {model_name}...")
        PATH_MODEL = PATH_MODELS / model_name
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

            df = stepshift_model.predict(run_type, "predict", df_viewser)
            df = get_standardized_df(df, model_config)
            data_generation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            output, df_output = generate_output_dict(df, model_config)
            evaluation, df_evaluation = generate_metric_dict(df, model_config)
            save_model_outputs(df_evaluation, df_output, PATH_GENERATED, model_config)
            save_predictions(df, PATH_GENERATED, model_config)
            create_log_file(PATH_GENERATED, model_config, ts, data_generation_timestamp)

        dfs.append(df)

    df_agg = get_aggregated_df(dfs, config["aggregation"])
    data_generation_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output, df_output = generate_output_dict(df_agg, config)
    evaluation, df_evaluation = generate_metric_dict(df_agg, config)
    log_wandb_log_dict(config, evaluation)

    # I don't think current timestamp is useful here.
    # Timestamp of single models is more important but how should we register them in ensemble config?
    config["timestamp"] = timestamp[:-1]
    save_model_outputs(df_evaluation, df_output, PATH_GENERATED_E, config)
    save_predictions(df_agg, PATH_GENERATED_E, config)

    # How to define an ensemble model timestamp? Currently set as data_generation_timestamp.
    create_log_file(PATH_GENERATED_E, config, data_generation_timestamp, data_generation_timestamp, 
                    model_type="ensemble", models=config["models"])
