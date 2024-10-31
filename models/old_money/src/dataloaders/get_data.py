import logging
from model_path import ModelPath
from utils_dataloaders import fetch_or_load_views_df

logger = logging.getLogger(__name__)


def get_data(args, model_name):
    model_path = ModelPath(model_name)
    path_raw = model_path.data_raw

    data, alerts = fetch_or_load_views_df(model_name, args.run_type, path_raw, use_saved=args.saved)
    logger.debug(f"DataFrame shape: {data.shape if data is not None else 'None'}")

    for ialert, alert in enumerate(str(alerts).strip('[').strip(']').split('Input')):
        if 'offender' in alert:
            logger.warning({f"{args.run_type} data alert {ialert}": str(alert)})

    return data
