#Questions:
    # Do we only want to return future predictions?
import sys
from pathlib import Path
import pandas as pd

from views_runs import DataPartitioner

#import modules from model folder
model_path = Path(__file__).resolve().parents[2] 
sys.path.append(str(model_path))

from configs.config_data_partition import get_data_partitions 
from src.training.train_model import train_model #stepshifter_model_calib, stepshifter_model_future
from src.utils.set_paths import get_data_path


def generate_forecasts(stepshifter_model_calib, stepshifter_model_future):
    """
    Generates forecasts for the future using trained models.

    Returns:
    - calib_predictions (DataFrame): Predictions for the calibration partition.
    - future_predictions (DataFrame): Predictions for the future partition.

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
    data_partitions = get_data_partitions()
    future_partitioner_dict = data_partitions["future_partitioner_dict"]

    # Predictions for test partition
    calib_predictions = stepshifter_model_calib.predict('calib','predict',data, proba=True)

    # Predictions for the future
    future_partition = DataPartitioner({'future':future_partitioner_dict}) #is this needed?
    future_predictions = stepshifter_model_future.future_predict('future','predict',data)

    # Predictions for the future, alternative method (not sure why this is needed, ask Håvard)
    #future_point_predictions = stepshifter_model_future.future_point_predict(time=529, data=data, proba=True)

    return calib_predictions, future_predictions 

if __name__ == "__main__":

    # Call the train_model function to get the models
    stepshifter_model_calib, stepshifter_model_future = train_model()

    # Call the generate_forecasts function
    generate_forecasts(stepshifter_model_calib, stepshifter_model_future)

