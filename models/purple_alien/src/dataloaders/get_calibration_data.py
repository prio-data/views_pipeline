# Use viewser env

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths
setup_project_paths(PATH)

from viewser import Queryset, Column
from ingester3.ViewsMonth import ViewsMonth

import os
import pickle

import numpy as np
import pandas as pd

from config_hyperparameters import get_hp_config
from config_partitioner import get_partitioner_dict
from utils_dataloaders import get_views_date, df_to_vol
 
if __name__ == "__main__":
    
    partition = 'calibration' # 'calibration', 'forecasting', 'testing'

    # Should be a function in a dataloaders utils (maybe in common_utils later on?)

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
    