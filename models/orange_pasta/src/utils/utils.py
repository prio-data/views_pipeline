import sys
import numpy as np
from darts.models import LightGBMModel, XGBModel
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

from hurdle_model import HurdleRegression
from set_partition import get_partitioner_dict
from views_forecasts.extensions import *


def create_log_file(PATH_GENERATED, config, data_generation_timestamp, data_fetch_timestamp=None):
    """
    Creates a log file in the specified model-specific folder with details about the generated data.

    Args:
    - PATH_GENERATED (Path): The path to the folder where the log file will be created.
    - config (dict): The configuration dictionary containing the model details.
    - data_generation_timestamp (str): The timestamp when the data was generated.
    - data_fetch_timestamp (str, optional): The timestamp when the raw data used was fetched from VIEWS.
    """

    Path(PATH_GENERATED).mkdir(parents=True, exist_ok=True)
    log_file_path = f"{PATH_GENERATED}/{config['run_type']}_log.txt"

    with open(log_file_path, 'w') as log_file:
        log_file.write(f"Model Name: {config['name']}\n")
        log_file.write(f"Model Timestamp: {config['timestamp']}\n")
        log_file.write(f"Data Generation Timestamp: {data_generation_timestamp}\n")
        if data_fetch_timestamp:
            log_file.write(f"Data Fetch Timestamp: {data_fetch_timestamp}\n")
        log_file.write(f"Deployment Status: {config['deployment_status']}\n")

    logger.info(f"Data log file created at: {log_file_path}")


def get_model(config):
    """
    Get the model based on the algorithm specified in the config
    """

    if config["algorithm"] == "HurdleRegression":
        model = HurdleRegression(clf_name=config["model_clf"], reg_name=config["model_reg"],
                                 clf_params=config["parameters"]["clf"], reg_params=config["parameters"]["reg"])
    else:
        parameters = get_parameters(config)
        model = globals()[config["algorithm"]](**parameters)

    return model


def get_parameters(config):
    """
    Get the parameters from the config file.
    If not sweep, then get directly from the config file, otherwise have to remove some parameters.
    """

    if config["sweep"]:
        keys_to_remove = ["algorithm", "depvar", "steps", "sweep", "run_type", "model_cls", "model_reg"]
        parameters = {k: v for k, v in config.items() if k not in keys_to_remove}
    else:
        parameters = config["parameters"]

    return parameters


def get_standardized_df(df, config):
    """
    Standardize the DataFrame based on the run type
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


def save_model_outputs(df_evaluation, df_output, PATH_GENERATED, config):
    Path(PATH_GENERATED).mkdir(parents=True, exist_ok=True)

    # Save the DataFrame of model outputs
    outputs_path = f"{PATH_GENERATED}/df_output_{config['steps'][-1]}_{config['run_type']}_{config['timestamp']}.pkl"
    with open(outputs_path, 'wb') as file:
        pickle.dump(df_output, file)
    logger.info(f"Model outputs saved at: {outputs_path}")

    # Save the DataFrame of evaluation metrics
    evaluation_path = f"{PATH_GENERATED}/df_evaluation_{config['steps'][-1]}_{config['run_type']}_{config['timestamp']}.pkl"
    with open(evaluation_path, 'wb') as file:
        pickle.dump(df_evaluation, file)
    logger.info(f"Evaluation metrics saved at: {evaluation_path}")


def save_predictions(df_predictions, PATH_GENERATED, config):
    Path(PATH_GENERATED).mkdir(parents=True, exist_ok=True)

    predictions_path = f"{PATH_GENERATED}/predictions_{config['steps'][-1]}_{config['run_type']}_{config['timestamp']}.pkl"
    with open(predictions_path, 'wb') as file:
        pickle.dump(df_predictions, file)
    logger.info(f"Predictions saved at: {predictions_path}")


def split_hurdle_parameters(parameters_dict):
    """
    Split the parameters dictionary into two separate dictionaries, one for the
    classification model and one for the regression model.
    """

    cls_dict = {}
    reg_dict = {}

    for key, value in parameters_dict.items():
        if key.startswith('cls_'):
            cls_key = key.replace('cls_', '')
            cls_dict[cls_key] = value
        elif key.startswith('reg_'):
            reg_key = key.replace('reg_', '')
            reg_dict[reg_key] = value

    return cls_dict, reg_dict


def update_config(hp_config, meta_config, dp_config, args):
    config = hp_config.copy()
    config['run_type'] = args.run_type
    config['sweep'] = False
    config['name'] = meta_config['name']
    config['depvar'] = meta_config['depvar']
    config['algorithm'] = meta_config['algorithm']
    if meta_config['algorithm'] == 'HurdleRegression':
        config['model_clf'] = meta_config['model_clf']
        config['model_reg'] = meta_config['model_reg']
    config['deployment_status'] = dp_config['deployment_status']

    return config


def update_sweep_config(sweep_config, args, meta_config):
    sweep_config['parameters']['run_type'] = {'value': args.run_type}
    sweep_config['parameters']['sweep'] = {'value': True}
    sweep_config['parameters']['depvar'] = {'value': meta_config['depvar']}
    sweep_config['parameters']['algorithm'] = {'value': meta_config['algorithm']}
    if meta_config['algorithm'] == 'HurdleRegression':
        sweep_config['parameters']['model_clf'] = {'value': meta_config['model_clf']}
        sweep_config['parameters']['model_reg'] = {'value': meta_config['model_reg']}
