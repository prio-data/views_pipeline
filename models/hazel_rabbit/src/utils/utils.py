import numpy as np
from datetime import datetime
import pickle




import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)




def get_raw_data(config):
    """
    Return the raw data.

    Args:
        config : Configuration object containing parameters and settings.
    """

    PATH_RAW, _, PATH_GENERATED = setup_data_paths(PATH)
    run_type = config.run_type
    file_name = f'/{run_type}_viewser_df.pkl'
    print(f'Loading {run_type} data from {file_name}...')
    views_raw = np.load(str(PATH_RAW) + file_name, allow_pickle=True)
    
    return views_raw




def create_model_time_stamp(config):
    """
    Create the timestamp of the evaluation and add to the config.

    Args:
        config : Configuration object containing parameters and settings.
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"timestamp: {timestamp}")
    # add to config for logging and conciseness
    config.model_time_stamp = timestamp

    return config


def save_generated_pred(config, views_res):
    """
    Save the predictions in a pickle file.

    Args:
        config : Configuration object containing parameters and settings.
        views_res : DataFrame containing the predictions.
    """

    _, _, PATH_GENERATED = setup_data_paths(PATH)
    outputs_path = f'{PATH_GENERATED}/df_sb_os_ns_output_{config.time_steps}_{config.run_type}_{config.model_time_stamp}.pkl'
    with open(outputs_path, 'wb') as file:
        pickle.dump(views_res, file)

    return






