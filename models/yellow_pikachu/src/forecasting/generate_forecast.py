import os
import warnings

warnings.filterwarnings("ignore")
os.environ['WANDB_SILENT'] = 'true'

from views_forecasts.extensions import *


def forecast(config):
    print('Predicting...')
    
    try:
        predictions_calib = pd.DataFrame.forecasts.read_store(name=config["storage_name"])
    except:
        predictions_calib = config["RunResult"].run.predict("future", "predict", config["RunResult"].data)
        # predictions_calib.forecasts.set_run(run_id)
        predictions_calib.forecasts.to_store(name=config["storage_name"])

    