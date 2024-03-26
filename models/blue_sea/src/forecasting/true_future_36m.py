import pandas as pd
from pathlib import Path
import numpy as np
from ..dataloaders.queryset import get_querysets

def forecast(data_for_forecasting) -> pd.DataFrame:
    '''
    This function generates the forecasts for the next 36 months based on partitioner dictionary.
    
    Args:
    data_for_forecasting: The data to be used for forecasting.
    
    Returns:
    data_for_forecasting: The data with the forecasts for the next 36 months.

    '''
    for i in range(1, 37):
        data_for_forecasting[f"step_pred_{i}"] = np.mean(data_for_forecasting['ln_ged_sb_dep'])
    print(data_for_forecasting)
    data_for_forecasting.to_parquet(
        f"{Path(__file__).parent.parent.parent}/data/generated/forecasts.parquet")
    print(get_querysets())
    
    return data_for_forecasting
