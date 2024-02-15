import pandas as pd
from pathlib import Path
from ..dataloaders.queryset import get_querysets

def forecast(data_for_forecasting) -> pd.DataFrame:
    for i in range(1, 37):
        data_for_forecasting[f"step_pred_{i}"] = 0
    print(data_for_forecasting)
    data_for_forecasting.to_parquet(
        f"{Path(__file__).parent.parent.parent}/data/generated/forecasts.parquet")
    print(get_querysets())
    
    return data_for_forecasting
