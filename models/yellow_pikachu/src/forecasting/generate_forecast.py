import pandas as pd
from pathlib import Path

import sys
src_path = f"{Path(__file__).parent.parent}"
sys.path.append(str(src_path)+"/utils")

# Remove this part after packaging views_stepshift
current_file_path = Path(__file__).resolve()
root_path = current_file_path.parent.parent.parent.parent.parent
sys.path.append(str(root_path))

from utils import get_artifacts_path, get_data_path

def forecast():
    print('Predicting...')

    stepshifter_model = pd.read_pickle(get_artifacts_path("future"))
    dataset = pd.read_parquet(get_data_path("raw"))

    # Predictions for the future (NaN values exist as it uses data from the last point in time in the selected partition):
    predictions = stepshifter_model.future_predict("future", "predict", dataset, keep_specific=True)

    return predictions