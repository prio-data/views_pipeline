import logging
from pathlib import Path
from set_path import setup_data_paths
from utils_dataloaders import fetch_or_load_views_df

logger = logging.getLogger(__name__)
PATH = Path(__file__)


def get_data(args):
    PATH_RAW, _, _ = setup_data_paths(PATH)

    data, alerts = fetch_or_load_views_df(args.run_type, PATH_RAW, use_saved=args.saved)
    logger.debug(f"DataFrame shape: {data.shape if data is not None else 'None'}")

    for ialert, alert in enumerate(str(alerts).strip('[').strip(']').split('Input')):
        if 'offender' in alert:
            logger.warning({f"{args.run_type} data alert {ialert}": str(alert)})

    return data
