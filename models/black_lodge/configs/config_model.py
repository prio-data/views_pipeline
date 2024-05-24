from xgboost import XGBRFRegressor

def get_model_config():
    """
    Contains the common configuration settings for the model (model architecture, name, target variable, level of analysis and deployment status).

    Returns:
    - model_config (dict): A dictionary containing model configuration settings.
    """
    model_config = {
        "name": "black_lodge",
        "algorithm": XGBRFRegressor, 
        "depvar": "ln_ged_sb_dep", 
        "queryset": "fatalities002_baseline",
        "level": "cm",
        "sweep": False,
        "force_retrain": False,
        "steps": [*range(1, 36 + 1, 1)],
        "deployment_status": "production",
        "creator": "Sara",
        "preprocessing": "float_it", #new
        "data_train": "baseline002", #new
        "n_jobs": 12, #new, move to hyperparameters
        "n_estimators": 300 #new, move to hyperparameters
    }
    return model_config 