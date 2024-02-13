from .src.training import training
from .src.forecasting import true_future_36m as forecast
from .src.visualization.visual import visualize_forecasts_in_maps
from .src.evaluation.evaluation_mse import evaluate_mse

def main():
    # training.training()
    forecast.forecast()
    visualize_forecasts_in_maps(12)
    evaluate_mse()
    
if __name__ == "__main__":
    main()