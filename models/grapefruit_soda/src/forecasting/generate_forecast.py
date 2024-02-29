from views_runs import DataPartitioner

from configs.config_common import common_config #contains data partition dictionaries
from src.training.train_model import stepshifter_model_calib, stepshifter_model_future
from src.dataloaders import data


def generate_forecasts():
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

    #Define configs
    future_partitioner_dict = common_config["future_partitioner_dict"]

    # Predictions for test partition
    calib_predictions = stepshifter_model_calib.predict('calib','predict',data, proba=True)

    # Predictions for the future
    future_partition = DataPartitioner({'future':future_partitioner_dict}) #is this needed?
    future_predictions = stepshifter_model_future.future_predict('future','predict',data)

    # Predictions for the future, alternative method (not sure why this is needed, ask Håvard)
    #future_point_predictions = stepshifter_model_future.future_point_predict(time=529, data=data, proba=True)

    return calib_predictions, future_predictions 

if __name__ == "__main__":

    # Call the generate_forecasts function
    generate_forecasts()

