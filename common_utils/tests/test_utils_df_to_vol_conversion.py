import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path

PATH = Path(__file__)
if 'views_pipeline' in PATH.parts:
    PATH_ROOT = Path(*PATH.parts[:PATH.parts.index('views_pipeline') + 1])
    PATH_COMMON_UTILS = PATH_ROOT / 'common_utils'
    if not PATH_COMMON_UTILS.exists():
        raise ValueError("The 'common_utils' directory was not found in the provided path.")
    sys.path.insert(0, str(PATH_COMMON_UTILS))
else:
    raise ValueError("The 'views_pipeline' directory was not found in the provided path.")

from utils_df_to_vol_conversion import (
    get_requried_columns_for_vol,
    calculate_absolute_indices,
    df_to_vol,
    vol_to_df,
    df_vol_conversion_test,
    plot_vol,
)


@pytest.fixture
def mock_df():
    """
    Fixture to create a mock DataFrame.

    This fixture creates a mock DataFrame with predefined data for testing purposes.
    The DataFrame contains columns for pg_id, col, row, month_id, c_id, ln_sb_best,
    ln_ns_best, and ln_os_best. The DataFrame is used to simulate input data for
    various functions that require a DataFrame as input.

    Returns:
        pd.DataFrame: A mock DataFrame with predefined data.
    """
    data = {
        "pg_id": [1, 2, 3, 4],
        "col": [1, 2, 3, 4],
        "row": [1, 2, 3, 4],
        "month_id": [1, 1, 2, 2],
        "c_id": [1, 1, 1, 1],
        "ln_sb_best": [0.1, 0.2, 0.3, 0.4],
        "ln_ns_best": [0.2, 0.3, 0.4, 0.5],
        "ln_os_best": [0.3, 0.4, 0.5, 0.6],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_vol():
    """
    Fixture to create a mock volume.

    This fixture creates a mock 4D numpy array (volume) with random values for testing
    purposes. The volume has dimensions (2, 180, 180, 8), simulating a 3D spatial grid
    over 2 time steps with 8 features.

    Returns:
        np.ndarray: A mock 4D numpy array with random values.
    """
    return np.random.rand(2, 180, 180, 8)


def test_get_requried_columns_for_vol():
    """
    Test the get_requried_columns_for_vol function.

    This test verifies that the get_requried_columns_for_vol function returns a list
    of required column names for volume conversion. It checks that the returned value
    is a list of strings.

    Raises:
        AssertionError: If the returned value is not a list or if any element in the list
                        is not a string.
    """
    required_columns = get_requried_columns_for_vol()
    assert isinstance(required_columns, list)
    assert all(isinstance(col, str) for col in required_columns)


def test_calculate_absolute_indices(mock_df):
    """
    Test the calculate_absolute_indices function.

    This test verifies that the calculate_absolute_indices function correctly calculates
    the absolute indices for rows, columns, and months. It checks that the output DataFrame
    contains the new columns abs_row, abs_col, and abs_month, and that these columns are
    correctly calculated based on the input DataFrame.

    Args:
        mock_df (pd.DataFrame): A mock DataFrame with predefined data.

    Raises:
        AssertionError: If the output is not a DataFrame, if the new columns are not present,
                        or if the values in the new columns are not correctly calculated.
    """
    df = calculate_absolute_indices(mock_df)
    assert isinstance(df, pd.DataFrame)
    assert "abs_row" in df.columns
    assert "abs_col" in df.columns
    assert "abs_month" in df.columns
    assert df["abs_row"].equals(df["row"] - df["row"].min())
    assert df["abs_col"].equals(df["col"] - df["col"].min())
    assert df["abs_month"].equals(df["month_id"] - df["month_id"].min())


def test_df_to_vol(mock_df):
    """
    Test the df_to_vol function.

    This test verifies that the df_to_vol function correctly converts a DataFrame into
    a 4D numpy array (volume). It checks that the output is a numpy array with the expected
    shape and that the volume contains the correct data based on the input DataFrame.

    Args:
        mock_df (pd.DataFrame): A mock DataFrame with predefined data.

    Raises:
        AssertionError: If the output is not a numpy array or if the shape of the array
                        is not as expected.
    """
    vol = df_to_vol(mock_df)
    assert isinstance(vol, np.ndarray)
    assert vol.shape == (2, 180, 180, 8)


def test_vol_to_df(mock_vol):
    """
    Test the vol_to_df function.

    This test verifies that the vol_to_df function correctly converts a 4D numpy array
    (volume) back into a DataFrame. It checks that the output is a DataFrame with the
    expected columns and that the DataFrame contains the correct data based on the input
    volume.

    Args:
        mock_vol (np.ndarray): A mock 4D numpy array with random values.

    Raises:
        AssertionError: If the output is not a DataFrame or if the columns of the DataFrame
                        do not match the expected columns.
    """
    df = vol_to_df(mock_vol)
    assert isinstance(df, pd.DataFrame)
    required_columns = get_requried_columns_for_vol()
    forecast_features = ["ln_sb_best", "ln_ns_best", "ln_os_best"]
    expected_columns = required_columns + forecast_features
    assert set(df.columns) == set(expected_columns)


def test_df_vol_conversion_test(mock_df):
    """
    Test the df_vol_conversion_test function.

    This test verifies that the df_vol_conversion_test function correctly converts a
    DataFrame to a volume and back to a DataFrame, and that the original DataFrame and
    the recreated DataFrame are equal. It checks that the DataFrame contains the expected
    columns and that the data is correctly preserved through the conversion process.

    Args:
        mock_df (pd.DataFrame): A mock DataFrame with predefined data.

    Raises:
        AssertionError: If the original DataFrame and the recreated DataFrame are not equal.
    """
    vol = df_to_vol(mock_df)
    df_vol_conversion_test(mock_df, vol)
    df_recreated = vol_to_df(vol)
    required_columns = get_requried_columns_for_vol()
    forecast_features = ["ln_sb_best", "ln_ns_best", "ln_os_best"]
    vol_features = required_columns + forecast_features
    df_trimmed = mock_df[vol_features]
    df_trimmed = df_trimmed.sort_values(by=["pg_id", "month_id"]).reset_index(drop=True)
    df_recreated = df_recreated.sort_values(by=["pg_id", "month_id"]).reset_index(
        drop=True
    )
    assert df_trimmed.equals(df_recreated)


def test_plot_vol(mock_vol):
    """
    Test the plot_vol function.

    This test verifies that the plot_vol function runs without errors and correctly
    generates plots for the given volume. It checks that the function does not raise
    any exceptions during execution.

    Args:
        mock_vol (np.ndarray): A mock 4D numpy array with random values.

    Raises:
        pytest.fail: If the plot_vol function raises any exceptions.
    """
    try:
        plot_vol(mock_vol, month_range=1)
    except Exception as e:
        pytest.fail(f"plot_vol raised an exception: {e}")
