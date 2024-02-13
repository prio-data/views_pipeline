from .src.training import training
from .src.forecasting import true_future_36m as forecast
from .src.visualization.visual import visualize_forecasts_in_maps

def main():
    # training.training()
    forecast.forecast()
    visualize_forecasts_in_maps(12)
    
if __name__ == "__main__":
    main()