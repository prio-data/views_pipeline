import logging
from views_pipeline.managers.path_manager import ModelPath

logger = logging.getLogger(__name__)


def read_log_file(log_file_path):
    """
    Reads the log file and returns a dictionary with the relevant information.

    Args:

    - log_file_path (str or Path): The path to the log file.

    Returns:
    - dict: A dictionary containing the model name, model timestamp, data generation timestamp, and data fetch timestamp.
    """

    log_data = {}
    with open(log_file_path, "r") as file:
        for line in file:
            line = line.strip()

            # Skip blank lines
            if not line:
                continue
            else:
                key, value = line.split(": ", 1)
                # There are duplicated keys for ensemble models, but it's not a problem bc these keys are not used
                log_data[key] = value

    return log_data
    

def create_data_fetch_log_file(path_raw, 
                              run_type,
                              model_name,
                              data_fetch_timestamp):
    """
    Creates a log file in the specified single model folder with details about the data fetch.

    Args:
    - path_raw (Path): The path to the folder where the log file will be created.
    - run_type (str): The type of run.
    - model_name (str): The name of the model.
    - data_fetch_timestamp (str): The timestamp when the raw data used was fetched from VIEWS.
    """
    
    data_fetch_log_file_path = f"{path_raw}/{run_type}_data_fetch_log.txt"

    with open(data_fetch_log_file_path, "w") as log_file:
        log_file.write(f"Single Model Name: {model_name}\n")
        log_file.write(f"Data Fetch Timestamp: {data_fetch_timestamp}\n\n")

    logger.info(f"Data fetch log file created at {data_fetch_log_file_path}")


def create_specific_log_file(path_generated,
                    run_type,
                    model_name,
                    deployment_status,
                    model_timestamp,
                    data_generation_timestamp,
                    data_fetch_timestamp,
                    model_type="single",
                    mode="w",):
    """
    Creates a log file in the specified model folder with details about the generated data.

    Args:
    - path_generated (Path): The path to the folder where the log file will be created.
    - run_type (str): The type of run
    - model_name (str): The name of the model.
    - deployment_status (str): The status of the deployment.
    - model_timestamp (str): The timestamp when the model was trained.
    - data_generation_timestamp (str): The timestamp when the data was generated.
    - data_fetch_timestamp (str, optional): The timestamp when the raw data used was fetched from VIEWS.
    - model_type (str, optional): The type of model. Default is "single".
    - mode (str, optional): The mode in which the file will be opened. Default is "w".
    """

    log_file_path = f"{path_generated}/{run_type}_log.txt"

    # Capitalize the first letter of the model type
    model_type = model_type[0].upper() + model_type[1:]

    with open(log_file_path, mode) as log_file:
        log_file.write(f"{model_type} Model Name: {model_name}\n")
        log_file.write(f"{model_type} Model Timestamp: {model_timestamp}\n")
        log_file.write(f"Data Generation Timestamp: {data_generation_timestamp}\n")
        log_file.write(f"Data Fetch Timestamp: {data_fetch_timestamp}\n")
        log_file.write(f"Deployment Status: {deployment_status}\n\n")


def create_log_file(path_generated,
                    model_config,
                    model_timestamp,
                    data_generation_timestamp,
                    data_fetch_timestamp,
                    model_type="single",
                    models=None):
    
    run_type = model_config["run_type"]
    model_name = model_config["name"]
    deployment_status = model_config["deployment_status"]
    
    create_specific_log_file(path_generated, run_type, model_name, deployment_status,
                    model_timestamp, data_generation_timestamp, data_fetch_timestamp, model_type)
    if models:
        for m_name in models:
            model_path = ModelPath(m_name)
            model_path_generated = model_path.data_generated
            log_data = read_log_file(model_path_generated / f"{run_type}_log.txt")
            create_specific_log_file(path_generated, run_type, m_name, log_data["Deployment Status"], 
                                     log_data["Single Model Timestamp"], log_data["Data Generation Timestamp"], log_data["Data Fetch Timestamp"], mode="a")
    
    logger.info(f"Log file created at {path_generated}/{run_type}_log.txt")
        