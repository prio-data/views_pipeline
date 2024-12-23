import pickle
import numpy as np
from darts import TimeSeries
from darts.models import LightGBMModel, XGBModel, LinearRegressionModel, RandomForest
from sklearn.utils.validation import check_is_fitted
from typing import List, Dict
from views_forecasts.extensions import *
from .validation import views_validate


class StepshifterModel:
    def __init__(self, config: Dict, partitioner_dict: Dict[str, List[int]]):
        self._steps = config['steps']
        self._depvar = config['depvar']
        self._reg = self._resolve_estimator(config['model_reg'])
        self._params = self._get_parameters(config)
        self._train_start, self._train_end = partitioner_dict['train']
        self._test_start, self._test_end = partitioner_dict['predict']
        self._models = {}

    @views_validate
    def fit(self, df: pd.DataFrame):
        self._prepare_time_series(df)
        for step in self._steps:
            model = self._reg(lags_past_covariates=[-step], **self._params)
            model.fit(self._target_train, past_covariates=self._past_cov_train)
            self._models[step] = model
        self.is_fitted_ = True

    @views_validate
    def predict(self, run_type, df: pd.DataFrame) -> pd.DataFrame:
        check_is_fitted(self, 'is_fitted_')
        pred_by_step = [self._predict_by_step(self._models[step], step, self._target_train, run_type) for step in self._steps]
        pred = pd.concat(pred_by_step, axis=1)

        # Add the target variable to the predictions to make sure it is a VIEWS prediction
        # But if it is forecasting, we don't need to add the target variable
        if run_type != 'forecasting':
            pred = pd.merge(pred, df[self._depvar], left_index=True, right_index=True)

        return pred

    @staticmethod
    def _resolve_estimator(func_name: str):
        """ Lookup table for supported estimators.
        This is necessary because sklearn estimator default arguments
        must pass equality test, and instantiated sub-estimators are not equal. """

        funcs = {
            'LinearRegressionModel': LinearRegressionModel,
            'RandomForestModel': RandomForest,
            'LightGBMModel': LightGBMModel,
            'XGBModel': XGBModel,
        }

        if func_name not in funcs.keys():
            raise ValueError(f"Model {func_name} is not a valid Darts forecasting model or is not supported now. "
                             f"Change the model in the config file.")
        return funcs[func_name]

    @staticmethod
    def _get_parameters(config: Dict):
        '''
        Get the parameters from the config file.
        If not sweep, then get directly from the config file, otherwise have to remove some parameters.
        '''

        if config["sweep"]:
            keys_to_remove = ["algorithm", "depvar", "steps", "sweep", "run_type", "model_cls", "model_reg"]
            parameters = {k: v for k, v in config.items() if k not in keys_to_remove}
        else:
            parameters = config["parameters"]

        return parameters

    def _prepare_time_series(self, df: pd.DataFrame):
        # set up
        self._time = df.index.names[0]
        self._level = df.index.names[1]
        self._independent_variables = [c for c in df.columns if c != self._depvar]

        # prepare time series
        df_reset = df.reset_index(level=[1])
        self._series = TimeSeries.from_group_dataframe(df_reset, group_cols=self._level,
                                                       value_cols=self._independent_variables + [self._depvar])

        self._target_train = [series.slice(self._train_start, self._train_end + 1)[self._depvar]
                              for series in self._series]  # ts.slice is different from df.slice
        self._past_cov_train = [series.slice(self._train_start, self._train_end + 1)[self._independent_variables]
                                for series in self._series]
        self._past_cov = [series[self._independent_variables] for series in self._series]

    def _predict_by_step(self, model, step, target, run_type):
        if run_type == 'forecasting':
            horizon = step
        else:
            horizon = self._test_end - self._test_start + 1

        ts_pred = model.predict(n=horizon,
                                series=target,
                                # darts automatically locates the time period of past_covariates
                                past_covariates=self._past_cov,
                                show_warnings=False)

        # process the predictions
        index_tuples, df_list = [], []
        test_period = slice(self._test_start, self._test_end)
        for pred in ts_pred:
            df_pred = pred.pd_dataframe().loc[test_period]
            level = pred.static_covariates.iat[0, 0]
            index_tuples.extend([(month, level) for month in df_pred.index])
            df_list.append(df_pred.values)

        df_preds = pd.DataFrame(
            data=np.concatenate(df_list),
            index=pd.MultiIndex.from_tuples(index_tuples, names=[self._time, self._level]),
            columns=[f"step_pred_{step}"]
        )

        return df_preds.sort_index()

    def save(self, path: str):
        try:
            with open(path, "wb") as file:
                pickle.dump(self, file)
            print(f"Model successfully saved to {path}")
        except Exception as e:
            print(f"Failed to save model: {e}")

    @property
    def models(self):
        return list(self._models.values())

    @property
    def steps(self):
        return self._steps

    @property
    def depvar(self):
        return self._depvar
