#Questions:
    # Do we only want to return future predictions?
import sys
from pathlib import Path
import pandas as pd

from views_runs import DataPartitioner

#import modules from model folder
model_path = Path(__file__).resolve().parents[2] 
sys.path.append(str(model_path))
print(sys.path)

from configs.config_data_partitions import get_data_partitions 
from src.training.train_model import train #stepshifter_model_calib, stepshifter_model_future
from src.utils.set_paths import get_data_path

from configs.config_hyperparameters import get_hp_config
from configs.config_model import get_model_config


def forecast(data_partitions, stepshifter_model_calib, stepshifter_model_future):
    """
    Generates forecasts for the future using trained models.

    Args:
    - stepshifter_model_calib (ViewsRun): Trained model for the calibration partition.
    - stepshifter_model_future (ViewsRun): Trained model for the future partition.
    - data_partitions (dict): Data partitions for calibration, testing, forecasting.

    Returns:
    - calib_predictions (DataFrame): Predictions for the calibration partition.
    - future_predictions (DataFrame): Predictions for the future partition.
    - future_point_predictions (DataFrame): Point predictions for the future partition.

    Notes:
    - The function relies on previously trained models, specifically `stepshifter_model_calib` and `stepshifter_model_future`.
    - The function loads configuration parameters, such as `future_partitioner_dict`, from `common_config`.
    - Predictions for the calibration partition are generated using `stepshifter_model_calib.predict()` method.
    - Predictions for the future partition are generated using `stepshifter_model_future.future_predict()` method.
    """

    print("Generating forecasts...")

    #Load data
    data = pd.read_parquet(get_data_path("raw"))

    #Define configs
    future_partitioner_dict = data_partitions["future_partitioner_dict"]

    # Predictions for test partition (S comment: do we mean calib or test?)
    calib_predictions = stepshifter_model_calib.predict('calib','predict',data, proba=True)

    # Predictions for the future
    future_partition = DataPartitioner({'future':future_partitioner_dict}) #is this being used? we don't define an equivalent for calib_predictions
    future_predictions = stepshifter_model_future.future_predict('future','predict',data)
    # Predictions for the future, point predictions
    future_point_predictions = stepshifter_model_future.future_point_predict(time=529, data=data, proba=True)

    calib_predictions.to_parquet(f"{Path(__file__).parent.parent.parent}/data/generated/calib_predictions.parquet") 
    future_predictions.to_parquet(f"{Path(__file__).parent.parent.parent}/data/generated/future_predictions.parquet")
    future_point_predictions.to_parquet(f"{Path(__file__).parent.parent.parent}/data/generated/future_point_predictions.parquet")

    return calib_predictions, future_predictions, future_point_predictions

if __name__ == "__main__":

    # Load configuration data
    data_partitions = get_data_partitions()
    hyperparameters = get_hp_config()
    model_config = get_model_config()

    # Call the train function with configuration data
    stepshifter_model_calib, stepshifter_model_future = train(model_config, hyperparameters, data_partitions)

    # Call the generate_forecasts function
    forecast(data_partitions, stepshifter_model_calib, stepshifter_model_future)

