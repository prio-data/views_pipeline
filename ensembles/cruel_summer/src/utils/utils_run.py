import numpy as np
import pandas as pd
import runpy
import logging
from model_path import ModelPath
from views_stepshifter_darts.stepshifter import StepshifterModel
from views_stepshifter_darts.hurdle_model import HurdleModel
from views_forecasts.extensions import *

logger = logging.getLogger(__name__)


def get_model(config, partitioner_dict):
    """
    Get the model based on the algorithm specified in the config
    """

    if config["algorithm"] == "HurdleModel":
        model = HurdleModel(config, partitioner_dict)
    else:
        config["model_reg"] = config["algorithm"]
        model = StepshifterModel(config, partitioner_dict)

    return model


def get_standardized_df(df, config):
    """
    Standardizes the DataFrame of model outputs based on the run type.

    Args:
    - df (pd.DataFrame): The DataFrame of model outputs.
    - config (dict): The configuration dictionary containing the model details.

    Returns:
    - df (pd.DataFrame): The standardized DataFrame of model outputs.
    """
    run_type = config["run_type"]
    steps = config["steps"]
    depvar = config["depvar"]

    # choose the columns to keep based on the run type and replace negative values with 0
    if run_type in ["calibration", "testing"]:
        cols = [depvar] + df.forecasts.prediction_columns
    elif run_type == "forecasting":
        cols = [f"step_pred_{i}" for i in steps]
    df = df.replace([np.inf, -np.inf], 0)[cols]
    df = df.mask(df < 0, 0)

    return df


def get_aggregated_df(dfs, aggregation):
    """
    Aggregates the DataFrames of model outputs based on the specified aggregation method.

    Args:
    - dfs (list of pd.DataFrame): A list of DataFrames of model outputs.
    - aggregation (str): The aggregation method to use (either "mean" or "median").

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
    config = {**hp_config, **meta_config, **dp_config}
    config["run_type"] = args.run_type
    config["saved"] = args.saved
    config["sweep"] = False

    return config


def get_single_model_config(model_name):
    model_path = ModelPath(model_name)
    hp_config = runpy.run_path(model_path.configs / "config_hyperparameters.py")["get_hp_config"]()
    meta_config = runpy.run_path(model_path.configs / "config_meta.py")["get_meta_config"]()
    dp_config = runpy.run_path(model_path.configs / "config_deployment.py")["get_deployment_config"]()

    return {**hp_config, **meta_config, **dp_config}
