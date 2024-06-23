
from set_partition import get_partitioner_dict

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)


from utils import get_raw_data, create_model_time_stamp, save_generated_pred


def evaluate_model_artifact(config, views_raw):
    """
    Create predictions using the zero baseline model. Return a DataFrame with the predictions.

    Args:
        config : Configuration object containing parameters and settings.
        views_raw : DataFrame containing the raw data
    """

    partitioner_dict = get_partitioner_dict(config.run_type)
            
    # get the months for the predictions
    first_month = partitioner_dict['predict'][0] if config.partitioner==True else partitioner_dict['predict'][1]-config.time_steps
    last_month = partitioner_dict['predict'][1]

    # apply the function to each grid group
    views_res = views_raw.groupby('pg_id').apply(create_months_index, config=config).reset_index(drop=True)

    # add 0 prediction
    views_res['y_pred'] = 0

    # add timestamp
    config = create_model_time_stamp(config)

    # save the DataFrame of model outputs
    if config.save_generated == True:
        save_generated_pred(config, views_res)

    return views_res



def create_months_index(group_df, config):
    """
    Add a new column (named 'out_sample_months') to a DataFrame with the numbers from 1 to config.time_steps.

    Args:
        group_df : DataFrame grouped by the grid id ('pg_id').
        config : Configuration object containing parameters and settings.
    """

    group_df = group_df.sort_values(by='month_id').tail(config.time_steps)
    group_df['out_sample_months'] = range(1, config.time_steps + 1)

    return group_df