# Use viewser env

from viewser import Queryset, Column
from ingester3.extensions import *
#from ingester3.DBWriter import DBWriter

import urllib.request
import os
import sys

import requests

import pickle
import numpy as np
import pandas as pd
import geopandas as gpd


def get_views_date(location, file_name):

    path_views_data = location + file_name

    if os.path.isfile(path_views_data) == True:

        print('File already downloaded')
        df = pd.read_pickle(path_views_data)
        
    else:
        print('Beginning file download through viewser...')


        queryset_base = (Queryset("simon_tests", "priogrid_month")
            .with_column(Column("ln_sb_best", from_table = "ged2_pgm", from_column = "ged_sb_best_count_nokgi").transform.ops.ln().transform.missing.replace_na())
            .with_column(Column("ln_ns_best", from_table = "ged2_pgm", from_column = "ged_ns_best_count_nokgi").transform.ops.ln().transform.missing.replace_na())
            .with_column(Column("ln_os_best", from_table = "ged2_pgm", from_column = "ged_os_best_count_nokgi").transform.ops.ln().transform.missing.replace_na())
            .with_column(Column("month", from_table = "month", from_column = "month"))
            .with_column(Column("year_id", from_table = "country_year", from_column = "year_id"))
            .with_column(Column("c_id", from_table = "country_year", from_column = "country_id")))


        df = queryset_base.publish().fetch()

        df.reset_index(inplace = True)

        df.rename(columns={'priogrid_gid': 'pg_id'}, inplace= True)

        #month_range = np.arange(partitioner_dict['train'][0], partitioner_dict['predict'][1]+1,1)
        #month_range = np.arange(partitioner_dict['train'][0],partitioner_dict['train'][0]+21,1)


        #df = df[df['month_id'].isin(month_range)] # temp sub
        df['in_viewser'] = True

    return df


def get_prio_shape(location):

    path_prio = location + '/priogrid_shapefiles.zip'


    if os.path.isfile(path_prio) == True:
        
        print('File already downloaded')
        prio_grid = gpd.read_file('zip://' + path_prio)

        prio_grid =  pd.DataFrame(prio_grid.drop(columns = ['geometry']))

    else:
        print('Beginning file download PRIO...')


        url_prio = 'http://file.prio.no/ReplicationData/PRIO-GRID/priogrid_shapefiles.zip'
        print(f'from {url_prio}')
        print(f'saving to {path_prio}')
        # urllib.request.urlretrieve(url_prio, path_prio) # old

        # New: ------
        # Set the timeout duration in seconds
        timeout_duration = 60

        try:
            response = requests.get(url_prio, timeout=timeout_duration)
            with open(path_prio, 'wb') as file:
                file.write(response.content)

        except requests.exceptions.RequestException as e:
            print("Error:", e)
        # ------

        prio_grid = gpd.read_file('zip://' + path_prio)

        prio_grid =  pd.DataFrame(prio_grid.drop(columns = ['geometry']))

    prio_grid.rename(columns={'gid': 'pg_id'}, inplace= True)

    return prio_grid


def monthly_grid(prio_grid, views_df):

    years = [sorted(views_df['year_id'].unique())] * prio_grid.shape[0]

    months = [sorted(views_df['month'].unique())] * prio_grid.shape[0] # then you only get one for the test runs# expensive to get these

    prio_grid['year_id'] = years
    prio_grid['month'] = months

    prio_grid = prio_grid.explode('year_id').reset_index(drop=True) 
    prio_grid = prio_grid.explode('month').reset_index(drop=True) 

    prio_grid['year_id'] = prio_grid['year_id'].astype(int)
    prio_grid['month'] = prio_grid['month'].astype(int)


    full_grid = prio_grid.merge(views_df, on = ['pg_id', 'year_id', 'month'], how = 'left')

    full_grid.fillna({'ln_sb_best' : 0, 'ln_ns_best' : 0, 'ln_os_best' : 0, 'c_id' : 0, 'in_viewser' : False}, inplace = True) # for c_id 0 is no country

    full_grid["month_id"] = full_grid.groupby(["year_id", "month"]).apply(lambda x: x.fillna(x.mean(skipna = True)))['month_id']

    # Drop stuff..
    full_grid.dropna(inplace=True)
    # the point of this is to drop months that were not give and month_id. The PRIO grid explosion makes only whole years, so this removes any excess months

    return full_grid


def get_sub_grid(grid, views_df):

        views_gids = views_df['pg_id'].unique()

        # get both dim to 180. Fine since you maxpool(2,2) two time: 180 -> 90 -> 45
        # A better number might be 192 since: 192 -> 96 -> 48 -> 24 -> 12 -> 6 -> 3
        max_coords = grid[grid['pg_id'].isin(views_gids)][['xcoord', 'ycoord']].max() + (1,1) 
        min_coords = grid[grid['pg_id'].isin(views_gids)][['xcoord', 'ycoord']].min() - (1,0.25) 
        
        # Maks it
        mask1 = ((grid['xcoord'] < max_coords[0]) & (grid['xcoord'] > min_coords[0]) & (grid['ycoord'] < max_coords[1]) & (grid['ycoord'] > min_coords[1]))
        grid = grid[mask1].copy()

        return grid


def make_volumn(grid):

    # we start with wat we know - but there is no reason not to try with more down til line.

    sub_df = grid[['pg_id', 'xcoord', 'ycoord', 'month_id', 'c_id', 'ln_sb_best', 'ln_ns_best', 'ln_os_best']].copy() # remove the everything also the geo col. What about in_viewser?

    sub_df_sorted = sub_df.sort_values(['month_id', 'ycoord', 'xcoord'], ascending = [True, False, True])

    x_dim = sub_df['xcoord'].unique().shape[0]
    y_dim = sub_df['ycoord'].unique().shape[0]
    z_dim = sub_df['month_id'].unique().shape[0]

    ucpd_vol = np.array(sub_df_sorted).reshape((z_dim, y_dim, x_dim, -1))

    return ucpd_vol


def compile():

    from pkg_resources import get_distribution
    installed_version = get_distribution('ingester3').version

    if installed_version >= '1.8.1':
        print (f"You are running version {installed_version} which is consistent with the documentation")
    else:
        print (f"""You are running an obsolete version ({installed_version}). Run: pip install ingester3 --upgrade to upgrade""")


    file_name = "/viewser_monthly_vol_forecast_sbnsos.pkl"

    #location = '/home/projects/ku_00017/data/raw/conflictNet' # computerome
    raw_location = '/home/simmaa/HydraNet_001/data/raw' # fimbulthul
    processed_location = '/home/simmaa/HydraNet_001/data/processed' # fimbulthul

    df = get_views_date(processed_location, file_name)
    print('Data loaded from viewser')
    
    grid = get_prio_shape(raw_location)
    print('PRIO-grid loaded')
    
    grid = monthly_grid(grid, df)
    print('PRIO-grid and viewser data merged')
    
    grid = get_sub_grid(grid, df)
    print('Sub-grid partitioned')

    vol = make_volumn(grid)
    print('Created volumn')

    print(f'Pickling {file_name}')
    output = open( processed_location + file_name, 'wb')
    pickle.dump(vol, output)
    output.close()
    print(f'Pickled {file_name}')
    print('Done.')


if __name__ == "__main__":
    compile()
