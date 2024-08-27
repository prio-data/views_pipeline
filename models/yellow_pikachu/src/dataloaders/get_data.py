import sys
from pathlib import Path
import pandas as pd

PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)

from config_input_data import get_input_data
from utils import ensure_float64


def get_data(args):
    print("Getting data...")
    PATH_RAW, _, _ = setup_data_paths(PATH)
    parquet_path = PATH_RAW / f'raw_{args.run_type}.parquet'
    # print('PARQUET PATH', parquet_path)
    if not parquet_path.exists():
        qs = get_input_data()
        data = qs.publish().fetch()
        data = ensure_float64(data)
        data.to_parquet(parquet_path)
    else:
        data = pd.read_parquet(parquet_path)

    return data