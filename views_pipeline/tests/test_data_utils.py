import pytest
import pandas as pd
import numpy as np
from views_pipeline.data.utils import ensure_float64

def test_ensure_float64_all_float64():
    """
    Test ensure_float64 with a DataFrame that already has all np.float64 columns.
    """
    df = pd.DataFrame({
        'a': np.array([1.0, 2.0, 3.0], dtype=np.float64),
        'b': np.array([4.0, 5.0, 6.0], dtype=np.float64)
    })
    result = ensure_float64(df)
    assert result.dtypes['a'] == np.float64
    assert result.dtypes['b'] == np.float64

def test_ensure_float64_mixed_types():
    """
    Test ensure_float64 with a DataFrame that has some non-np.float64 numeric columns.
    """
    df = pd.DataFrame({
        'a': np.array([1, 2, 3], dtype=np.int32),
        'b': np.array([4.0, 5.0, 6.0], dtype=np.float64),
        'c': np.array([7.0, 8.0, 9.0], dtype=np.float32)
    })
    result = ensure_float64(df)
    assert result.dtypes['a'] == np.float64
    assert result.dtypes['b'] == np.float64
    assert result.dtypes['c'] == np.float64

def test_ensure_float64_no_numeric():
    """
    Test ensure_float64 with a DataFrame that has no numeric columns.
    """
    df = pd.DataFrame({
        'a': ['x', 'y', 'z'],
        'b': ['foo', 'bar', 'baz']
    })
    result = ensure_float64(df)
    assert result.dtypes['a'] == object
    assert result.dtypes['b'] == object

def test_ensure_float64_empty():
    """
    Test ensure_float64 with an empty DataFrame.
    """
    df = pd.DataFrame()
    result = ensure_float64(df)
    assert result.empty