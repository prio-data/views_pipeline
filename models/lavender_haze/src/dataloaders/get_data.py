import pandas as pd
from pathlib import Path

import sys
model_path = f"{Path(__file__).parent.parent.parent}"
pipeline_path = f"{Path(__file__).parent.parent.parent.parent.parent}"
sys.path.append(str(model_path)+"/configs")
sys.path.append(str(pipeline_path)+"/common_utils")


from configs.config_queryset import get_queryset
from common_utils.set_path import get_data_path

def get_data(common_config):
    print("Getting data...")
    parque_path = get_data_path(common_config["name"], "raw")
    if not parque_path.exists():
        qs_baseline = get_queryset()
        data = qs_baseline.publish().fetch()
        data.to_parquet(parque_path)
    else: 
        data = pd.read_parquet(parque_path)

    return data