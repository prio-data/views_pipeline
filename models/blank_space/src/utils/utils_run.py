import numpy as np
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestClassifier
from hurdle_model import HurdleRegression
from views_forecasts.extensions import *


def get_model(config):
    """
    Get the model based on the algorithm specified in the config
    """

    if config["algorithm"] == "HurdleRegression":
        model = HurdleRegression(clf_name=config["model_clf"], reg_name=config["model_reg"],
                                 clf_params=config["parameters"]["clf"], reg_params=config["parameters"]["reg"])
    else:
        parameters = get_parameters(config)
        model = globals()[config["algorithm"]](**parameters)

    return model


def get_parameters(config):
    """
    Get the parameters from the config file.
    If not sweep, then get directly from the config file, otherwise have to remove some parameters.
    """

    if config["sweep"]:
        keys_to_remove = ["algorithm", "depvar", "steps", "sweep", "run_type", "model_cls", "model_reg"]
        parameters = {k: v for k, v in config.items() if k not in keys_to_remove}
    else:
        parameters = config["parameters"]

    return parameters


def get_standardized_df(df, config):
    """
    Standardize the DataFrame based on the run type
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


def split_hurdle_parameters(parameters_dict):
    """
    Split the parameters dictionary into two separate dictionaries, one for the
    classification model and one for the regression model.
    """

    cls_dict = {}
    reg_dict = {}

    for key, value in parameters_dict.items():
        if key.startswith("cls_"):
            cls_key = key.replace("cls_", "")
            cls_dict[cls_key] = value
        elif key.startswith("reg_"):
            reg_key = key.replace("reg_", "")
            reg_dict[reg_key] = value

    return cls_dict, reg_dict


def update_config(hp_config, meta_config, dp_config, args):
    config = hp_config.copy()
    config["run_type"] = args.run_type
    config["sweep"] = False
    config["name"] = meta_config["name"]
    config["depvar"] = meta_config["depvar"]
    config["algorithm"] = meta_config["algorithm"]
    if meta_config["algorithm"] == "HurdleRegression":
        config["model_clf"] = meta_config["model_clf"]
        config["model_reg"] = meta_config["model_reg"]
    config["deployment_status"] = dp_config["deployment_status"]

    return config


def update_sweep_config(sweep_config, args, meta_config):
    sweep_config["parameters"]["run_type"] = {"value": args.run_type}
    sweep_config["parameters"]["sweep"] = {"value": True}
    sweep_config["parameters"]["name"] = {"value": meta_config["name"]}
    sweep_config["parameters"]["depvar"] = {"value": meta_config["depvar"]}
    sweep_config["parameters"]["algorithm"] = {"value": meta_config["algorithm"]}
    if meta_config["algorithm"] == "HurdleRegression":
        sweep_config["parameters"]["model_clf"] = {"value": meta_config["model_clf"]}
        sweep_config["parameters"]["model_reg"] = {"value": meta_config["model_reg"]}
