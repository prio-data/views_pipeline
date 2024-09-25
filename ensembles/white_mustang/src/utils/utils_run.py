import numpy as np
from views_forecasts.extensions import *

import logging
logging.basicConfig(filename='../../run.log', encoding='utf-8', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_standardized_df(df, config):
    """
    Standardizes the DataFrame of model outputs based on the run type.

    Args:
    - df (pd.DataFrame): The DataFrame of model outputs.
    - config (dict): The configuration dictionary containing the model details.

    Returns:
    - df (pd.DataFrame): The standardized DataFrame of model outputs.
    """
    run_type = config['run_type']
    steps = config['steps']
    depvar = config['depvar']

    # choose the columns to keep based on the run type and replace negative values with 0
    if run_type in ['calibration', 'testing']:
        cols = [depvar] + df.forecasts.prediction_columns
    elif run_type == "forecasting":
        cols = [f'step_pred_{i}' for i in steps]
    df = df.replace([np.inf, -np.inf], 0)[cols]
    df = df.mask(df < 0, 0)

    return df


def get_aggregated_df(dfs, aggregation):
    """
    Aggregates the DataFrames of model outputs based on the specified aggregation method.

    Args:
    - dfs (list of pd.DataFrame): A list of DataFrames of model outputs.
    - aggregation (str): The aggregation method to use (either 'mean' or 'median').

    Returns:
    - df (pd.DataFrame): The aggregated DataFrame of model outputs.
    """
    if aggregation == "mean":
        return pd.concat(dfs).groupby(level=[0, 1]).mean()
    elif aggregation == "median":
        return pd.concat(dfs).groupby(level=[0, 1]).median()
    else:
        logger.error(f"Invalid aggregation: {aggregation}")


def update_config(hp_config, meta_config, dp_config, args):
    config = hp_config.copy()
    config['run_type'] = args.run_type
    config['aggregation'] = meta_config['aggregation']
    config['name'] = meta_config['name']
    config['models'] = meta_config['models']
    config['depvar'] = meta_config['depvar']
    config['deployment_status'] = dp_config['deployment_status']

    return config