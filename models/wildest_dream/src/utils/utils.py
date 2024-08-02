import sys
import numpy as np
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
import pickle

PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths
setup_project_paths(PATH)

from hurdle_model import HurdleRegression
from set_partition import get_partitioner_dict
from views_forecasts.extensions import *


def ensure_float64(df):
    """
    Check if the DataFrame only contains np.float64 types. If not, raise a warning
    and convert the DataFrame to use np.float64 for all its numeric columns.
    """
    
    non_float64_cols = df.select_dtypes(include=['number']).columns[df.select_dtypes(include=['number']).dtypes != np.float64]

    if len(non_float64_cols) > 0:
        print(f"Warning: DataFrame contains non-np.float64 numeric columns. Converting the following columns: {', '.join(non_float64_cols)}")

        for col in non_float64_cols:
            df[col] = df[col].astype(np.float64)

    return df


def get_model(config):
    if config["algorithm"] == "HurdleRegression":
        model = HurdleRegression(clf_name=config["model_clf"], reg_name=config["model_reg"],
                                 clf_params=config["parameters"]["clf"], reg_params=config["parameters"]["reg"])
    else:
        parameters = get_parameters(config)
        model = globals()[config["algorithm"]](**parameters)
    return model


def get_parameters(config):
    '''
    Get the parameters from the config file.
    If not sweep, then get directly from the config file, otherwise have to remove some parameters.
    '''

    if config["sweep"]:
        keys_to_remove = ["algorithm", "depvar", "steps", "sweep", "run_type", "model_cls", "model_reg"]
        parameters = {k: v for k, v in config.items() if k not in keys_to_remove}
    else:
        parameters = config["parameters"]

    return parameters


def get_partition_data(df, run_type):
    partitioner_dict = get_partitioner_dict(run_type)

    month_first = partitioner_dict['train'][0]

    if run_type in ['calibration', 'testing']:
        month_last = partitioner_dict['predict'][1] + 1
    elif run_type == 'forecasting':
        month_last = partitioner_dict['predict'][0]
    else:
        raise ValueError('partition should be either "calibration", "testing" or "forecasting"')

    month_range = np.arange(month_first, month_last, 1)  # predict[1] is the last month to predict, so we need to add 1 to include it.

    df = df[df.index.get_level_values("month_id").isin(month_range)].copy()  # temporal subset

    return df


def get_standardized_df(df, config):
    run_type = config['run_type']
    steps = config['steps']
    if run_type in ['calibration', 'testing']:
        cols = [df.forecasts.target] + df.forecasts.prediction_columns
    elif run_type == "forecasting":
        cols = [f'step_pred_{i}' for i in steps]
    df = df.replace([np.inf, -np.inf], 0)[cols]
    df = df.mask(df < 0, 0)
    return df


def save_model_outputs(df_evaluation, df_output, PATH_GENERATED, config):
    Path(PATH_GENERATED).mkdir(parents=True, exist_ok=True)
    print(f'PATH to generated data: {PATH_GENERATED}')

    # Save the DataFrame of model outputs
    outputs_path = f"{PATH_GENERATED}/df_output_{config['steps'][-1]}_{config['run_type']}_{config['timestamp']}.pkl"
    with open(outputs_path, 'wb') as file:
        pickle.dump(df_output, file)

    # Save the DataFrame of evaluation metrics
    evaluation_path = f"{PATH_GENERATED}/df_evaluation_{config['steps'][-1]}_{config['run_type']}_{config['timestamp']}.pkl"
    with open(evaluation_path, 'wb') as file:
        pickle.dump(df_evaluation, file)


def split_hurdle_parameters(parameters_dict):
    """
    Split the parameters dictionary into two separate dictionaries, one for the
    classification model and one for the regression model. 
    """

    cls_dict = {}
    reg_dict = {}
    
    for key, value in parameters_dict.items():
        if key.startswith('cls_'):
            cls_key = key.replace('cls_', '')
            cls_dict[cls_key] = value
        elif key.startswith('reg_'):
            reg_key = key.replace('reg_', '')
            reg_dict[reg_key] = value
            
    return cls_dict, reg_dict


def update_hp_config(hp_config, args, meta_config):
    hp_config['run_type'] = args.run_type
    hp_config['sweep'] = False
    hp_config['name'] = meta_config['name']
    hp_config['depvar'] = meta_config['depvar']
    hp_config['algorithm'] = meta_config['algorithm']
    if meta_config['algorithm'] == 'HurdleRegression':
        hp_config['model_clf'] = meta_config['model_clf']
        hp_config['model_reg'] = meta_config['model_reg']

        
def update_sweep_config(sweep_config, args, meta_config):
    sweep_config['parameters']['run_type'] = {'value': args.run_type}
    sweep_config['parameters']['sweep'] = {'value': True}
    sweep_config['parameters']['depvar'] = {'value': meta_config['depvar']}
    sweep_config['parameters']['algorithm'] = {'value': meta_config['algorithm']}
    if meta_config['algorithm'] == 'HurdleRegression':
        sweep_config['parameters']['model_clf'] = {'value': meta_config['model_clf']}
        sweep_config['parameters']['model_reg'] = {'value': meta_config['model_reg']}