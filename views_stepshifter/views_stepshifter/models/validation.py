import functools
import numpy as np
import pandas as pd
import logging
from views_forecasts.extensions import *

logger = logging.getLogger(__name__)


def dataframe_is_right_format(dataframe: pd.DataFrame):
    try:
        assert len(dataframe.index.levels) == 2
        # print("The dataframe has a two-level index")
    except AssertionError:
        logger.exception("Dataframe must have a two-level index")
        raise AssertionError("Dataframe must have a two-level index")
        
    try:
        assert dataframe.index.names[0] == "month_id"
        # print("The first level of the index is correct")
    except AssertionError:
        logger.exception("The first level of the index must be 'month_id'")
        raise AssertionError("The first level of the index must be 'month_id'")
    
    try:
        assert dataframe.index.names[1] in ["country_id", "priogrid_gid"]
        # print("The second level of the index is correct")
    except AssertionError:
        logger.exception("The second level of the index must be 'country_id' or 'priogrid_gid'")
        raise AssertionError("The second level of the index must be 'country_id' or 'priogrid_gid'")

    try:
        assert set(dataframe.dtypes) == {np.dtype(float)}
        # print("The dataframe contains only np.float64 floats")
    except AssertionError:
        logger.exception("The dataframe must contain only np.float64 floats")
        raise AssertionError("The dataframe must contain only np.float64 floats")
    

def views_validate(fn):
    @functools.wraps(fn)
    def inner(*args,**kwargs):
        dataframe_is_right_format(args[-1])
        return fn(*args, **kwargs)
    return inner