import numpy as np
import pandas as pd
import geopandas as gpd
import pickle
import urllib.request
import os


def get_gwno():

    location = '/home/projects/ku_00017/data/raw/PRIO'
    #location = '/home/simon/Documents/Bodies/data/PRIO'#local
    #path_gwno = location + '/PRIO-GRID Yearly Variables for 2003-2009 - 2022-06-16.csv' #https://grid.prio.org/#/download # need to figrue out the API
    path_gwno = location + '/PRIO-GRID Yearly Variables for 1989-2014 - 2022-06-16.csv' #https://grid.prio.org/#/download # need to figrue out the API

    # why not just go 1989 - 2019 like ucdp...

    gwno = pd.read_csv(path_gwno)

    return gwno

def get_prio_shape():

    location = '/home/projects/ku_00017/data/raw/PRIO'
    #location = '/home/simon/Documents/Bodies/data/PRIO'#local
    path_prio = location + '/priogrid_shapefiles.zip'

    if os.path.isfile(path_prio) == True:
        
        print('File already downloaded')
        prio_grid = gpd.read_file('zip://' + path_prio)

        prio_grid =  pd.DataFrame(prio_grid.drop(columns = ['geometry']))

    else:
        print('Beginning file download PRIO...')
        url_prio = 'http://file.prio.no/ReplicationData/PRIO-GRID/priogrid_shapefiles.zip'

        urllib.request.urlretrieve(url_prio, path_prio)
        prio_grid = gpd.read_file('zip://' + path_prio)

        prio_grid =  pd.DataFrame(prio_grid.drop(columns = ['geometry']))

    return prio_grid


def get_gwno():

    location = '/home/projects/ku_00017/data/raw/PRIO'
    #location = '/home/simon/Documents/Bodies/data/PRIO' #local
    #path_gwno = location + '/PRIO-GRID Yearly Variables for 2003-2009 - 2022-06-16.csv' #https://grid.prio.org/#/download # need to figrue out the API
    path_gwno = location + '/PRIO-GRID Yearly Variables for 1989-2014 - 2022-06-16.csv' #https://grid.prio.org/#/download # need to figrue out the API

    # why not just go 1989 - 2019 like ucdp...

    gwno = pd.read_csv(path_gwno)

    return gwno


def get_ucdp():

    location = '/home/projects/ku_00017/data/raw/UCDP'
    #location = '/home/simon/Documents/Bodies/data/UCDP' #local
    path_ucdp = location + "/ged201-csv.zip"
    
    if os.path.isfile(path_ucdp) == True:
        print('file already downloaded')
        ucdp = pd.read_csv(path_ucdp, low_memory=False)


    else: 
        print('Beginning file download UCDP...')

        url_ucdp = 'https://ucdp.uu.se/downloads/ged/ged201-csv.zip'
    
        urllib.request.urlretrieve(url_ucdp, path_ucdp)
        ucdp = pd.read_csv(path_ucdp, low_memory=False)


    # just to save ram for now !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # sub_years = sorted(ucdp['year'].unique())[:2]
    # ucdp = ucdp[ucdp['year'].isin(sub_years)]
    # -----------------------------------------------------------------------------------------------------

    ucdp['month'] = pd.to_datetime(ucdp['date_start']).dt.month
    ucdp.rename(columns= {'priogrid_gid' : 'gid'}, inplace= True)

    feature_list = ['month','year', 'gid', 'deaths_a','deaths_b', 'deaths_civilians', 'deaths_unknown','best', 'high', 'low']

    ucdp_monthly_unit = ucdp.loc[:,feature_list].groupby(['month','year', 'gid']).sum().reset_index()
    ucdp_monthly_unit['log_best'] = np.log(ucdp_monthly_unit['best'] +1)
    ucdp_monthly_unit['log_low'] = np.log(ucdp_monthly_unit['low'] +1)
    ucdp_monthly_unit['log_high'] = np.log(ucdp_monthly_unit['high'] +1)

    ucdp_monthly_unit['in_ucdp'] = True # handy later when I wnat to remove water and stuff.

    return ucdp_monthly_unit


def monthly_grid(prio_grid, ucdp):

    years = [sorted(ucdp['year'].unique())] * prio_grid.shape[0]
    months = [list(np.arange(1, 13))] * prio_grid.shape[0]

    prio_grid['year'] = years
    prio_grid['month'] = months

    prio_grid = prio_grid.explode('year').reset_index(drop=True) 
    prio_grid = prio_grid.explode('month').reset_index(drop=True) 

    prio_grid['year'] = prio_grid['year'].astype(int)
    prio_grid['month'] = prio_grid['month'].astype(int)

    return prio_grid


def make_full_grid(prio_grid, ucdp, gwno):

    prio_grid = prio_grid.merge(gwno, on = ['gid', 'year'], how = 'left') 

    # you can easily add monthly prio features here (if you got the ram for it)

    full_grid = prio_grid.merge(ucdp, on = ['gid', 'year', 'month'], how = 'left') 
    full_grid.fillna({'best' : 0, 'low' : 0, 'high' : 0, 'log_best' : 0, 'log_low' : 0, 'log_high' : 0, 'gwno' : 0}, inplace = True) # for gwno 0 is no country
    full_grid.fillna({'in_ucdp' : False}, inplace = True)

    full_grid['log_best'] = np.log(full_grid['best'] + 1)
    full_grid['log_high'] = np.log(full_grid['high'] + 1)
    full_grid['log_low'] = np.log(full_grid['low'] + 1)

    return full_grid


def add_month_id(prio_grid):

    prio_grid['year_month'] = prio_grid['year'].astype(str) + '_' + prio_grid['month'].astype(str) 

    ts = prio_grid['year_month'].unique()
    n_ts = len(ts)
    month_ids = np.arange(109, n_ts + 109, 1)
    month_id_df = pd.DataFrame({'year_month' : ts, 'month_id': month_ids})
    prio_grid = prio_grid.merge(month_id_df, on = 'year_month', how = 'left')

    return prio_grid

def check_month_id(prio_grid):

    for year in prio_grid['year'].unique():
        print(year, end = ': ')
        print(prio_grid[prio_grid['year'] == year]['month_id'].unique(), end = ': ')
        print(len(prio_grid[prio_grid['year'] == year]['month_id'].unique()))


def make_volumn(df):

    # we start with wat we know - but there is no reason not to try with more down til line.

    sub_df = df[['gid', 'xcoord', 'ycoord', 'month_id', 'best', 'low', 'high', 'log_best', 'log_low', 'log_high']].copy() # remove the everything also the geo col.

    sub_df_sorted = sub_df.sort_values(['month_id', 'ycoord', 'xcoord'], ascending = [True, False, True])

    # try to keep the jazz
    #grid_ucdpS = grid_ucdpS[['gid','best', 'low',  'high', 'log_best', 'log_low', 'log_high']].copy() # remove the everything also the geo col. But keep gid. Why not.

    x_dim = sub_df['xcoord'].unique().shape[0]
    y_dim = sub_df['ycoord'].unique().shape[0]
    z_dim = sub_df['month_id'].unique().shape[0]

    ucpd_vol = np.array(sub_df_sorted).reshape((z_dim, y_dim, x_dim, -1))

    return ucpd_vol



def compile():

    prio_grid = get_prio_shape()
    gwno = get_gwno()
    ucdp = get_ucdp()
    prio_grid = monthly_grid(prio_grid, ucdp)
    prio_grid = make_full_grid(prio_grid, ucdp, gwno)
    prio_grid = add_month_id(prio_grid)
    print(prio_grid.shape)

    check_month_id(prio_grid)

    ucpd_vol = make_volumn(prio_grid)
    print(ucpd_vol.shape)


    location = '/home/projects/ku_00017/data/raw/conflictNet'
    #location = '/home/simon/Documents/Articles/ConflictNet/data/raw'



    print('Saving pickle')
    file_name = "/ucpd_monthly_vol.pkl"
    output = open(location + file_name, 'wb')
    pickle.dump(ucpd_vol, output)
    output.close()

    print('Done')


if __name__ == '__main__':
    compile()