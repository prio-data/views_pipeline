import sys
from pathlib import Path
import pandas as pd
import numpy as np

PATH = Path(__file__) 
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils"))
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)

from utils_input_data import ensure_float64
from set_partition import get_partitioner_dict
from config_input_data import get_input_data

def get_data():
    """ 
    Fetches the input data from the viewser queryset defined in get_input_data function of config_input_data.py 
    Checks if the data is already saved as a parquet file, if not, fetches the data and saves it as a parquet file. 
    Also ensures that all numeric columns are of type np.float64.

    Returns:
    - data (pd.DataFrame): Input data fetched from the viewser queryset.
    """
    print("Getting data...")
    PATH_RAW, _, _ = setup_data_paths(PATH)
    parquet_path = PATH_RAW / 'raw.parquet'
    # print('PARQUET PATH', parquet_path)
    if not parquet_path.exists():        
        qs = get_input_data()
        data = qs.publish().fetch() 
        data = ensure_float64(data)
        data.to_parquet(parquet_path)
    else: 
        data = pd.read_parquet(parquet_path)

    return data

def get_partition_data(df, partition):
    """
    Temporally subsets the input data based on the partition.

    Args:
    - df (pd.DataFrame): Input data fetched from the viewser queryset.
    - partition (str): The partition of the data (calibration, testing, forecasting).

    Returns:
    - df (pd.DataFrame): Temporally subsetted data based on the partition.
    """

    partitioner_dict = get_partitioner_dict(partition)

    month_first = partitioner_dict['train'][0]

    if partition == 'forecasting':
        month_last = partitioner_dict['train'][1] + 1 # no need to get the predict months as these are empty

    elif partition == 'calibration' or partition == 'testing':
        month_last = partitioner_dict['predict'][1] + 1 # predict[1] is the last month to predict, so we need to add 1 to include it.
    
    else:
        raise ValueError('partition should be either "calibration", "testing" or "forecasting"')
    
    month_range = np.arange(month_first, month_last,1) # predict[1] is the last month to predict, so we need to add 1 to include it.

    df = df[df.index.get_level_values("month_id").isin(month_range)].copy() # temporal subset

    return df


def check_data():
    """
    Check missingness and infinity values in the input data
    """
    data = get_data()
    print("Checking missingness and infinity values in the input data...")
    print("Missing values in the input data:")
    print(data.isnull().sum())
    print("Infinity values in the input data:")
    print(data.isin([np.inf, -np.inf]).sum())


if __name__ == "__main__":
    get_data()
    print("Data fetched successfully.")