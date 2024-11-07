import logging
from model_path import ModelPath
from utils_dataloaders import fetch_or_load_views_df

logger = logging.getLogger(__name__)

def get_data(model_name, run_type, use_saved, self_test):
    model_path = ModelPath(model_name, validate=False)
    path_raw = model_path.data_raw

    data, alerts = fetch_or_load_views_df(model_name, run_type, path_raw, self_test, use_saved)
    logger.debug(f"DataFrame shape: {data.shape if data is not None else 'None'}")

    return data
