# Use viewser env

#import sys
#from pathlib import Path
import argparse

#PATH = Path(__file__)
#sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
#from set_path import setup_project_paths, setup_data_paths
#setup_project_paths(PATH)
#
#from viewser import Queryset, Column
#from ingester3.ViewsMonth import ViewsMonth
#
import os
import numpy as np
import pandas as pd


#from config_partitioner import get_partitioner_dict
from set_partition import get_partitioner_dict
from config_input_data import get_input_data_config # this is model specific... this is thi issue.. .
from utils_df_to_vol_conversion import df_to_vol



def fetch_data_from_viewser():
    """
    Fetches and prepares the initial DataFrame from viewser.

    Returns:
        pd.DataFrame: The prepared DataFrame with initial processing done.
    """
    print('Beginning file download through viewser...')
    queryset_base = get_input_data_config() # just used here.. 
    df = queryset_base.publish().fetch()
    df.reset_index(inplace=True)
    df.rename(columns={'priogrid_gid': 'pg_id'}, inplace=True) # arguably HydraNet or at lest vol specific
    df['in_viewser'] = True  # arguably HydraNet or at lest vol specific
    return df


def get_month_range(partition):
    """
    Determines the month range based on the partition type.

    Args:
        partition (str): The partition type ('calibration', 'testing', or 'forecasting').

    Returns:
        tuple: The start and end month IDs for the partition.

    Raises:
        ValueError: If partition is not 'calibration', 'testing', or 'forecasting'.
    """
    partitioner_dict = get_partitioner_dict(partition)
    month_first = partitioner_dict['train'][0]

    if partition == 'forecasting':
        month_last = partitioner_dict['train'][1] + 1
    elif partition == 'calibration' or partition == 'testing':
        month_last = partitioner_dict['predict'][1] + 1
    else:
        raise ValueError('partition should be either "calibration", "testing" or "forecasting"')

    return month_first, month_last


def filter_dataframe_by_month_range(df, month_first, month_last):
    """
    Filters the DataFrame to include only the specified month range.

    Args:
        df (pd.DataFrame): The input DataFrame to be filtered.
        month_first (int): The first month ID to include.
        month_last (int): The last month ID to include.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    month_range = np.arange(month_first, month_last)
    return df[df['month_id'].isin(month_range)].copy()


# moved to utils_df_to_vol_conversion.py as that is where it is used..
#def calculate_absolute_indices(df, month_first): # arguably HydraNet or at lest vol specific
#    """
#    Calculates absolute row, column, and month indices for the DataFrame.
#
#    Args:
#        df (pd.DataFrame): The DataFrame to update.
#        month_first (int): The first month ID in the month range.
#
#    Returns:
#        pd.DataFrame: The updated DataFrame with absolute indices.
#    """
#    df['abs_row'] = df['row'] - df['row'].min()         
#    df['abs_col'] = df['col'] - df['col'].min()
#    df['abs_month'] = df['month_id'] - month_first
#    return df
#

def get_views_df(partition):
    """
    Fetches and processes a DataFrame containing spatial-temporal data for the specified partition type.
    
    This function combines fetching data, determining the month range, filtering the DataFrame,
    and calculating absolute indices based on the provided partition type ('calibration', 'testing', or 'forecasting').

    Args:
        partition (str): Specifies the type of partition to retrieve. Must be one of 'calibration', 'testing', 
                         or 'forecasting'.
                         - 'calibration': Use months specified for calibration.
                         - 'testing': Use months specified for testing.
                         - 'forecasting': Use months specified for forecasting future data.

    Returns:
        pd.DataFrame: A DataFrame filtered and processed to include only the data within the specified partition's
                      temporal range. The DataFrame includes:
                      - 'pg_id': Priogrid ID (renamed from 'priogrid_gid').
                      - 'month_id': Month identifier.
                      - 'in_viewser': Boolean flag indicating data presence.
                      - 'abs_row': Absolute row index (row - minimum row).
                      - 'abs_col': Absolute column index (col - minimum col).
                      - 'abs_month': Absolute month index (month_id - first month in partition range).

    Raises:
        ValueError: If `partition` is not one of 'calibration', 'testing', or 'forecasting'.
    """
    df = fetch_data_from_viewser() # then it is used here..... 
    month_first, month_last = get_month_range(partition)
    df = filter_dataframe_by_month_range(df, month_first, month_last)
    #df = calculate_absolute_indices(df, month_first) # could go in the volume creation function...
    return df


def fetch_or_load_views_df(partition, PATH_RAW, PATH_PROCESSED):

    """
    ...
    """

    path_viewser_df = os.path.join(str(PATH_RAW), f'{partition}_viewser_df.pkl') #maby change to df...

    # Create the folders if they don't exist
    os.makedirs(str(PATH_RAW), exist_ok=True)
    os.makedirs(str(PATH_PROCESSED), exist_ok=True)

    # Check if the VIEWSER data file exists
    if os.path.isfile(path_viewser_df):
        print('File already downloaded')
        df = pd.read_pickle(path_viewser_df)
    else:
        print('Downloading file...')
        df = get_views_df(partition) # which is then used here 
        print(f'Saving file to {path_viewser_df}')
        df.to_pickle(path_viewser_df)

    print('Done')

    return df


def create_or_load_views_vol(partition, PATH_RAW, PATH_PROCESSED):

    """
    ...
    """

    path_vol = os.path.join(str(PATH_PROCESSED), f'{partition}_vol.npy')

    # Create the folders if they don't exist
    os.makedirs(str(PATH_RAW), exist_ok=True)
    os.makedirs(str(PATH_PROCESSED), exist_ok=True)

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

    return vol

def parse_args():
    parser = argparse.ArgumentParser(description='Fetch data for different partitions')

    # Add binary flags for each partition
    parser.add_argument('-c', '--calibration', action='store_true', help='Fetch calibration data from viewser')
    parser.add_argument('-t', '--testing', action='store_true', help='Fetch testing data from viewser')
    parser.add_argument('-f', '--forecasting', action='store_true', help='Fetch forecasting data from viewser')

    return parser.parse_args()

# seems rrdundent... 
#def process_data(partition, PATH):
#    """
#    Fetch the data for the given partition from viewser.
#
#    Args:
#        partition (str): The partition type (e.g., 'calibration', 'testing', 'forecasting').
#        PTAH (Path): The base path for data.
#
#    Returns:
#        tuple: DataFrame and volume array for the partition.
#    """
#    df, vol = process_partition_data(partition, PATH)
#    return df, vol
#


# It could be argued that a cuple of the designs above are only relevant for HydraNet, or at leat the volume creation part.
# But, it is really just the addition of a couple of features that can be sorted out downstream.
# So, I would keep it as is for now, but let me know if this is a huge bother for the stepsifted models.