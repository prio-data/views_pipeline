from .stepshifter import StepshifterModel
from .validation import views_validate
from views_forecasts.extensions import *
from sklearn.utils.validation import check_is_fitted


class HurdleModel(StepshifterModel):
    """
    Hurdle model for time series forecasting. The model consists of two stages:
    1. Binary stage: Predicts whether the target variable is 0 or > 0.
    2. Positive stage: Predicts the value of the target variable when it is > 0.

    ! Note:
    We use a lightly different algorithm here. For the binary stage, a regression model is used, but the target is binary (0 or 1).
    For the positive stage, a regression model is used as well. We select countries/priogrids that have at least one positive value in the target variable.
    Since the target variable can be a float number, we use a threshold (default 0.1) to determine whether the target variable is positive or not.
    """
    def __init__(self, config: Dict, partitioner_dict: Dict[str, List[int]]):
        super().__init__(config, partitioner_dict)
        self.clf = self._resolve_estimator(config['model_clf'])
        self.reg = self._resolve_estimator(config['model_reg'])
        self.clf_params = self._get_parameters(config)['clf']
        self.reg_params = self._get_parameters(config)['reg']

    @views_validate
    def fit(self, df: pd.DataFrame, threshold: float = 0.1):
        self._prepare_time_series(df)

        # Binary outcome (event/no-event)
        # According to the DARTS doc, if timeSeries uses a numeric type different from np.float32 or np.float64, not all functionalities may work properly.
        # So use astype(float) instead of astype(int) (we should have binary outputs 0,1 though)
        target_binary = [s.map(lambda x: (x > threshold).astype(float)) for s in self._target]

        # Positive outcome (for cases where target > 0)
        target_pos, past_cov_pos = zip(*[(t, p) for t, p in zip(self._target, self._past_cov)
                                         if (t.values() > threshold).any()])

        for step in self.steps:
            # Fit binary-like stage using a regression model, but the target is binary (0 or 1)
            binary_model = self.clf(lags_past_covariates=[-step], **self.clf_params)
            binary_model.fit(target_binary, past_covariates=self._past_cov)

            # Fit positive stage using the regression model
            positive_model = self.reg(lags_past_covariates=[-step], **self.reg_params)
            positive_model.fit(target_pos, past_covariates=past_cov_pos)
            self._models[step] = (binary_model, positive_model)
        self.is_fitted_ = True

    @views_validate
    def predict(self, run_type: str, df: pd.DataFrame) -> pd.DataFrame:
        check_is_fitted(self, 'is_fitted_')
        pred_by_step_binary = [self._predict_by_step(self._models[step][0], step, self._target, run_type)
                               for step in self.steps]

        pred_by_step_positive = [self._predict_by_step(self._models[step][1], step, self._target, run_type)
                                 for step in self.steps]

        # Combine predictions: binary stage sets the threshold, positive stage adds values where applicable
        final_pred = pd.concat(pred_by_step_binary, axis=1) * pd.concat(pred_by_step_positive, axis=1)

        # Add the target variable to the predictions to make sure it is a VIEWS prediction
        # But if it is forecasting, we don't need to add the target variable
        if run_type != 'forecasting':
            final_pred = pd.merge(final_pred, df[self.depvar], left_index=True, right_index=True)

        return final_pred
