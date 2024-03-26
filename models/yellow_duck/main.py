from src.dataloaders.fetch_data_run_query import fetch_data
from src.forecasting.generate_forecasts import forecast
from src.evaluation.evaluation_mse import evaluate_mse
from configs import config

def main():
    '''
    This is the main function that will be called to run the entire pipeline
    
    1. Fetch data
    2. Forecast
    3. Evaluate MSE
    '''
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
    
