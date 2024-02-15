# Use viewser env

import sys

from viewser import Queryset, Column
from ingester3.ViewsMonth import ViewsMonth

import os
import pickle

import numpy as np
import pandas as pd


# Set the base path relative to the current script location
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(f'working int {base_path}')

# Add the required directories to the system path
sys.path.insert(0, os.path.join(base_path, "architectures"))
sys.path.insert(0, os.path.join(base_path, "configs"))
sys.path.insert(0, os.path.join(base_path, "utils"))  

from config_hyperparameters import get_hp_config
from config_partitioner import get_partitioner_dict
from utils_dataloaders import get_views_date, df_to_vol


# def get_views_date():
# 
#     print('Beginning file download through viewser...')
# 
#     queryset_base = (Queryset("simon_tests", "priogrid_month")
#         .with_column(Column("ln_sb_best", from_table = "ged2_pgm", from_column = "ged_sb_best_count_nokgi").transform.ops.ln().transform.missing.replace_na())
#         .with_column(Column("ln_ns_best", from_table = "ged2_pgm", from_column = "ged_ns_best_count_nokgi").transform.ops.ln().transform.missing.replace_na())
#         .with_column(Column("ln_os_best", from_table = "ged2_pgm", from_column = "ged_os_best_count_nokgi").transform.ops.ln().transform.missing.replace_na())
#         .with_column(Column("month", from_table = "month", from_column = "month"))
#         .with_column(Column("year_id", from_table = "country_year", from_column = "year_id"))
#         .with_column(Column("c_id", from_table = "country_year", from_column = "country_id"))
#         .with_column(Column("col", from_table = "priogrid", from_column = "col"))
#         .with_column(Column("row", from_table = "priogrid", from_column = "row")))
# 
# 
#     df = queryset_base.publish().fetch()
# 
#     df.reset_index(inplace = True)
# 
#     df.rename(columns={'priogrid_gid': 'pg_id'}, inplace= True)
# 
#     df['in_viewser'] = True
# 
#     month_first = df[df['year_id'] == 1990]['month_id'].min() # Jan 1990
#     month_last =  ViewsMonth.now().id - 2 # minus 1 because the current month is not yet available,
# 
#     df = df[df['month_id'] <= month_last].copy()
#     df.loc[:,'abs_row'] = df.loc[:,'row'] - df.loc[:,'row'].min() 
#     df.loc[:,'abs_col'] = df.loc[:,'col'] - df.loc[:,'col'].min()
#     df.loc[:,'abs_month'] = df.loc[:,'month_id'] - month_first  
#     #partitioner_dict = {"train":(121,396),"predict":(397,444)} # calib_partitioner_dict - (01/01/1990 - 12/31/2012) : (01/01/2013 - 31/12/2015)
#  
#     partitioner_dict = get_partitioner_dict('calibration')
# 
#     month_range = np.arange(partitioner_dict['train'][0], partitioner_dict['predict'][1]+1,1)
# 
#     df = df[df['month_id'].isin(month_range)] # temp sub
#  
#     return df
# 
# 
# def df_to_vol(df):
# 
#     month_first = df['month_id'].min() # Jan 1990
#     month_last =  df['month_id'].max() # minus 1 because the current month is not yet available,
# 
#     month_range = month_last - month_first + 1
#     space_range = 180
# 
#     features_num = 8 # should be inferred from the number of columns in the dataframe... 
#     
#     
#     vol = np.zeros([space_range, space_range, month_range, features_num])
#     
#     vol[df['abs_row'], df['abs_col'], df['abs_month'], 0] = df['pg_id']
#     vol[df['abs_row'], df['abs_col'], df['abs_month'], 1] = df['col'] # this is not what I want, I want the xcoord but...
#     vol[df['abs_row'], df['abs_col'], df['abs_month'], 2] = df['row'] # this is not what I want, I want the ycoord but...
#     vol[df['abs_row'], df['abs_col'], df['abs_month'], 3] = df['month_id']
#     vol[df['abs_row'], df['abs_col'], df['abs_month'], 4] = df['c_id']
#     vol[df['abs_row'], df['abs_col'], df['abs_month'], 5] = df['ln_sb_best']
#     vol[df['abs_row'], df['abs_col'], df['abs_month'], 6] = df['ln_ns_best']
#     vol[df['abs_row'], df['abs_col'], df['abs_month'], 7] = df['ln_os_best']
#     
#     vol = np.flip(vol, axis = 0) # flip the rows, so north is up.
#     vol = np.transpose(vol, (2,0,1,3) ) # move the month dim to the front. Could just do it above but..  # move the month dim to the front. Could just do it above but.. should be something like (324, 180, 180, 8)
#     
#     print(f'Volume of shape {vol.shape} created. Should be (n_month, 180, 180, 8)')
# 
#  
#     return vol
# 
if __name__ == "__main__":
    
    # processed_location = '/home/simon/Documents/scripts/conflictNet/data/processed' # local
    # raw_location = '/home/simon/Documents/scripts/conflictNet/data/raw' # local

    #processed_location = '/home/simmaa/HydraNet_001/data/processed' # server
    #raw_location = '/home/simmaa/HydraNet_001/data/raw' # server

    partition = 'calibration'

    config = get_hp_config()

    processed_location = config['path_processed_data']
    raw_location = config['path_raw_data']

    path_viewser_data = raw_location + '/calibration_viewser_data.pkl'
    path_vol = processed_location +  '/calibration_vol.npy'

    # create the folders if they don't exist
    if not os.path.exists(raw_location):
        os.makedirs(raw_location)

    if not os.path.exists(processed_location):
        os.makedirs(processed_location)

    # check if the VIEWSER files exist
    if os.path.isfile(path_viewser_data) == True:

        print('File already downloaded')
        df = pd.read_pickle(path_viewser_data)
    
    else:
        print('Downloading file...')
        df = get_views_date(partition)

        # save pkl
        print(f'Saving file to {path_viewser_data}')
        df.to_pickle(path_viewser_data)

    # check if the volume exists
    if os.path.isfile(path_vol) == True:

        print('Volume already created')
        vol = np.load(path_vol)

    else:
        print('Creating volume...')

        # create volume
        vol = df_to_vol(df)

        print(f'shape of volume: {vol.shape}')
        print(f'Saving volume to {path_vol}')
        # save npy
        np.save(path_vol, vol)

    print('Done')
    