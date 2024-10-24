from pathlib import Path
import logging

logger = logging.getLogger(__name__)


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
