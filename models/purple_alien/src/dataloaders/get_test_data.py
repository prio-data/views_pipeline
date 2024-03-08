# Use viewser env

import sys

from viewser import Queryset, Column
from ingester3.ViewsMonth import ViewsMonth

import os
import pickle

import numpy as np
import pandas as pd


# ------------------------- CHANGE TO A COMMON UTIL ---------------------------------
from pathlib import Path

def setup_project_paths():
    root_path = Path(__file__).resolve().parents[3]

    # Define common paths
    common_utils_path = root_path / "common_utils"
    common_configs_path = root_path / "common_configs"

    # Define model-specific paths
    model_path = Path(__file__).resolve().parents[1]
    configs_path = model_path / "configs"
    src_path = model_path / "src"
    utils_path = src_path / "utils"
    architectures_path = src_path / "architectures"

    paths_to_add = [common_utils_path, common_configs_path, configs_path, utils_path, architectures_path]

    for path in paths_to_add:
        path_str = str(path)
        if path.exists() and path_str not in sys.path:
            sys.path.insert(0, path_str)

# Call the function to setup the project paths
setup_project_paths()
# -----------------------------------------------------------------------------------

from config_hyperparameters import get_hp_config
from config_partitioner import get_partitioner_dict
from utils_dataloaders import get_views_date, df_to_vol

 
if __name__ == "__main__":
    
    partition = 'testing'   # 'calibration', 'forecasting', 'testing'

    config = get_hp_config()

    processed_location = config['path_processed_data']
    raw_location = config['path_raw_data']

    path_viewser_data = raw_location + f'/{partition}_viewser_data.pkl'
    path_vol = processed_location +  f'/{partition}_vol.npy'

    # create the folders if they don't exist
    if not os.path.exists(raw_location):
        os.makedirs(raw_location)

    if not os.path.exists(processed_location):
        os.makedirs(processed_location)

    # check if the VIEWSER files exist
    if os.path.isfile(path_viewser_data) == True:

        print('File already downloaded')
        df = pd.read_pickle(path_viewser_data)
    
    else:
        print('Downloading file...')
        df = get_views_date(partition)

        # save pkl
        print(f'Saving file to {path_viewser_data}')
        df.to_pickle(path_viewser_data)

    # check if the volume exists
    if os.path.isfile(path_vol) == True:

        print('Volume already created')
        vol = np.load(path_vol)

    else:
        print('Creating volume...')

        # create volume
        vol = df_to_vol(df)

        print(f'shape of volume: {vol.shape}')
        print(f'Saving volume to {path_vol}')
 
        # save npy
        np.save(path_vol, vol)

    print('Done')
    