import logging
from pathlib import Path
import sys


PATH = Path(__file__)

def get_path_common_utils():

    if 'views_pipeline' in PATH.parts:

        PATH_ROOT = Path(*PATH.parts[:PATH.parts.index('views_pipeline') + 1])
        PATH_COMMON_UTILS = PATH_ROOT / 'common_utils'

        if not PATH_COMMON_UTILS.exists():

            raise ValueError("The 'common_utils' directory was not found in the provided path.")
        
    else:

        raise ValueError("The 'views_pipeline' directory was not found in the provided path.")

    return PATH_COMMON_UTILS


# Import your logging setup function from wherever it is defined
# from your_logging_module import setup_logging, get_common_logs_path

def test_logging_setup():
    # Step 1: Set up the logging configuration
    try:
        log_directory = get_common_logs_path()  # Fetch centralized log directory
        logger = setup_logging()  # Initialize logging setup
    
    except Exception as e:
        print(f"Failed to initialize logging setup: {e}")
        return

    # Step 2: Generate test log messages
    logger.debug("This is a DEBUG log message for testing.")
    logger.info("This is an INFO log message for testing.")
    logger.error("This is an ERROR log message for testing.")

    # Step 3: Define expected log files
    expected_files = [
        log_directory / "views_pipeline_INFO.log",
        log_directory / "views_pipeline_DEBUG.log",
        log_directory / "views_pipeline_ERROR.log"
    ]

    # Step 4: Check if log files exist and are not empty
    for file_path in expected_files:
        if file_path.exists():
            print(f"Log file '{file_path}' exists.")
            if file_path.stat().st_size > 0:
                print(f"Log file '{file_path}' contains data.")
            else:
                print(f"Warning: Log file '{file_path}' is empty.")
        else:
            print(f"Error: Log file '{file_path}' was not created as expected.")

    print("Logging setup test completed.")

# Run the test

if __name__ == "__main__":

    PATH_COMMON_UTILS = get_path_common_utils()

    sys.path.append(str(PATH_COMMON_UTILS))

    from utils_logger import setup_logging, get_common_logs_path

    test_logging_setup()
