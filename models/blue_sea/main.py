from ..blue_sea.src.dataloaders.fetch_data_run_query import fetch_data
from ..blue_sea.src.forecasting.true_future_36m import forecast
from ..blue_sea.src.evaluation.evaluation_mse import evaluate_mse
from ..blue_sea.configs import config

def main():
    data_for_training = fetch_data()
    start_month, end_month = config.common_config['future_partitioner_dict']['predict']
    forecasts = forecast(data_for_training.loc[start_month:end_month])    
    print(forecasts)
    evaluate_mse()
    print(config.common_config)
    
if __name__ == "__main__":
    data_for_training = fetch_data()
    start_month, end_month = config.common_config['future_partitioner_dict']['predict']
    forecasts = forecast(data_for_training.loc[start_month:end_month])    
    print(forecasts)
    evaluate_mse()
    print(config.common_config)

