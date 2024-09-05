import sys
import numpy as np
import pickle

import logging
logging.basicConfig(filename='../../run.log', encoding='utf-8', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from pathlib import Path
PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths
setup_project_paths(PATH)

from views_forecasts.extensions import *


def create_log_file(PATH_GENERATED,
                    config,
                    model_timestamp,
                    data_generation_timestamp=None,
                    data_fetch_timestamp=None):
    """
    Creates a log file in the specified model-specific folder with details about the generated data.

    Args:
    - PATH_GENERATED (Path): The path to the folder where the log file will be created.
    - config (dict): The configuration dictionary containing the model details.
    - model_timestamp (str): The timestamp when the model was trained.
    - data_generation_timestamp (str): The timestamp when the data was generated.
    - data_fetch_timestamp (str, optional): The timestamp when the raw data used was fetched from VIEWS.
    """

    Path(PATH_GENERATED).mkdir(parents=True, exist_ok=True)
    log_file_path = f"{PATH_GENERATED}/{config['run_type']}_log.txt"

    with open(log_file_path, 'w') as log_file:
        log_file.write(f"Model Name: {config['name']}\n")
        log_file.write(f"Model Timestamp: {model_timestamp}\n")
        log_file.write(f"Data Generation Timestamp: {data_generation_timestamp}\n")
        log_file.write(f"Data Fetch Timestamp: {data_fetch_timestamp}\n")
        log_file.write(f"Deployment Status: {config['deployment_status']}\n")

    logger.info(f"Model log file created at: {log_file_path}")


def read_log_file(log_file_path):
    """
    Reads the log file and returns a dictionary with the relevant information.

    Args:
    - log_file_path (str): The path to the log file.

    Returns:
    - dict: A dictionary containing the model name, model timestamp, data generation timestamp, and data fetch timestamp.
    """
    log_data = {}
    with open(log_file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(': ', 1)
            log_data[key] = value

    return log_data


def get_standardized_df(df, config):
    """
    Standardizes the DataFrame of model outputs based on the run type.

    Args:
    - df (pd.DataFrame): The DataFrame of model outputs.
    - config (dict): The configuration dictionary containing the model details.

    Returns:
    - df (pd.DataFrame): The standardized DataFrame of model outputs.
    """
    run_type = config['run_type']
    steps = config['steps']
    depvar = config['depvar']

    # choose the columns to keep based on the run type and replace negative values with 0
    if run_type in ['calibration', 'testing']:
        cols = [depvar] + df.forecasts.prediction_columns
    elif run_type == "forecasting":
        cols = [f'step_pred_{i}' for i in steps]
    df = df.replace([np.inf, -np.inf], 0)[cols]
    df = df.mask(df < 0, 0)

    return df


def get_aggregated_df(dfs, aggregation):
    """
    Aggregates the DataFrames of model outputs based on the specified aggregation method.

    Args:
    - dfs (list of pd.DataFrame): A list of DataFrames of model outputs.
    - aggregation (str): The aggregation method to use (either 'mean' or 'median').

    Returns:
    - df (pd.DataFrame): The aggregated DataFrame of model outputs.
    """
    if aggregation == "mean":
        return pd.concat(dfs).groupby(level=[0, 1]).mean()
    elif aggregation == "median":
        return pd.concat(dfs).groupby(level=[0, 1]).median()
    else:
        logger.error(f"Invalid aggregation: {aggregation}")


def save_model_outputs(df_evaluation, df_output, PATH_GENERATED, config):
    Path(PATH_GENERATED).mkdir(parents=True, exist_ok=True)

    # Save the DataFrame of model outputs
    outputs_path = f'{PATH_GENERATED}/df_output_{config.steps[-1]}_{config.run_type}_{config.timestamp}.pkl'
    with open(outputs_path, 'wb') as file:
        pickle.dump(df_output, file)
    logger.info(f"Model outputs saved at: {outputs_path}")

    # Save the DataFrame of evaluation metrics
    evaluation_path = f'{PATH_GENERATED}/df_evaluation_{config.steps[-1]}_{config.run_type}_{config.timestamp}.pkl'
    with open(evaluation_path, 'wb') as file:
        pickle.dump(df_evaluation, file)
    logger.info(f"Evaluation metrics saved at: {evaluation_path}")


def save_predictions(df_predictions, PATH_GENERATED, config):
    Path(PATH_GENERATED).mkdir(parents=True, exist_ok=True)

    predictions_path = f"{PATH_GENERATED}/predictions_{config['steps'][-1]}_{config['run_type']}_{config['timestamp']}.pkl"
    with open(predictions_path, 'wb') as file:
        pickle.dump(df_predictions, file)
    logger.info(f"Predictions saved at: {predictions_path}")


def update_config(hp_config, meta_config, dp_config, args):
    config = hp_config.copy()
    config['run_type'] = args.run_type
    config['aggregation'] = args.aggregation
    config['name'] = meta_config['name']
    config['models'] = meta_config['models']
    config['depvar'] = meta_config['depvar']
    config['deployment_status'] = dp_config['deployment_status']

    return config