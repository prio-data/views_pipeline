import logging


def setup_logging(log_file: str, log_level=logging.INFO):
    """
    Sets up logging to both a specified file and the terminal (console).

    Args:
        log_file (str): The file where logs should be written.
        log_level (int): The logging level. Default is logging.INFO.
    """
    # Create a logger object

    basic_logger = logging.getLogger()
    basic_logger.setLevel(log_level)

    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()

    file_handler.setLevel(log_level)
    console_handler.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Clear previous handlers if they exist
    if basic_logger.hasHandlers():
        basic_logger.handlers.clear()

    basic_logger.addHandler(file_handler)
    basic_logger.addHandler(console_handler)

    return basic_logger
