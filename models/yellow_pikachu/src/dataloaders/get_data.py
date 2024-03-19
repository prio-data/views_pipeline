import sys
from pathlib import Path
import pandas as pd
import numpy as np

PATH = Path(__file__) 
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)

from set_partition import get_partitioner_dict
from config_input_data import get_input_data
from utils import ensure_float64


def get_data():
    print("Getting data...")
    PATH_RAW, _, _ = setup_data_paths(PATH)
    parquet_path = PATH_RAW / 'raw.parquet'
    # print('PARQUET PATH', parquet_path)
    if not parquet_path.exists():
        qs_baseline = get_input_data()
        data = qs_baseline.publish().fetch()
        data = ensure_float64(data)
        data.to_parquet(parquet_path)
    else: 
        data = pd.read_parquet(parquet_path)

    return data


def get_partition_data(df, partition):
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


        