import pandas as pd
from mlforecast import MLForecast
from sklearn.metrics import mean_squared_error
from lightgbm import LGBMRegressor
import warnings
warnings.filterwarnings("ignore")
from views_forecasts.extensions import *


class StepShift:
    """
    Attributes:
        common_config (dict): Dictionary specifying the common configuration.
        -- partition (dict): Dictionary specifying the train and test partitions.
        -- steps (int): Number of steps to predict.
        -- target_col (str): Name of the target column.
        -- level (str): Data granularity level, 'cm' or 'pgm'.
        -- algorithm (str): Name of the algorithm to use.
        model_config (dict): Dictionary specifying the model configuration.
    """

    def __init__(self, df_raw, common_config, model_config):
        self.df_raw = df_raw
        self.predictions = {}
        self.partition = common_config["partition"]
        self.steps = common_config["steps"]
        self.target_col = common_config["depvar"]
        self.model_name = common_config["algorithm"]
        self.model = globals()[common_config["algorithm"]](**model_config)
        self.level = common_config["level"]
        if self.level == "cm":
            self.id_col = "country_id"
        elif self.level == "pgm":
            self.id_col = "priogrid_gid"
        else:
            raise ValueError(f"Invalid level: {self.level}. Please use 'cm' or 'pgm'.")
        self.__check_required_columns()

    
    def __check_required_columns(self):
        """Check if required columns exist in the DataFrame as columns not indexes. If not, index is reset."""
        required_columns = [self.id_col, 'month_id']

        if not all(item in self.df_raw.columns for item in required_columns) :
            self.df_raw = self.df_raw.reset_index()


    def __get_pivot_df(self, df, base_month):

        df['step'] = df['month_id'] - base_month

        pivot_df = df.pivot_table(index=['month_id', self.id_col], columns='step', values=self.model_name)

        pivot_df.columns = [f'step_pred_{int(col)}' for col in pivot_df.columns]

        return pivot_df
    

    def fit_predict(self, combine_actuals=True):
        for month in range(self.partition['test'][0] - self.steps + 1, self.partition['test'][1] + 1):
            fcst = MLForecast(models=self.model, freq=1)

            df_train = self.df_raw[self.df_raw['month_id'].isin(range(self.partition['train'][0], month))]
            fcst.fit(df_train, target_col=self.target_col, time_col='month_id', id_col=self.id_col, static_features=[])
            
            df_test = self.df_raw[self.df_raw['month_id'].isin(range(month, self.partition['test'][1] + 1))]
            
            prediction = fcst.predict(min(self.steps, self.partition['test'][1]-month+1), X_df=df_test)
            prediction = prediction.loc[prediction['month_id'].isin(range(self.partition['test'][0], self.partition['test'][1] + 1))]
            self.predictions[month - 1] = prediction

        df_prediction = pd.DataFrame()
        for base_month, df in self.predictions.items():
            pivot_df = self.__get_pivot_df(df, base_month)

            if df_prediction.empty:
                df_prediction = pivot_df
            else:
                df_prediction = df_prediction.combine_first(pivot_df)
        
        if combine_actuals:
            df_test = self.df_raw[self.df_raw['month_id'].isin(range(self.partition['test'][0], self.partition['test'][1] + 1))]
            df_test = df_test[['month_id', self.id_col, self.target_col]]
            df_test = df_test.set_index(['month_id', self.id_col])

            df_prediction = pd.merge(df_prediction, df_test, left_index=True, right_index=True)

        return df_prediction


    def evaluate(self, df):
        if not self.target_col in df.columns:
            raise ValueError(f"Target column {self.target_col} not found in the DataFrame.")
        
        pred_cols = [f'step_pred_{str(i)}' for i in range(1, self.steps+1)]
        df['mse'] = df.apply(lambda row: mean_squared_error([row['ged_sb_dep']] * 36,
                                                            [row[col] for col in pred_cols]), axis=1)
        return df['mse'].mean()


    
