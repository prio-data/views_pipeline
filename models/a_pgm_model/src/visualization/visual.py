# add script to visualize the results stored in the generated folder

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from .map_config import visual_config as map_config
import numpy as np

def visualize_forecasts_in_maps(step) -> None:
    """
    This function visualizes the forecasts in maps for a given step. It takes the step as an input and plots the map for
    the given step. The map is then saved in the reports/plots/maps folder.
    
    Args:
        step: int
            The step for which the map is to be plotted.
    Returns: 
        None           
    """
    
    # Load the forecast data
    latest_forecasts = pd.read_parquet(map_config['forecast_path'])
    converted_forecast_to_raw_from_log = np.exp(latest_forecasts)-1

    # Reset the index of latest_forecasts and then set 'priogrid_gid' as the index
    latest_forecasts.reset_index(inplace=True)
    latest_forecasts.set_index('priogrid_gid', inplace=True)

    converted_forecast_to_raw_from_log.reset_index(inplace=True)
    converted_forecast_to_raw_from_log.set_index('priogrid_gid', inplace=True)
    
    # Load the map shapefile from local shape file
    world = gpd.read_file(map_config['shapefile_path'])

    # Merge the forecast data with the world map data
    merged = world.set_index('priogrid_i').join(latest_forecasts)

    # Plot the merged data
    fig, ax = plt.subplots(1, 1, figsize=map_config['figure_size'],dpi = map_config['dpi'])
    merged.plot(column=f'step_pred_{step}', ax=ax, legend=True)

    # Save the plot in a folder
    output_dir = map_config['output_dir']
    fig.savefig(f'{output_dir}/map_step_{step}.png')

    # get the second axes which is the colorbar
    colorbar = plt.gcf().get_axes()[1]
    colorbar.set_ylabel('Fatalities in log scale')
    
    merged_raw_forecasts = world.set_index('priogrid_i').join(converted_forecast_to_raw_from_log)
    
    fig, ax = plt.subplots(1, 1, figsize=map_config['figure_size'],dpi = map_config['dpi'])
    merged_raw_forecasts.plot(column=f'step_pred_{step}', ax=ax, legend=True)
    output_dir = map_config['output_dir']
    fig.savefig(f'{output_dir}/map_step_{step}_raw.png')
    
    # get the second axes which is the colorbar
    colorbar = plt.gcf().get_axes()[1]
    colorbar.set_ylabel('Fatalities in raw scale')
    
    plt.show()
