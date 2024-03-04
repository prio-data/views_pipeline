import pandas as pd
from pathlib import Path

import sys
src_path = f"{Path(__file__).parent.parent}"
model_path = f"{Path(__file__).parent.parent.parent}"
sys.path.append(str(model_path)+"/configs")
sys.path.append(str(src_path)+"/utils")

from configs.config_queryset import get_queryset
from utils import get_data_path

def get_data():
    print("Getting data...")
    parque_path = get_data_path("raw")
    if not parque_path.exists():
        qs_baseline = get_queryset()
        data = qs_baseline.publish().fetch()
        data.to_parquet(parque_path)
    else: 
        data = pd.read_parquet(parque_path)

    return data