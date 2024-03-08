import sys
from pathlib import Path
import pandas as pd

from views_runs import DataPartitioner

model_path = Path(__file__).resolve().parents[2] 
sys.path.append(str(model_path))
print(sys.path)

from configs.config_data_partitions import get_data_partitions 
from configs.config_hyperparameters import get_hp_config
from configs.config_model import get_model_config
from src.training.train_model import train 
from src.utils.set_paths import get_data_path, get_generated_data_path

def forecast(data_partitions, model_calibration_partition, model_future_partition):
    """
    Generates forecasts for the future using trained models.

    Args:
    - model_calibration_partition (ViewsRun): Trained model for the calibration partition.
    - model_future_partition (ViewsRun): Trained model for the future partition.
    - data_partitions (dict): Data partitions for calibration, testing, forecasting.

    Returns:
    - calibration_predictions (DataFrame): Predictions for the calibration partition.
    - future_predictions (DataFrame): Predictions for the future partition.
    - future_point_predictions (DataFrame): Point predictions for the future partition.

    Notes:
    - The function relies on previously trained models, specifically `model_calibration_partition` and `model_future_partition`.
    - The function loads configuration parameters, such as `future_partitioner_dict`, from `common_config`.
    - Predictions for the calibration partition are generated using `model_calibration_partition.predict()` method.
    - Predictions for the future partition are generated using `model_future_partition.future_predict()` method.
    """

    print("Generating forecasts...")

    data = pd.read_parquet(get_data_path("raw"))
    future_partitioner_dict = data_partitions["future_partitioner_dict"]

    calib_predictions = model_calibration_partition.predict('calib','predict',data, proba=True)

    future_partition = DataPartitioner({'future':future_partitioner_dict}) #is this being used? we don't define an equivalent for calib_predictions
    future_predictions = model_future_partition.future_predict('future','predict',data)
    future_point_predictions = model_future_partition.future_point_predict(time=529, data=data, proba=True)

    calib_predictions.to_parquet(get_generated_data_path("calibration"))
    future_predictions.to_parquet(get_generated_data_path("future"))
    future_point_predictions.to_parquet(get_generated_data_path("future_point"))

    print("Forecasts generated and saved in data/generated!")

    return calib_predictions, future_predictions, future_point_predictions

if __name__ == "__main__":

    data_partitions = get_data_partitions()
    hyperparameters = get_hp_config()
    model_config = get_model_config()

    model_calibration_partition, model_future_partition = train(model_config, hyperparameters, data_partitions)

    forecast(data_partitions, model_calibration_partition, model_future_partition)

