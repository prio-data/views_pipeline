import logging
import logging.config
import yaml
import os
from pathlib import Path
from model_path import ModelPath
from global_cache import GlobalCache
# SINCE WE ARE IN COMMON_UTILS, WE CAN JUST USE THE MODEL_PATH OBJECT HERE...------------------------------
# def get_config_log_path() -> Path:
#     """
#     Retrieves the path to the 'config_log.yaml' file within the 'views_pipeline' directory.

#     This function identifies the 'views_pipeline' directory within the path of the current file,
#     constructs a new path up to and including this directory, and then appends the relative path
#     to the 'config_log.yaml' file. If the 'views_pipeline' directory or the 'config_log.yaml' file
#     is not found, it raises a ValueError.

#     Returns:
#         pathlib.Path: The path to the 'config_log.yaml' file.

#     Raises:
#         ValueError: If the 'views_pipeline' directory or the 'config_log.yaml' file is not found in the provided path.
#     """
#     PATH = Path(__file__)
#     if 'views_pipeline' in PATH.parts:
#         PATH_ROOT = Path(*PATH.parts[:PATH.parts.index('views_pipeline') + 1])
#         PATH_CONFIG_LOG = PATH_ROOT / 'common_configs/config_log.yaml'
#         if not PATH_CONFIG_LOG.exists():
#             raise ValueError("The 'config_log.yaml' file was not found in the provided path.")
#     else:
#         raise ValueError("The 'views_pipeline' directory was not found in the provided path.")
#     return PATH_CONFIG_LOG
# # --------------------------------------------------------------------------------------------------------------


# # SINCE WE ARE IN COMMON_UTILS, WE CAN JUST USE THE MODEL_PATH OBJECT HERE...-----------------------------------
# def get_common_logs_path() -> Path:
#     """
#     Retrieve the absolute path to the 'common_logs' directory within the 'views_pipeline' structure.

#     This function locates the 'views_pipeline' directory in the current file's path, then constructs
#     a new path to the 'common_logs' directory. If 'common_logs' or 'views_pipeline' directories are not found,
#     it raises a ValueError.

#     Returns:
#         pathlib.Path: Absolute path to the 'common_logs' directory.

#     Raises:
#         ValueError: If the 'views_pipeline' or 'common_logs' directory is not found.
#     """
#     PATH = Path(__file__)
#     if 'views_pipeline' in PATH.parts:
#         PATH_ROOT = Path(*PATH.parts[:PATH.parts.index('views_pipeline') + 1])
#         PATH_COMMON_LOGS = PATH_ROOT / 'common_logs'
#         if not PATH_COMMON_LOGS.exists():
#             raise ValueError("The 'common_logs' directory was not found in the provided path.")
#     else:
#         raise ValueError("The 'views_pipeline' directory was not found in the provided path.")
#     return PATH_COMMON_LOGS
# # ------------------------------------------------------------------------------------------------------------

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





## Old version
#def setup_logging(log_file: str, log_level=logging.INFO):
#    """
#    Sets up logging to both a specified file and the terminal (console).
#
#    Args:
#        log_file (str): The file where logs should be written.
#        log_level (int): The logging level. Default is logging.INFO.
#    """
#
#    basic_logger = logging.getLogger()
#    basic_logger.setLevel(log_level)
#
#    file_handler = logging.FileHandler(log_file)
#    console_handler = logging.StreamHandler()
#
#    file_handler.setLevel(log_level)
#    console_handler.setLevel(log_level)
#
#    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#    file_handler.setFormatter(formatter)
#    console_handler.setFormatter(formatter)
#
#    # Clear previous handlers if they exist
#    if basic_logger.hasHandlers():
#        basic_logger.handlers.clear()
#
#    basic_logger.addHandler(file_handler)
#    basic_logger.addHandler(console_handler)
#
#    return basic_logger
#