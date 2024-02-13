import wandb
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.base import BaseEstimator
from sklearn.utils.estimator_checks import check_estimator
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.ensemble import HistGradientBoostingClassifier
from xgboost import XGBRegressor
from xgboost import XGBClassifier
from xgboost import XGBRFRegressor, XGBRFClassifier
from lightgbm import LGBMClassifier, LGBMRegressor

def _resolve_estimator(func_name: str):
    """ Lookup table for supported estimators.
        This is necessary because sklearn estimator default arguments
        must pass equality test, and instantiated sub-estimators are not equal. """

    funcs = {'linear': LinearRegression(),
             'logistic': LogisticRegression(solver='liblinear'),
             'LGBMRegressor': LGBMRegressor(n_estimators=250),
             'LGBMClassifier': LGBMClassifier(n_estimators=250),
             'RFRegressor': XGBRFRegressor(n_estimators=250, n_jobs=-2),
             'RFClassifier': XGBRFClassifier(n_estimators=250, n_jobs=-2),
             'GBMRegressor': GradientBoostingRegressor(n_estimators=200),
             'GBMClassifier': GradientBoostingClassifier(n_estimators=200),
             'XGBRegressor': XGBRegressor(n_estimators=100, learning_rate=0.05, n_jobs=-2),
             'XGBClassifier': XGBClassifier(n_estimators=100, learning_rate=0.05, n_jobs=-2),
             'HGBRegressor': HistGradientBoostingRegressor(max_iter=200),
             'HGBClassifier': HistGradientBoostingClassifier(max_iter=200),
             }

    return funcs[func_name]


def wandb_log(project_name, entity_name, entity_to_log, name_of_entity):
    wandb.init(project=project_name, entity=entity_name)
    wandb.log({f'{name_of_entity}': entity_to_log})
    wandb.finish()

def wandb_init(project_name, entity_name):
    wandb.init(project=project_name, entity=entity_name)
    
def wandb_finish():
    wandb.finish()