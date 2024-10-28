import sys
import logging
import wandb

from pathlib import Path
PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)

from utils_dataloaders import fetch_or_load_views_df, create_or_load_views_vol, get_alert_help_string

logger = logging.getLogger(__name__)


def get_data(args, project, self_test):
    logger.info("Getting data...")
    PATH_RAW, _, _ = setup_data_paths(PATH)

    with wandb.init(project=f'{project}', entity="views_pipeline"):

        data, alerts = fetch_or_load_views_df(args.run_type, PATH_RAW, self_test, args.saved)
        logger.info(f"DataFrame shape: {data.shape if data is not None else 'None'}")

    return data
