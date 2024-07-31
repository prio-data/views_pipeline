import pickle
import numpy as np
import pandas as pd
from darts import TimeSeries
from darts.models import LightGBMModel, XGBModel
from darts.models.forecasting.forecasting_model import ModelMeta
import warnings
warnings.filterwarnings("ignore")
import time
from typing import List, Dict

from views_forecasts.extensions import *
from .validation import views_validate
from utils import get_parameters


class StepshifterModel:
    def __init__(self, config: Dict, partitioner_dict: Dict[str, List[int]]):
        self._initialize_model(config)

        self.steps = config['steps']
        self.target = config['depvar']

        self._params = get_parameters(config)
        self._steps_extent = max(self.steps)
        self._train_start, self._train_end = partitioner_dict['train']
        self._test_start, self._test_end = partitioner_dict['predict']

        self._models = {}
        self._independent_variables = None
        self._time = None
        self._level = None
        self._series = None


    @views_validate
    def fit(self, df: pd.DataFrame):
        self._setup(df)
        self._prepare_time_series(df)
        self._fit_models()


    @views_validate
    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        pred = self._predict_models()
        pred[self.target] = df.loc[(slice(self._test_start, self._test_end),),:][self.target]
        return pred


    def _initialize_model(self, config: Dict):
        self.clf = globals()[config['algorithm']]
        if not isinstance(self.clf, ModelMeta):
            raise ValueError(f"Model {config['algorithm']} is not a valid Darts forecasting model. Change the model in the config file.")


    def _setup(self, df: pd.DataFrame):
        self._time = df.index.names[0]
        self._level = df.index.names[1]
        self._independent_variables = [c for c in df.columns if c != self.target]


    def _prepare_time_series(self, df: pd.DataFrame):
        df_reset = df.reset_index(level=[1])
        self._series = TimeSeries.from_group_dataframe(df_reset, group_cols=self._level,
                                                       value_cols=self._independent_variables + [self.target])


    def _fit_models(self):
        target = [series.slice(self._train_start, self._train_end + 1)[self.target]
                  for series in self._series]  # ts.slice is different from df.slice
        past_cov = [series.slice(self._train_start, self._train_end + 1)[self._independent_variables]
                    for series in self._series]
        for step in self.steps:
            model = self.clf(lags_past_covariates=[-step], **self._params)
            model.fit(target, past_covariates=past_cov)
            self._models[step] = model


    def _predict_models(self):
        target = [series.slice(self._train_start, self._train_end + 1)[self.target]
                  for series in self._series]

        preds_by_step = [self._predict_for_step(step, target) for step in self.steps]
        return pd.concat(preds_by_step, axis=1)


    def _predict_for_step(self, step, target):
        model = self._models[step]
        horizon = self._test_end - self._test_start + 1
        ts_pred = model.predict(n=horizon,
                                series=target,
                                # darts automatically locates the time period of past_covariates
                                past_covariates=[series[self._independent_variables] for series in self._series],
                                show_warnings=False)
        return self._process_predictions(ts_pred, step)


    def _process_predictions(self, ts_pred, step):
        preds = []
        for pred in ts_pred:
            df_pred = pred.pd_dataframe()
            df_pred.index = pd.MultiIndex.from_product([df_pred.index, [pred.static_covariates.iloc[0, 0]]])
            df_pred.index.names = [self._time, self._level]
            df_pred.columns = [f"step_pred_{step}"]
            df_pred = df_pred.loc[slice(self._test_start, self._test_end, ), :]
            preds.append(df_pred)
        return pd.concat(preds).sort_index()


    def save(self, path: str):
        try:
            with open(path, "wb") as file:
                pickle.dump(self, file)
            print(f"Model successfully saved to {path}")
        except Exception as e:
            print(f"Failed to save model: {e}")


    @property
    def models(self):
        return self._models.values()

'''
if __name__ == "__main__":
    month = [*range(1, 600)]
    pg = [123, 456]
    idx = pd.MultiIndex.from_product([month, pg], names=['month_id', 'priogrid_gid'])
    df = pd.DataFrame(index=idx)
    df['ged_sb_dep'] = df.index.get_level_values(0).astype(float)
    df['ln_ged_sb'] = df.index.get_level_values(0) + df.index.get_level_values(1) / 1000
    df['ln_pop_gpw_sum'] = df.index.get_level_values(0) * 10 + df.index.get_level_values(1) / 1000
    steps = [*range(1, 3 + 1, 1)]
    partitioner_dict = {"train": (121, 131), "predict": (132, 135)}
    target = 'ged_sb_dep'

    # df = pd.read_parquet('raw.parquet')
    # steps = [*range(1, 36 + 1, 1)]
    # partitioner_dict = {"train": (121, 444), "predict": (445, 492)}
    # target = df.forecasts.target
    #
    start_t = time.time()
    
    hp_config = {
        "name": "orange_pasta",
        "algorithm": "LightGBMModel",
        "depvar": "ged_sb_dep",
        "steps": [*range(1, 36 + 1, 1)],
        "parameters": {
            "learning_rate": 0.01,
            "n_estimators": 100,
            "num_leaves": 31,
        }
    }

    stepshifter = StepshifterModel(hp_config, partitioner_dict)
    stepshifter.fit(df)
    stepshifter.save('./model.pkl')

    train_t = time.time()
    minutes = (train_t - start_t) / 60
    print(f'Done training. Runtime: {minutes:.3f} minutes')

    # stepshift = pd.read_pickle('./model.pkl')
    pred = stepshifter.predict()
    pred.to_parquet('pred.parquet')

    end_t = time.time()
    minutes = (end_t - train_t) / 60
    print(f'Done predicting. Runtime: {minutes:.3f} minutes')
'''



