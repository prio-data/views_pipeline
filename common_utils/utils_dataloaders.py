import argparse
import os
import numpy as np
import pandas as pd
from pathlib import Path
import sys
# from config_partitioner import get_partitioner_dict
try:
    from set_partition import get_partitioner_dict
except:
    pass
# from config_input_data import get_input_data_config  # this is model specific
from common_configs import config_drift_detection
from utils_df_to_vol_conversion import df_to_vol
from viewser import Queryset, Column

sys.path.append(str(Path(__file__).parent))
from meta_tools.utils import utils_model_paths
import logging
from model_path import ModelPath
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Super sus but works for now.
def find_model_name():
    for path in sys.path:
        try:
            model_name = utils_model_paths.get_model_name_from_path(path)
            if model_name:
                return model_name
        except:
            continue
    raise RuntimeError('Could not find model name')

def fetch_data_from_viewser(month_first, month_last, drift_config_dict, self_test):
    """
    Fetches and prepares the initial DataFrame from viewser.

    For more documentation, refer to the viewser repository: https://github.com/prio-data/viewser

    Returns:
        pd.DataFrame: The prepared DataFrame with initial processing done.
    """
    logger.info(f'Beginning file download through viewser with month range {month_first},{month_last}')
    model_path = ModelPath(model_name_or_path=find_model_name(), validate=True)
    queryset_base = model_path.get_queryset()  # just used here..
    if queryset_base is None:
        raise RuntimeError(f'Could not find queryset for {model_path.model_name} in common_querysets')
    else:
        logger.info(f'Found queryset for {model_path.model_name} in common_querysets')
    del model_path
    df, alerts = queryset_base.publish().fetch_with_drift_detection(start_date=month_first,
                                                                    end_date=month_last - 1,
                                                                    drift_config_dict=drift_config_dict,
                                                                    self_test=self_test)

    df = ensure_float64(df)  # The dataframe must contain only np.float64 floats

    # Not required for stepshift model
    # df.reset_index(inplace=True)
    # df.rename(columns={'priogrid_gid': 'pg_id'}, inplace=True) # arguably HydraNet or at lest vol specific
    # df['in_viewser'] = True  # arguably HydraNet or at lest vol specific

    return df, alerts


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
    month in the train and max month in the predict portions (or min and max months in the train portion for
    the forecasting partition)

    Args:
        df: dataframe to be checked
        partition: partition against which to check
        override_month: if user has overridden the end month of the forecasting partition, this value
        is substituted for the last month in the forecasting train portion

    Returns:
        True=success, False=failed

    """

    if 'month_id' in df.columns:
        df_time_units = df['month_id'].values
    else:
        df_time_units = df.index.get_level_values('month_id').values
    partitioner_dict = get_partitioner_dict(partition)
    if partition in ['calibration', 'testing']:
        first_month = partitioner_dict['train'][0]
        last_month = partitioner_dict['predict'][1]
    else:
        first_month = partitioner_dict['train'][0]
        last_month = partitioner_dict['train'][1]
        if override_month is not None:
            last_month = override_month - 1

    if [np.min(df_time_units), np.max(df_time_units)] != [first_month, last_month]:
        return False
    else:
        return True


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


def get_views_df(partition, override_month=None, self_test=False):
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

    df, alerts = fetch_data_from_viewser(month_first, month_last, drift_config_dict, self_test)

    return df, alerts


def fetch_or_load_views_df(partition, PATH_RAW, self_test=False, use_saved=False, override_month=None):
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

    path_viewser_df = os.path.join(str(PATH_RAW), f'{partition}_viewser_df.pkl')  # maby change to df...

    # Create the folders if they don't exist
    os.makedirs(str(PATH_RAW), exist_ok=True)
    # os.makedirs(str(PATH_PROCESSED), exist_ok=True)

    alerts = None

    if use_saved:
        # Check if the VIEWSER data file exists
        try:
            df = pd.read_pickle(path_viewser_df)
            print(f'Reading saved data from {path_viewser_df}')

        except:
            raise RuntimeError(f'Use of saved data was specified but {path_viewser_df} not found')

    else:
        print(f'Fetching file...')
        df, alerts = get_views_df(partition, override_month, self_test)  # which is then used here
        print(f'Saving file to {path_viewser_df}')
        df.to_pickle(path_viewser_df)

    if validate_df_partition(df, partition, override_month):

        return df, alerts

    else:
        raise RuntimeError(f'file at {path_viewser_df} incompatible with partition {partition}')


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


def get_alert_help_string():
    help_string = (f"""
                 # Data fetching and drift detection run
                 Issues alerts if drift detection algorithms selected in config\_drift\_detection
                 are triggered\n
                 ## Guide to interpreting alerts
                 **alarm**: which detection algorithm issued the warning, e.g. feature zeros
                 delta completeness - names should be self.explanatory\n
                 **offender**: what entity triggered the alert - which features, space units,
                 or time units (a dummy value is returned if the alert refers to the 
                 whole dataset\n
                 **threshold**: what threshold was set in config dict\n
                 **severity**: indication of how far over the threshold the trigger is
                 """)

    return help_string


def publish_drift_detection_test_ps():

    """
    This function defines and publishes a small simple test queryset used by the drift-detection system for
    self testing.

    This MUST be done before self-testing can be done.

    This queryset should only be modified in EXCEPTIONAL CIRCUMSTANCES after CAREFUL CONSIDERATION!

    Returns: Nothing

    """

    qs_self_test = (Queryset("drift_detection_self_test", "country_month")

                    .with_column(Column("ln_ged_ns", from_loa="country_month",
                                        from_column="ged_ns_best_sum_nokgi")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 )

                    .with_column(Column("ln_ged_os", from_loa="country_month",
                                        from_column="ged_os_best_sum_nokgi")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 )

                    .with_column(Column("ln_ged_sb", from_loa="country_month",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 )

                    .with_column(Column("wdi_sp_pop_totl", from_loa="country_year",
                                        from_column="wdi_sp_pop_totl")
                                 .transform.missing.replace_na()
                                 .transform.ops.ln()
                                 )
                    )

    qs_self_test.publish()

    return

def ensure_float64(df):
    """
    Check if the DataFrame only contains np.float64 types. If not, raise a warning
    and convert the DataFrame to use np.float64 for all its numeric columns.
    """

    non_float64_cols = df.select_dtypes(include=['number']).columns[
        df.select_dtypes(include=['number']).dtypes != np.float64]

    if len(non_float64_cols) > 0:
        print(
            f"Warning: DataFrame contains non-np.float64 numeric columns. Converting the following columns: {', '.join(non_float64_cols)}")

        for col in non_float64_cols:
            df[col] = df[col].astype(np.float64)

    return df


def parse_args():
    parser = argparse.ArgumentParser(description='Fetch data for different partitions')

    # Add binary flags for each partition
    parser.add_argument('-c', '--calibration', action='store_true', help='Fetch calibration data from viewser')
    parser.add_argument('-t', '--testing', action='store_true', help='Fetch testing data from viewser')
    parser.add_argument('-f', '--forecasting', action='store_true', help='Fetch forecasting data from viewser')
    parser.add_argument('-s', '--saved', action='store_true', help='Used locally stored data')
    parser.add_argument('-o', '--override_month', help='Over-ride use of current month', type=int)

    return parser.parse_args()