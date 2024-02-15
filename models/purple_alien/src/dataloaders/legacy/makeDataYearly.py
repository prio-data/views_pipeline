import numpy as np
import pandas as pd
import geopandas as gpd
import pickle
import urllib.request

# run with geo_env

def get_data(location):

    # Getting and loading views data
    print('Beginning file download UCDP...')

    url_ucdp = 'https://ucdp.uu.se/downloads/ged/ged201-csv.zip'
    path_ucdp = location + "/ged201-csv.zip"
    urllib.request.urlretrieve(url_ucdp, path_ucdp)


    # Getting and loading prio data
    print('Beginning file download PRIO...')

    url_prio = 'http://file.prio.no/ReplicationData/PRIO-GRID/priogrid_shapefiles.zip'
    path_prio = location + '/priogrid_shapefiles.zip'
    urllib.request.urlretrieve(url_prio, path_prio)

    # And move to correct location on computerome
    # gpd.read_file('zip://' + path_prio)
    prio_grid = gpd.read_file('zip://' + path_prio)
    ucdp = pd.read_csv(path_ucdp)

    return prio_grid, ucdp

def trim_ucdp(ucdp):

    ucdp_slim = ucdp[['year','priogrid_gid','best','low','high']]
    ucdp_gid = ucdp_slim.groupby(by=['priogrid_gid','year']).sum().reset_index()
    ucdp_gid.rename(columns={'priogrid_gid':'gid'}, inplace=True)

    ucdp_gid['log_best'] = np.log(ucdp_gid['best'] +1)
    ucdp_gid['log_low'] = np.log(ucdp_gid['low'] +1)
    ucdp_gid['log_high'] = np.log(ucdp_gid['high'] +1)

    return ucdp_gid


def elong_df(df, df_w_years):

    years = sorted(df_w_years['year'].unique())
    df['year'] = years[0]
    concat_df = df.copy()

    for i,j in enumerate(years[1:]):

        df_temp = df.copy()
        df_temp['year'] = j

        concat_df = pd.concat([concat_df,df_temp])
    
    concat_df.reset_index(inplace = True)
    return concat_df 


def make_df(prio_grid, ucdp):

    print('Creating DF...')

    ucdp_gid = trim_ucdp(ucdp=ucdp)
    prio_grid_yearly = elong_df(prio_grid, ucdp_gid)

    grid_ucdp =  pd.merge(prio_grid_yearly, ucdp_gid, how = 'left', on = ['gid', 'year'])
    grid_ucdp.fillna({'best' : 0, 'low' : 0, 'high' : 0, 'log_best' : 0, 'log_low' : 0, 'log_high' : 0}, inplace = True)

    grid_ucdp = grid_ucdp[['gid', 'xcoord', 'ycoord', 'year', 'best', 'low', 'high', 'log_best', 'log_low', 'log_high']].copy() # remove the everything also the geo col.

    grid_ucdpS = grid_ucdp.sort_values(['year', 'ycoord', 'xcoord'], ascending = [True, False, True])

    # try to keep the jazz
    #grid_ucdpS = grid_ucdpS[['gid','best', 'low',  'high', 'log_best', 'log_low', 'log_high']].copy() # remove the everything also the geo col. But keep gid. Why not.

    x_dim = grid_ucdp['xcoord'].unique().shape[0]
    y_dim = grid_ucdp['ycoord'].unique().shape[0]
    z_dim = grid_ucdp['year'].unique().shape[0]

    ucpd_vol = np.array(grid_ucdpS).reshape((z_dim, y_dim, x_dim, -1))

    return ucpd_vol

# --------------------------------------------------------------

location = '/home/projects/ku_00017/data/raw/conflictNet'
#location = '/home/simon/Documents/Articles/ConflictNet/data/raw'

prio_grid, ucdp = get_data(location)
ucpd_vol = make_df(prio_grid = prio_grid, ucdp=ucdp)

print('Saving pickle')
file_name = "/ucpd_vol.pkl"
output = open(location + file_name, 'wb')
pickle.dump(ucpd_vol, output)
output.close()

print('Done')