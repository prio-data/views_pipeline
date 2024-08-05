import argparse
import os
import numpy as np
import pandas as pd


#from config_partitioner import get_partitioner_dict
from set_partition import get_partitioner_dict
from config_input_data import get_input_data_config # this is model specific... this is thi issue.. .
from common_configs import config_drift_detection
from utils_df_to_vol_conversion import df_to_vol
from utils_logging_and_print_outputs import print_dataset_dates


def fetch_data_from_viewser(month_first,month_last, drift_config_dict):
    """
    Fetches and prepares the initial DataFrame from viewser.

    Returns:
        pd.DataFrame: The prepared DataFrame with initial processing done.
    """
    print(f'Beginning file download through viewser with month range {month_first},{month_last}')
    queryset_base = get_input_data_config() # just used here.. 

# Input drift dection 
#    df, alerts = queryset_base.publish().fetch_with_drift_detection(month_first, month_last-1, drift_config_dict)

# no Input drift detection
    df = queryset_base.publish().fetch() #.fetch_with_drift_detection(month_first, month_last-1, drift_config_dict)

    df.reset_index(inplace=True)
    df.rename(columns={'priogrid_gid': 'pg_id'}, inplace=True) # arguably HydraNet or at lest vol specific
    df['in_viewser'] = True  # arguably HydraNet or at lest vol specific

    df = filter_dataframe_by_month_range(df, month_first, month_last)

# Input drift detection    
#    for alert in alerts: ####
#        print(alert)     #####

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

def get_drift_config_dict(partition):

    """
    Gets the drift-detection configuration dictionary for the pertinent partition from the
    drift detection configs

    Args:
        partition:

    Returns:
        the drift-detection configuration dict for the requested partition

    """

    drift_config_dict = config_drift_detection.drift_detection_partition_dict[partition]

    return drift_config_dict

def validate_df_partition(df, partition, override_month=None):

    """
    Checks to see if the min and max months in the input dataframe are the same as the min
    month in the train and max month in the predict set (or min and max months in the train set for
    the forecasting partition)

    Args:
        df: dataframe to be checked
        partition: partition against which to check
        override_month: if user has overridden the end month of the forecasting partition, this value
        is substituted for the last month in the forecasting train set

    Returns:
        True=success, False=failed

    """

    df_time_units = df['month_id'].values
    partitioner_dict = get_partitioner_dict(partition)
    
    if partition in ['calibration', 'testing']:
        first_month = partitioner_dict['train'][0]
        last_month = partitioner_dict['predict'][1]

        # debug !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #print(f'first_month: {first_month}, last_month: {last_month}')
        #print(f'{np.min(df_time_units)}, {np.max(df_time_units)}') # okay so here is a bug - the dataframe goes from 1 to 852... 
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    else:
        first_month = partitioner_dict['train'][0]
        last_month = partitioner_dict['train'][1]
        if override_month is not None:
            last_month=override_month-1

    if [np.min(df_time_units), np.max(df_time_units)] != [first_month,last_month]:
        return False
    else:
        return True

def filter_dataframe_by_month_range(df, month_first, month_last): # This is currentloy used in fetch_data_from_viewser (above). But when/if we can specificy the month range in the queryset then that should be done instead.
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


def get_views_df(partition, override_month=None):
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

    month_first, month_last = get_month_range(partition)
    drift_config_dict = get_drift_config_dict(partition)

    if partition == 'forecasting' and override_month is not None: 
        month_last = override_month
        print(f'\n ***Warning: overriding end month in forecasting partition to {month_last} ***\n')

    df = fetch_data_from_viewser(month_first, month_last, drift_config_dict)

    return df


def fetch_or_load_views_df(partition, PATH_RAW, use_saved=False, override_month=None):

    """
    Fetches or loads a DataFrame for a given partition from viewser.

    This function handles the retrieval or loading of raw data for the specified partition.

    The default behaviour is to fetch fresh data via viewser. This can be overridden by setting the
    used_saved flag to True, in which case saved data is returned, if it can be found.

    Args:
        partition (str): The partition to process. Valid options are 'calibration', 'forecasting', 'testing'.
        PATH_RAW (str or Path): The path to the model-specific directory where raw data should be stored.

    Returns:
        pd.DataFrame: The DataFrame fetched or loaded from viewser, with minimum preprocessing applied.
    """

    path_viewser_df = os.path.join(str(PATH_RAW), f'{partition}_viewser_df.pkl') #maybe change to df...

    # Create the folders if they don't exist
    os.makedirs(str(PATH_RAW), exist_ok=True)
    #os.makedirs(str(PATH_PROCESSED), exist_ok=True)

    if use_saved:
        # Check if the VIEWSER data file exists
        try:
            df = pd.read_pickle(path_viewser_df)
            print(f'Reading saved data from {path_viewser_df}')

        except:
            raise RuntimeError(f'Use of saved data was specified but {path_viewser_df} not found')

    else:
        print(f'Fetching file...')
        df = get_views_df(partition, override_month) # which is then used here
        print(f'Saving file to {path_viewser_df}')
        df.to_pickle(path_viewser_df)

    
    # return df 
    print_dataset_dates(df)
    
    if validate_df_partition(df, partition, override_month):
        return df

    else:
        raise RuntimeError(f'file at {path_viewser_df} incompatible with partition {partition}') # so now we save but also stop the sctipt?


# could be moved to common_utils/utils_df_to_vol_conversion.py but it is not really a conversion function so I would keep it here for now.
def create_or_load_views_vol(partition, PATH_PROCESSED, PATH_RAW):

    """
    Creates or loads a volume from a DataFrame for a specified partition.

    This function manages the creation or loading of a 4D volume array based on the DataFrame 
    associated with the given partition. It ensures that the volume file is available locally,
    either by loading it if it exists or creating it from the DataFrame if it does not.
    This volume array is used as input data for CNN-based models such as HydraNet.

    Args:
        partition (str): The partition to process. Valid options are 'calibration', 'forecasting', 'testing'.
        PATH_PROCESSED (str or Path): The path to the directory where processed volume data should be stored.

    Returns:
        np.ndarray: The 4D volume array created or loaded from the DataFrame, with shape 
                    [n_months, height, width, n_features].

    """

    path_vol = os.path.join(str(PATH_PROCESSED), f'{partition}_vol.npy')

    # Create the folders if they don't exist
    os.makedirs(str(PATH_PROCESSED), exist_ok=True)

    # Check if the volume exists
    if os.path.isfile(path_vol):
        print('Volume already created')
        vol = np.load(path_vol)
    else:
        print('Creating volume...')
        path_raw = os.path.join(str(PATH_RAW), f'{partition}_viewser_df.pkl')
        vol = df_to_vol(pd.read_pickle(path_raw))
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
    parser.add_argument('-s', '--saved', action='store_true', help='Used locally stored data')
    parser.add_argument('-o', '--override_month', help='Over-ride use of current month', type=int)


    return parser.parse_args()
