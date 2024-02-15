import pandas as pd
import numpy as np
from views_forecasts.extensions import *

def get_standardized_df(df):
    '''
    Standardize the dataframe to have the same columns as the forecast dataframe, i.e., the target and prediction columns
    '''

    cols = [df.forecasts.target] + df.forecasts.prediction_columns
    return df[cols]

    
