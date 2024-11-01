import pytest
import pandas as pd
import numpy as np
import os
from unittest.mock import Mock, patch, MagicMock

from pathlib import Path
import sys

# Setting up the path to include the common_utils directory for imports
PATH = Path(__file__)
if 'views_pipeline' in PATH.parts:
    PATH_ROOT = Path(*PATH.parts[:PATH.parts.index('views_pipeline') + 1])
    PATH_COMMON_UTILS = PATH_ROOT / 'common_utils'
    if not PATH_COMMON_UTILS.exists():
        raise ValueError("The 'common_utils' directory was not found in the provided path.")
    sys.path.insert(0, str(PATH_COMMON_UTILS))
else:
    raise ValueError("The 'views_pipeline' directory was not found in the provided path.")

from utils_dataloaders import (
    get_month_range,
    get_drift_config_dict,
    validate_df_partition,
    fetch_data_from_viewser,
    fetch_or_load_views_df,
    create_or_load_views_vol
)

# Pretends to be "electric_relaxation".

# Fixture to provide a sample DataFrame for testing
@pytest.fixture
def sample_df():
    """
    Fixture to create a sample DataFrame for testing.

    Returns:
        pd.DataFrame: A sample DataFrame with month_id and value columns.
    """
    data = {
        'month_id': [1, 2, 3, 4, 5],
        'value': [10, 20, 30, 40, 50]
    }
    return pd.DataFrame(data)

# Fixture to provide a sample partitioner dictionary for testing
@pytest.fixture
def partitioner_dict():
    """
    Fixture to create a sample partitioner dictionary for testing.

    Returns:
        dict: A sample partitioner dictionary with train and predict keys.
    """
    return {
        'train': [1, 3],
        'predict': [4, 5]
    }

# Fixture to provide a sample drift configuration dictionary for testing
@pytest.fixture
def drift_config_dict():
    """
    Fixture to create a sample drift configuration dictionary for testing.

    Returns:
        dict: A sample drift configuration dictionary with calibration, testing, and forecasting keys.
    """
    return {
        'calibration': {'threshold': 0.1},
        'testing': {'threshold': 0.2},
        'forecasting': {'threshold': 0.3}
    }

def test_get_month_range(partitioner_dict):
    """
    Test the get_month_range function.

    This test verifies that the get_month_range function correctly determines the month range
    based on the partition type.

    Args:
        partitioner_dict (dict): The sample partitioner dictionary provided by the fixture.

    Asserts:
        - The month range for 'calibration' is (1, 6).
        - The month range for 'testing' is (1, 6).
        - The month range for 'forecasting' is (1, 4).
    """
    with patch('utils_dataloaders.get_partitioner_dict', return_value=partitioner_dict):
        assert get_month_range('calibration') == (1, 6)
        assert get_month_range('testing') == (1, 6)
        assert get_month_range('forecasting') == (1, 4)

def test_get_drift_config_dict():
    """
    Test the get_drift_config_dict function.

    This test verifies that the get_drift_config_dict function correctly retrieves the drift-detection
    configuration dictionary for the specified partition.

    Asserts:
        - The drift configuration for 'calibration' is {'threshold': 0.1}.
    """
    drift_config_dict = Mock()
    drift_config_dict.drift_detection_partition_dict = {
        'calibration': {'threshold': 0.1},
        'forecasting': {'threshold': 0.3},
        'testing': {'threshold': 0.2}
    }
    with patch('utils_dataloaders.config_drift_detection', drift_config_dict):
        assert get_drift_config_dict('calibration') == {'threshold': 0.1}

def test_validate_df_partition(sample_df, partitioner_dict):
    """
    Test the validate_df_partition function.

    This test verifies that the validate_df_partition function correctly validates the DataFrame
    based on the partition type.

    Args:
        sample_df (pd.DataFrame): The sample DataFrame provided by the fixture.
        partitioner_dict (dict): The sample partitioner dictionary provided by the fixture.

    Asserts:
        - The DataFrame is valid for 'calibration'.
        - The DataFrame is valid for 'testing'.
        - The DataFrame is not valid for 'forecasting'.
    """
    with patch('utils_dataloaders.get_partitioner_dict', return_value=partitioner_dict):
        assert validate_df_partition(sample_df, 'calibration') == True
        assert validate_df_partition(sample_df, 'testing') == True
        assert validate_df_partition(sample_df, 'forecasting') == False

@patch('utils_dataloaders.ModelPath')
@patch('utils_dataloaders.Queryset')
def test_fetch_data_from_viewser(mock_queryset, mock_modelpath, sample_df):
    """
    Test the fetch_data_from_viewser function.

    This test verifies that the fetch_data_from_viewser function correctly fetches and prepares
    the initial DataFrame from viewser.

    Args:
        mock_queryset (MagicMock): The mock object for Queryset.
        mock_modelpath (MagicMock): The mock object for ModelPath.
        sample_df (pd.DataFrame): The sample DataFrame provided by the fixture.

    Asserts:
        - The fetched DataFrame is of type pd.DataFrame.
        - The alerts are correctly fetched.
    """
    mock_modelpath.return_value.get_queryset.return_value = mock_queryset
    mock_queryset.publish.return_value.fetch_with_drift_detection.return_value = (sample_df, "alerts")
    
    df, alerts = fetch_data_from_viewser("electric_relaxation", 1, 5, {}, False) # No self test
    
    assert isinstance(df, pd.DataFrame)
    assert alerts == "alerts"

@patch('os.path.isfile')
@patch('os.makedirs')
@patch('pandas.read_pickle')
@patch('utils_dataloaders.get_views_df')
@patch('utils_dataloaders.create_data_fetch_log_file')
@patch('utils_dataloaders.validate_df_partition', return_value=True)
def test_fetch_or_load_views_df(mock_validate, mock_create_log, mock_get_views_df, mock_read_pickle, mock_makedirs, mock_isfile, sample_df):
    """
    Test the fetch_or_load_views_df function.

    This test verifies that the fetch_or_load_views_df function correctly fetches or loads
    a DataFrame for a given partition from viewser.

    Args:
        mock_validate (MagicMock): The mock object for validate_df_partition.
        mock_create_log (MagicMock): The mock object for create_data_fetch_log_file.
        mock_get_views_df (MagicMock): The mock object for get_views_df.
        mock_read_pickle (MagicMock): The mock object for pd.read_pickle.
        mock_makedirs (MagicMock): The mock object for os.makedirs.
        mock_isfile (MagicMock): The mock object for os.path.isfile.
        sample_df (pd.DataFrame): The sample DataFrame provided by the fixture.

    Asserts:
        - The fetched or loaded DataFrame is of type pd.DataFrame.
        - The alerts are correctly set to None when using saved data.
    """
    mock_isfile.return_value = True
    mock_read_pickle.return_value = sample_df
    mock_get_views_df.return_value = (sample_df, "alerts")

    df, alerts = fetch_or_load_views_df("electric_relaxation", "calibration", "/path/to/raw", False, use_saved=True)
    assert isinstance(df, pd.DataFrame)
    assert alerts is None  # Check for the correct default value of alerts

@patch('os.path.isfile')
@patch('os.makedirs')
@patch('numpy.load')
@patch('numpy.save')
@patch('pandas.read_pickle')
@patch('utils_dataloaders.df_to_vol')
def test_create_or_load_views_vol(mock_df_to_vol, mock_read_pickle, mock_save, mock_load, mock_makedirs, mock_isfile, sample_df):
    """
    Test the create_or_load_views_vol function.

    This test verifies that the create_or_load_views_vol function correctly creates or loads
    a volume for a given partition from viewser.

    Args:
        mock_df_to_vol (MagicMock): The mock object for df_to_vol.
        mock_read_pickle (MagicMock): The mock object for pd.read_pickle.
        mock_save (MagicMock): The mock object for np.save.
        mock_load (MagicMock): The mock object for np.load.
        mock_makedirs (MagicMock): The mock object for os.makedirs.
        mock_isfile (MagicMock): The mock object for os.path.isfile.
        sample_df (pd.DataFrame): The sample DataFrame provided by the fixture.

    Asserts:
        - The created or loaded volume is of type np.ndarray.
    """
    mock_isfile.return_value = True
    mock_load.return_value = np.array([1, 2, 3])
    
    vol = create_or_load_views_vol("calibration", "/path/to/processed", "/path/to/raw")
    
    assert isinstance(vol, np.ndarray)
    
    mock_isfile.return_value = False
    mock_read_pickle.return_value = sample_df
    mock_df_to_vol.return_value = np.array([1, 2, 3])
    
    vol = create_or_load_views_vol("calibration", "/path/to/processed", "/path/to/raw")
    
    assert isinstance(vol, np.ndarray)