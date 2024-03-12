# Use viewser env

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths
setup_project_paths(PATH)

from config_hyperparameters import get_hp_config
from utils_dataloaders import get_views_date, df_to_vol, process_partition_data
 
if __name__ == "__main__":
    
    partition = 'testing'   # 'calibration', 'forecasting', 'testing'

    df, vol = process_partition_data(partition, get_hp_config, get_views_date, df_to_vol, PATH)   