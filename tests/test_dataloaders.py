import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path
import os

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

from model_path import ModelPath
from dataloaders import ViewsDataLoader

@pytest.fixture
def sample_df():
    """
    Fixture to create a sample DataFrame for testing.

    Returns:
        pd.DataFrame: A sample DataFrame with month_id and value columns.
    """
    return pd.DataFrame({
        'month_id': [121, 122, 123, 124, 125],
        'value': [10, 20, 30, 40, 50]
    })

@pytest.fixture
def model_path(tmpdir):
    """
    Fixture to create a mock ModelPath object for testing.

    Args:
        tmpdir: A temporary directory provided by pytest.

    Returns:
        Mock: A mock ModelPath object with specified attributes.
    """
    mock_model_path = Mock(spec=ModelPath)
    mock_model_path.model_name = "test_model"
    mock_model_path.validate = False
    mock_model_path.target = "model"
    mock_model_path.data_raw = tmpdir.mkdir("raw")
    mock_model_path.data_processed = tmpdir.mkdir("processed")
    return mock_model_path

def test_initialization(model_path):
    """
    Test the initialization of the ViewsDataLoader class.

    This test verifies that the ViewsDataLoader class initializes correctly with the given ModelPath object.

    Args:
        model_path (Mock): The mock ModelPath object provided by the fixture.

    Asserts:
        - The _model_path attribute is set correctly.
        - The partition attribute is set to "calibration".
    """
    loader = ViewsDataLoader(model_path, partition="calibration")
    assert loader._model_path == model_path
    assert loader.partition == "calibration"

def test_get_partition_dict(model_path):
    """
    Test the _get_partition_dict method.

    This test verifies that the _get_partition_dict method returns the correct partition dictionary
    for each partition type.

    Args:
        model_path (Mock): The mock ModelPath object provided by the fixture.

    Asserts:
        - The partition dictionary for "calibration" is correct.
        - The partition dictionary for "testing" is correct.
        - The partition dictionary for "forecasting" is correct.
        - A ValueError is raised for an invalid partition type.
    """
    loader = ViewsDataLoader(model_path, partition="calibration")
    partition_dict = loader._get_partition_dict()
    assert partition_dict == {"train": (121, 396), "predict": (397, 444)}

    loader.partition = "testing"
    partition_dict = loader._get_partition_dict()
    assert partition_dict == {"train": (121, 444), "predict": (445, 492)}

    loader.partition = "forecasting"
    partition_dict = loader._get_partition_dict()
    assert partition_dict == {"train": (121, 537), "predict": (538, 574)}

    loader.partition = "invalid"
    with pytest.raises(ValueError):
        loader._get_partition_dict()

def test_validate_df_partition(model_path, sample_df):
    """
    Test the _validate_df_partition method.

    This test verifies that the _validate_df_partition method correctly validates the DataFrame
    based on the partition type.

    Args:
        model_path (Mock): The mock ModelPath object provided by the fixture.
        sample_df (pd.DataFrame): The sample DataFrame provided by the fixture.

    Asserts:
        - The DataFrame is valid for "calibration".
        - The DataFrame is not valid for "forecasting".
    """
    loader = ViewsDataLoader(model_path, partition="calibration")
    loader.partition_dict = loader._get_partition_dict()
    loader.month_first, loader.month_last = loader._get_month_range()
    assert loader._validate_df_partition(sample_df) == True

    loader.partition = "forecasting"
    loader.partition_dict = loader._get_partition_dict()
    loader.month_first, loader.month_last = loader._get_month_range()
    assert loader._validate_df_partition(sample_df) == False

def test_filter_dataframe_by_month_range(model_path, sample_df):
    """
    Test the filter_dataframe_by_month_range method.

    This test verifies that the filter_dataframe_by_month_range method correctly filters the DataFrame
    based on the specified month range.

    Args:
        model_path (Mock): The mock ModelPath object provided by the fixture.
        sample_df (pd.DataFrame): The sample DataFrame provided by the fixture.

    Asserts:
        - The filtered DataFrame contains the correct number of rows.
    """
    loader = ViewsDataLoader(model_path, partition="calibration")
    loader.month_first, loader.month_last = 121, 126
    filtered_df = loader.filter_dataframe_by_month_range(df=sample_df)
    assert len(filtered_df) == 5

@patch('dataloaders.create_data_fetch_log_file')
@patch('dataloaders.Path.exists', return_value=True)
@patch('dataloaders.pd.read_pickle')
@patch('dataloaders.os.makedirs')
@patch('dataloaders.ViewsDataLoader._fetch_data_from_viewser')
def test_get_data(mock_fetch_data, mock_makedirs, mock_read_pickle, mock_path_exists, mock_create_log, model_path, sample_df):
    """
    Test the get_data method.

    This test verifies that the get_data method correctly fetches or loads a DataFrame for a given partition
    from viewser.

    Args:
        mock_fetch_data (MagicMock): The mock object for _fetch_data_from_viewser.
        mock_makedirs (MagicMock): The mock object for os.makedirs.
        mock_read_pickle (MagicMock): The mock object for pd.read_pickle.
        mock_path_exists (MagicMock): The mock object for Path.exists.
        mock_create_log (MagicMock): The mock object for create_data_fetch_log_file.
        model_path (Mock): The mock ModelPath object provided by the fixture.
        sample_df (pd.DataFrame): The sample DataFrame provided by the fixture.

    Asserts:
        - The fetched or loaded DataFrame is of type pd.DataFrame.
        - The alerts are correctly set to ["alert1", "alert2"].
    """
    mock_read_pickle.return_value = sample_df
    mock_fetch_data.return_value = (sample_df, ["alert1", "alert2"])
    loader = ViewsDataLoader(model_path, partition="calibration")
    loader.partition_dict = loader._get_partition_dict()
    loader.month_first, loader.month_last = loader._get_month_range()
    
    # Ensure the directory exists
    mock_makedirs(loader._model_path.data_raw, exist_ok=True)
    
    df, alerts = loader.get_data(self_test=True, partition="calibration", use_saved=False)
    assert isinstance(df, pd.DataFrame)
    assert alerts == ["alert1", "alert2"]