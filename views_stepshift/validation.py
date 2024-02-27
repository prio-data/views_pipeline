import functools
import numpy as np
import pandas as pd

class ValidationError(Exception):
    pass

def dataframe_is_right_format(dataframe: pd.DataFrame):
    try:
        assert len(dataframe.index.levels) == 2
    except AssertionError:
        raise ValidationError("Dataframe must have a two-level index")

    try:
        assert set(dataframe.dtypes) == {np.dtype(float)}
    except AssertionError:
        raise ValidationError("The dataframe must contain only np.float64 floats")

def views_validate(fn):
    @functools.wraps(fn)
    def inner(*args,**kwargs):
        dataframe_is_right_format(args[-1])
        return fn(*args,**kwargs)
    return inner
