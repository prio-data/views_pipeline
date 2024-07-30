import sys
import numpy as np
from pathlib import Path
import pickle

PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)

from set_partition import get_partitioner_dict
from views_forecasts.extensions import *


def get_partition_data(df, run_type):
    partitioner_dict = get_partitioner_dict(run_type)

    month_first = partitioner_dict['train'][0]

    if run_type in ['calibration', 'testing', 'forecasting']:
        # predict[1] is the last month to predict, so we need to add 1 to include it.
        # forecasting also needs to get predict months even if they are empty
        month_last = partitioner_dict['predict'][1] + 1
    else:
        raise ValueError('partition should be either "calibration", "testing" or "forecasting"')

    month_range = np.arange(month_first, month_last, 1)

    df = df[df.index.get_level_values("month_id").isin(month_range)].copy()  # temporal subset

    return df

def get_standardized_df(df, run_type):
    if run_type in ['calibration', 'testing']:
        cols = [df.forecasts.target] + df.forecasts.prediction_columns
    elif run_type == "forecasting":
        cols = df.forecasts.prediction_columns
    df = df.replace([np.inf, -np.inf], 0)[cols]
    df = df.mask(df < 0, 0)
    return df

def get_aggregated_df(dfs, aggregation):
    if aggregation == "mean":
        return pd.concat(dfs).groupby(level=[0, 1]).mean()
    elif aggregation == "median":
        return pd.concat(dfs).groupby(level=[0, 1]).median()
    else:
        raise ValueError(f"Invalid aggregation: {aggregation}")


def save_model_outputs(df_evaluation, df_output, PATH_GENERATED, config):
    Path(PATH_GENERATED).mkdir(parents=True, exist_ok=True)
    # print(f'PATH to generated data: {PATH_GENERATED}')

    # Save the DataFrame of model outputs
    outputs_path = f'{PATH_GENERATED}/df_output_{config.steps[-1]}_{config.run_type}_{config.timestamp}.pkl'
    with open(outputs_path, 'wb') as file:
        pickle.dump(df_output, file)

    # Save the DataFrame of evaluation metrics
    evaluation_path = f'{PATH_GENERATED}/df_evaluation_{config.steps[-1]}_{config.run_type}_{config.timestamp}.pkl'
    with open(evaluation_path, 'wb') as file:
        pickle.dump(df_evaluation, file)


