import sys

import logging
logging.basicConfig(filename='../../run.log', encoding='utf-8', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from pathlib import Path
PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)

from utils_dataloaders import fetch_or_load_views_df, create_or_load_views_vol, get_alert_help_string


def get_data(args):
    logger.info("Getting data...")
    PATH_RAW, _, _ = setup_data_paths(PATH)

    data, alerts = fetch_or_load_views_df(args.run_type, PATH_RAW, args.saved)
    logger.info(f"DataFrame shape: {data.shape if data is not None else 'None'}")

    for ialert, alert in enumerate(str(alerts).strip('[').strip(']').split('Input')):
        if 'offender' in alert:
            logger.warning({f"{args.run_type} data alert {ialert}": str(alert)})

    return data
