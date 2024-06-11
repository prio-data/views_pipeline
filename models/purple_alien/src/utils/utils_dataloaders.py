# Use viewser env

import sys
from pathlib import Path
import argparse

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)

from viewser import Queryset, Column
from ingester3.ViewsMonth import ViewsMonth

import os
import numpy as np
import pandas as pd


#from config_partitioner import get_partitioner_dict
from set_partition import get_partitioner_dict
from config_input_data import get_input_data_config

def get_views_date(partition):

    """partition can be 'calibration', 'testing' or 'forecasting'"""

    print('Beginning file download through viewser...')

    queryset_base = get_input_data_config()

# old viewser 5 code
#    queryset_base = (Queryset("simon_tests", "priogrid_month")
#        .with_column(Column("ln_sb_best", from_table = "ged2_pgm", from_column = "ged_sb_best_count_nokgi").transform.ops.ln().transform.missing.replace_na())
#        .with_column(Column("ln_ns_best", from_table = "ged2_pgm", from_column = "ged_ns_best_count_nokgi").transform.ops.ln().transform.missing.replace_na())
#        .with_column(Column("ln_os_best", from_table = "ged2_pgm", from_column = "ged_os_best_count_nokgi").transform.ops.ln().transform.missing.replace_na())
#        .with_column(Column("month", from_table = "month", from_column = "month"))
#        .with_column(Column("year_id", from_table = "country_year", from_column = "year_id"))
#        .with_column(Column("c_id", from_table = "country_year", from_column = "country_id"))
#        .with_column(Column("col", from_table = "priogrid", from_column = "col"))
#        .with_column(Column("row", from_table = "priogrid", from_column = "row")))
#

    df = queryset_base.publish().fetch()
    df.reset_index(inplace = True)

    df.rename(columns={'priogrid_gid': 'pg_id'}, inplace= True)

    df['in_viewser'] = True

    partitioner_dict = get_partitioner_dict(partition) # not that the partion includes both trainin and prediction/validation months

    month_first = partitioner_dict['train'][0]

    if partition == 'forecasting':
        month_last = partitioner_dict['train'][1] + 1 # no need to get the predict months as these are empty

    elif partition == 'calibration' or partition == 'testing':
        month_last = partitioner_dict['predict'][1] + 1 # predict[1] is the last month to predict, so we need to add 1 to include it.
    
    else:
        raise ValueError('partition should be either "calibration", "testing" or "forecasting"')

    
    month_range = np.arange(month_first, month_last,1) # predict[1] is the last month to predict, so we need to add 1 to include it.

    df = df[df['month_id'].isin(month_range)].copy() # temporal subset
    
    df.loc[:,'abs_row'] = df.loc[:,'row'] - df.loc[:,'row'].min() 
    df.loc[:,'abs_col'] = df.loc[:,'col'] - df.loc[:,'col'].min()
    df.loc[:,'abs_month'] = df.loc[:,'month_id'] - month_first  

    return df


def df_to_vol(df):

    """
    Converts a dataframe to a volume.
    
    Args:
        df (pandas.DataFrame): The input dataframe containing the data.

    Returns:
        numpy.ndarray: The volume representation of the dataframe.
    """

    month_first = df['month_id'].min() # Jan 1990
    month_last =  df['month_id'].max() # minus 1 because the current month is not yet available,

    month_range = month_last - month_first + 1
    space_range = 180

    features_num = 8 # should be inferred from the number of columns in the dataframe... 
    
    
    vol = np.zeros([space_range, space_range, month_range, features_num])
    
    vol[df['abs_row'], df['abs_col'], df['abs_month'], 0] = df['pg_id']
    vol[df['abs_row'], df['abs_col'], df['abs_month'], 1] = df['col'] # this is not what I want, I want the xcoord but...
    vol[df['abs_row'], df['abs_col'], df['abs_month'], 2] = df['row'] # this is not what I want, I want the ycoord but...
    vol[df['abs_row'], df['abs_col'], df['abs_month'], 3] = df['month_id']
    vol[df['abs_row'], df['abs_col'], df['abs_month'], 4] = df['c_id']
    vol[df['abs_row'], df['abs_col'], df['abs_month'], 5] = df['ln_sb_best']
    vol[df['abs_row'], df['abs_col'], df['abs_month'], 6] = df['ln_ns_best']
    vol[df['abs_row'], df['abs_col'], df['abs_month'], 7] = df['ln_os_best']
    
    vol = np.flip(vol, axis = 0) # flip the rows, so north is up.
    vol = np.transpose(vol, (2,0,1,3) ) # move the month dim to the front. Could just do it above but.. # move the month dim to the front. Could just do it above but.. should be something like (324, 180, 180, 8)
    
    print(f'Volume of shape {vol.shape} created. Should be (n_month, 180, 180, 8)')

    return vol


def process_partition_data(partition, PATH):

    """
    Fetches data for a given partition by ensuring the existence of necessary directories,
    downloading or loading existing data, and creating or loading a volume.

    Args:
        partition (str): The partition to process, e.g., 'calibration', 'forecasting', 'testing'.

    Returns:
        tuple: A tuple containing the DataFrame `df` and the volume `vol`.
    """
    
    PATH_RAW, PATH_PROCESSED, _ = setup_data_paths(PATH)

    path_viewser_data = os.path.join(str(PATH_RAW), f'{partition}_viewser_data.pkl')
    path_vol = os.path.join(str(PATH_PROCESSED), f'{partition}_vol.npy')

    # Create the folders if they don't exist
    os.makedirs(str(PATH_RAW), exist_ok=True)
    os.makedirs(str(PATH_PROCESSED), exist_ok=True)

    # Check if the VIEWSER data file exists
    if os.path.isfile(path_viewser_data):
        print('File already downloaded')
        df = pd.read_pickle(path_viewser_data)
    else:
        print('Downloading file...')
        df = get_views_date(partition)
        print(f'Saving file to {path_viewser_data}')
        df.to_pickle(path_viewser_data)

    # Check if the volume exists
    if os.path.isfile(path_vol):
        print('Volume already created')
        vol = np.load(path_vol)
    else:
        print('Creating volume...')
        vol = df_to_vol(df)
        print(f'shape of volume: {vol.shape}')
        print(f'Saving volume to {path_vol}')
        np.save(path_vol, vol)

    print('Done')

    return df, vol

def parse_args():
    parser = argparse.ArgumentParser(description='Fetch data for different partitions')

    # Add binary flags for each partition
    parser.add_argument('-c', '--calibration', action='store_true', help='Fetch calibration data from viewser')
    parser.add_argument('-t', '--testing', action='store_true', help='Fetch testing data from viewser')
    parser.add_argument('-f', '--forecasting', action='store_true', help='Fetch forecasting data from viewser')

    return parser.parse_args()

def process_data(partition, PATH):
    """
    Fetch the data for the given partition from viewser.

    Args:
        partition (str): The partition type (e.g., 'calibration', 'testing', 'forecasting').
        PTAH (Path): The base path for data.

    Returns:
        tuple: DataFrame and volume array for the partition.
    """
    df, vol = process_partition_data(partition, PATH)
    return df, vol
