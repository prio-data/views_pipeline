import sys
from pathlib import Path
import pandas as pd

PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)

from utils_dataloaders import fetch_or_load_views_df, create_or_load_views_vol, get_alert_help_string


def get_data(args):
    print("Getting data...")
    PATH_RAW, _, _ = setup_data_paths(PATH)

    data, alerts = fetch_or_load_views_df(args.run_type, PATH_RAW, args.saved)
    print(f"DataFrame shape: {data.shape if data is not None else 'None'}")

    for ialert, alert in enumerate(str(alerts).strip('[').strip(']').split('Input')):
        if 'offender' in alert:
            print({f"{args.run_type} data alert {ialert}": str(alert)})

    return data