import logging
import logging.config
import yaml
import os
from pathlib import Path
from views_pipeline.managers.path_manager import ModelPath
from global_cache import GlobalCache

_split_by_model = True # Only works for lavender_haze

def ensure_log_directory(log_path: str) -> None:
    """
    Ensure the log directory exists for file-based logging handlers.

    Parameters:
    log_path (str): The full path to the log file for which the directory should be verified.
    """
    log_dir = os.path.dirname(log_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)


def setup_logging(
    default_level: int = logging.INFO, env_key: str = 'LOG_CONFIG') -> logging.Logger:

    """
    Setup the logging configuration from a YAML file and return the root logger.

    Parameters:
    default_level (int): The default logging level if the configuration file is not found
                         or cannot be loaded. Default is logging.INFO.
                         
    env_key (str): Environment variablei key to override the default path to the logging
                   configuration file. Default is 'LOG_CONFIG'.

    Returns:
    logging.Logger: The root logger configured based on the loaded configuration.

    Example Usage:
    >>> logger = setup_logging()
    >>> logger.info("Logging setup complete.")
    """

    CONFIG_LOGS_PATH = ModelPath.get_common_configs() / 'config_log.yaml'
    if _split_by_model:
        try:
            COMMON_LOGS_PATH = ModelPath.get_common_logs() / GlobalCache["current_model"]
        except:
            # Pretection in case model name is not available or GlobalCache fails.
            COMMON_LOGS_PATH = ModelPath.get_common_logs()
    else:
        COMMON_LOGS_PATH = ModelPath.get_common_logs()

    # Load YAML configuration
    path = os.getenv(env_key, CONFIG_LOGS_PATH)

    if os.path.exists(path):
        try:
            with open(path, 'rt') as f:
                config = yaml.safe_load(f.read())
            
            # Replace placeholder with actual log directory path
            for handler in config.get("handlers", {}).values():
                if "filename" in handler and "{LOG_PATH}" in handler["filename"]:
                    handler["filename"] = handler["filename"].replace("{LOG_PATH}", str(COMMON_LOGS_PATH))
                    ensure_log_directory(handler["filename"])
            
            # Apply logging configuration
            logging.config.dictConfig(config)

        except Exception as e:
            logging.basicConfig(level=default_level)
            logging.error(f"Failed to load logging configuration from {path}. Using basic configuration. Error: {e}")
    else:
        logging.basicConfig(level=default_level)
        logging.warning(f"Logging configuration file not found at {path}. Using basic configuration.")
    
    return logging.getLogger()

