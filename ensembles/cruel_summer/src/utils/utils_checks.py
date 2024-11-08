from datetime import datetime
import logging
from pathlib import Path
from model_path import ModelPath
from utils_log_files import read_log_file
from utils_run import get_single_model_config

logger = logging.getLogger(__name__)


def check_model_config(model_config, config):
    """
    Checks if devpar and level of the single model matches the ensemble model using config files.

    Args:
    - model_config (dict): The configuration dictionary containing the model details.
    - config (dict): The configuration dictionary containing the ensemble details.

    Returns:
    - bool: True if all conditions are met, False otherwise.
    """

    if model_config["depvar"] != config["depvar"]:
        logger.error(f"Model {model_config['name']} target variable {model_config['depvar']} does not match the ensemble target variable {config['depvar']}. Exiting.")
        return False
    
    if model_config["level"] != config["level"]:
        logger.error(f"Model {model_config['name']} level {model_config['level']} does not match the ensemble level {config['level']}. Exiting.")
        return False

    return True


def check_model_conditions(path_generated, run_type):
    """
    Checks if the single model meets the required conditions based on the log file.

    Args:
    - model_folder (str): The path to the model-specific folder containing the log file.
    - config (dict): The configuration dictionary containing the model details.

    Returns:
    - bool: True if all conditions are met, False otherwise.
    """
    
    log_file_path = Path(path_generated) / f"{run_type}_log.txt"
    try:
        log_data = read_log_file(log_file_path)
    except Exception as e:
        logger.error(f"Error reading log file: {e}")
        return False

    current_time = datetime.now()
    current_year = current_time.year
    current_month = current_time.month

    # Extract from log data
    model_name = log_data["Single Model Name"]
    model_timestamp = datetime.strptime(log_data["Single Model Timestamp"], "%Y%m%d_%H%M%S")
    data_generation_timestamp = None if log_data["Data Generation Timestamp"] == "None" else (
        datetime.strptime(log_data["Data Generation Timestamp"], "%Y%m%d_%H%M%S"))

    data_fetch_timestamp = None if log_data["Data Fetch Timestamp"] == "None" else (
        datetime.strptime(log_data["Data Fetch Timestamp"], "%Y%m%d_%H%M%S"))

    # Condition 1: Model trained in the current year after July
    if current_month >= 7:
        if not (model_timestamp.year == current_year and model_timestamp.month >= 7):
            logger.error(f"Model {model_name} was trained in {model_timestamp.year}_{model_timestamp.month}. "
                         f"Please use the latest model that is trained after {current_year}_07. Exiting.")
            return False
    elif current_month < 7:
        if not (
                (model_timestamp.year == current_year - 1 and model_timestamp.month >= 7) or
                (model_timestamp.year == current_year and model_timestamp.month < 7)
        ):
            logger.error(f"Model {model_name} was trained in {model_timestamp.year}_{model_timestamp.month}. "
                         f"Please use the latest model that is trained after {current_year - 1}_07. Exiting.")
            return False

    # Condition 2: Data generated in the current month
    if data_generation_timestamp and not (
            data_generation_timestamp.year == current_year and data_generation_timestamp.month == current_month):
        logger.error(f"Data for model {model_name} was not generated in the current month. Exiting.")
        return False

    # Condition 3: Raw data fetched in the current month
    if data_fetch_timestamp and not (
            data_fetch_timestamp.year == current_year and data_fetch_timestamp.month == current_month):
        logger.error(f"Raw data for model {model_name} was not fetched in the current month. Exiting.")
        return False

    return True


def check_model_deployment_status(path_generated, run_type, deployment_status):
    """
    Checks if the ensemble model meets the required deployment status conditions based on the log file.

    Args:
    - model_folder (str): The path to the model-specific folder containing the log file.

    Returns:
    - bool: True if all conditions are met, False otherwise.
    """

    log_file_path = Path(path_generated) / f"{run_type}_log.txt"
    try:
        log_data = read_log_file(log_file_path)
    except Exception as e:
        logger.error(f"Error reading log file: {e}. Exiting.")
        return False

    model_name = log_data["Single Model Name"]
    model_dp_status = log_data["Deployment Status"]

    # More check conditions can be added here
    if model_dp_status == "Deployed" and deployment_status != "Deployed":
        logger.error(f"Model {model_name} deployment status is deployed "
                     f"but the ensemble is not. Exiting.")
        return False

    return True


def ensemble_model_check(config):
    """
    Performs the ensemble model check based on the log files of individual models.

    Args:
    - model_folders (list of str): A list of paths to model-specific folders containing log files.

    Returns:
    - None: Shuts down if conditions are not met; proceeds otherwise.
    """

    for model_name in config["models"]:
        model_path = ModelPath(model_name)
        path_generated = model_path.data_generated
        model_config = get_single_model_config(model_name)

        if (
                (not check_model_config(model_config, config)) or
                (not check_model_conditions(path_generated, config["run_type"])) or
                (not check_model_deployment_status(path_generated, config["run_type"], config["deployment_status"]))
        ):
            exit(1)  # Shut down if conditions are not met
    logger.info(f"Model {config['name']} meets the required conditions.")
