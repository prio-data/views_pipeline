from pathlib import Path
import logging
logging.basicConfig(filename='../../run.log', encoding='utf-8', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
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