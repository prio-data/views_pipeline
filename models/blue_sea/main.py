# from src.dataloaders.fetch_data_run_query import fetch_data
# from src.forecasting.true_future_36m import forecast
# from src.evaluation.evaluation_mse import evaluate_mse
# from configs import config

from src.dataloaders import fetch_data_run_query
from src.forecasting import true_future_36m
from src.evaluation import evaluation_mse
from configs import config


def main():
    data_for_training = fetch_data_run_query.fetch_data()
    start_month, end_month = config.common_config['future_partitioner_dict']['predict']
    forecasts = true_future_36m.forecast(data_for_training.loc[start_month:end_month])    
    print(forecasts)
    evaluation_mse.evaluate_mse()
    print(config.common_config)
    
if __name__ == "__main__":
    main()

