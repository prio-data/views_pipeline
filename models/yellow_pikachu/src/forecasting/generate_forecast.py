from pathlib import Path
from views_forecasts.extensions import *
from ..training.train_model import *



def forecast(config):
    print('Predicting...')

    stepshifter_model = pd.read_pickle(Path(__file__).parent.parent.parent / "artifacts/model_forecasting.pkl")


    dataset = pd.read_parquet(f"{Path(__file__).parent.parent.parent}/data/raw/raw.parquet")


    # Predictions for the future (NaN values exist as it uses data from the last point in time in the selected partition):
    predictions = stepshifter_model.future_predict("future", "predict", dataset, keep_specific=True)

    return predictions