import pandas as pd
from views_forecasts.extensions import *
from src.offline_evaluation.evaluate_ensemble import evaluate_model
from configs.config_common import get_common_config

def get_standardized_df(df):
    cols = [df.forecasts.target] + df.forecasts.prediction_columns
    return df[cols]

def median_emsemble(df1, df2):
    return (df1 + df2) / 2

    

if __name__ == "__main__":
    df1 = pd.DataFrame.forecasts.read_store(name="orange_pasta")
    df1 = get_standardized_df(df1)

    df2 = pd.DataFrame.forecasts.read_store(name="yellow_pikachu")
    df2 = get_standardized_df(df2)  
    
    df_median = median_emsemble(df1, df2)
    df_median.forecasts.set_run('cabin_001_530_b')
    df_median.forecasts.to_store(name="white_snow")

    config = get_common_config()
    evaluate_model(config)
    