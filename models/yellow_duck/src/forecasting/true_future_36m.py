import pandas as pd
from pathlib import Path


def forecast(data_for_forecasting) -> pd.DataFrame:
    # groupby priogrid_gid first
    # data_for_forecasting.reset_index(inplace=True)
    # for i in range(1, 37):
    #     data_for_forecasting[f"step_pred_{i}"] = None
    # for k in range(min(data_for_forecasting['priogrid_gid']), max(data_for_forecasting['priogrid_gid'])+1):
    #     data_for_forecasting_k = data_for_forecasting[data_for_forecasting['priogrid_gid'] == k]
    #     for i in range(1, 37):
    #         data_for_forecasting_k[f"step_pred_{i}"] = data_for_forecasting_k['ln_ged_sb_dep'].shift(i).fillna(0)
    #     data_for_forecasting[data_for_forecasting['priogrid_gid'] == k] = data_for_forecasting_k
    for i in range(1, 37):
        data_for_forecasting[f"step_pred_{i}"] = data_for_forecasting.groupby('priogrid_gid')['ln_ged_sb_dep'].shift(i).fillna(0)   
    print(data_for_forecasting)
    #data_for_forecasting.set_index(['month_id', 'priogrid_gid'], inplace=True)    
    data_for_forecasting.to_parquet(
        f"{Path(__file__).parent.parent.parent}/data/generated/forecasts.parquet")
    
    return data_for_forecasting
