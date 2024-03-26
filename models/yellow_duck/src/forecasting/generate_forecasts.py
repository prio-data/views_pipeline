import pandas as pd
from pathlib import Path


def forecast(data_for_forecasting) -> pd.DataFrame:
    '''
    This function is used to forecast.
    
    Args:
    data_for_forecasting: The data to be used for forecasting.
    
    Returns:
    data_for_forecasting: The data with the forecasts for the next 36 months.
    '''
    for i in range(1, 37):
        data_for_forecasting[f"step_pred_{i}"] = data_for_forecasting.groupby('priogrid_gid')['ln_ged_sb_dep'].shift(i).fillna(0)   
    print(data_for_forecasting)
    data_for_forecasting.to_parquet(
        f"{Path(__file__).parent.parent.parent}/data/generated/forecasts.parquet")
    
    return data_for_forecasting
