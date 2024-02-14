import os
import glob
import pandas as pd
from views_forecasts.extensions import *
import inspect

def ensemble_mean():
    
    forecasts = {}
    path_to_test = os.path.dirname(os.getcwd())
    print(path_to_test)
    for file in glob.glob(path_to_test + "/views_pipeline/models/**/data/generated/forecasts.parquet", recursive=True):
        print(file)
        # get the model name from the file path
        model_name = file.split('/')[-4]
        forecasts[model_name] = pd.read_parquet(file)
        

    ensemble = pd.concat(forecasts.values()).groupby(level=[0,1]).mean()
    ensemble = ensemble.filter(regex='^step_pred_|^ln_ged_sb_dep$')
   
    # get the directory of this function
    function_file = inspect.getfile(ensemble_mean)
    function_dir = os.path.dirname(function_file)
    parent_dir = os.path.dirname(function_dir)
    ensemble_model_name = parent_dir.split('/')[-2]
    ensemble.forecasts.to_store(ensemble_model_name, overwrite=True)
    print(ensemble)