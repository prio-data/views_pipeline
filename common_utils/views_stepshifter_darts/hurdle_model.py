from .stepshifter import StepshifterModel
from .validation import views_validate
from views_forecasts.extensions import *


class HurdleModel(StepshifterModel):
    def __init__(self, config: Dict, partitioner_dict: Dict[str, List[int]]):
        super().__init__(config, partitioner_dict)
        self.clf = self._resolve_estimator(config['model_clf'])
        self.reg = self._resolve_estimator(config['model_reg'])
        self.clf_params = self._get_parameters(config)['clf']
        self.reg_params = self._get_parameters(config)['reg']

    @views_validate
    def fit(self, df: pd.DataFrame):
        self._prepare_time_series(df)

        # Binary outcome (event/no-event)
        binary_target = [series > 0 for series in self._target]

        # Positive outcome (for cases where target > 0)
        positive_target = [series[series > 0] for series in self._target]

        for step in self.steps:
            # Fit binary-like stage using a regression model, but the target is binary (0 or 1)
            binary_model = self.clf(lags_past_covariates=[-step], **self.clf_params)
            binary_model.fit(binary_target, past_covariates=self._past_cov)

            # Fit positive stage using the regression model
            positive_model = self.reg(lags_past_covariates=[-step], **self.reg_params)
            positive_model.fit(positive_target, past_covariates=self._past_cov)
            self._models[step] = (binary_model, positive_model)
        self._is_fitted = True

    @views_validate
    def predict(self, run_type: str, df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
        pred_by_step_binary = [self._predict_by_step(self._models['step'][0], step, self._target, run_type)
                               for step in self.steps]

        pred_by_step_positive = [self._predict_by_step(self._models['step'][1], step, self._target, run_type)
                                 for step in self.steps]

        # Apply a threshold to binary predictions (default is 0.5)
        binary_pred = [pred.clip(0, 1).apply(lambda x: 1 if x >= threshold else 0)
                       for pred in pred_by_step_binary]

        # Combine predictions: binary stage sets the threshold, positive stage adds values where applicable
        final_pred = pd.concat(binary_pred, axis=1) * pd.concat(pred_by_step_positive, axis=1)

        # Add the target variable to the predictions to make sure it is a VIEWS prediction
        # But if it is forecasting, we don't need to add the target variable
        if run_type != 'forecasting':
            final_pred = pd.merge(final_pred, df[self.depvar], left_index=True, right_index=True)

        return final_pred
