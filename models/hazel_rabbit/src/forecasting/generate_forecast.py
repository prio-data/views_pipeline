
from set_partition import get_partitioner_dict

import pandas as pd

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)


from utils import get_raw_data, create_model_time_stamp, save_generated_pred


def forecast_with_model_artifact(config, views_raw):
    """
    Create forecasts using the zero baseline model. Return a DataFrame with the predictions.

    Args:
        config : Configuration object containing parameters and settings.
        views_raw : DataFrame containing the raw data
    """

    partitioner_dict = get_partitioner_dict(config.run_type)
            
    # get the months for the predictions
    first_month = partitioner_dict['predict'][0] #if config.partitioner==True else partitioner_dict['predict'][1]-config.time_steps
    last_month = partitioner_dict['predict'][1]

    views_raw = views_raw[['month_id', 'pg_id', 'month', 'year_id', 'c_id']]  

    views_res = generate_forecast(config, views_raw, first_month, last_month)  

    # add timestamp
    config = create_model_time_stamp(config)

    # save the DataFrame of model outputs
    if config.save_generated == True:
        save_generated_pred(config, views_res)

    return views_res




def generate_forecast(config, views_raw, first_month, last_month):
    # get the unique grids as a Series
    unique_grids = views_raw['pg_id'].unique()
    
    # create the next 36 months for these grids
    next_months = pd.DataFrame({
        'pg_id': unique_grids.repeat(config.time_steps),
        'month_id': [month for _ in unique_grids for month in range(first_month, last_month)]  
    })

    # assign the sequence from 1 to 36 for the new months
    next_months['out_sample_months'] = next_months.groupby('pg_id').cumcount() + 1
    next_months['y_pred'] = 0

    return next_months