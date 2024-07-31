def get_meta_config():
    """
    Contains the common configuration settings for the model (model architecture, name, target variable, level of analysis and deployment status).

    Returns:
    - model_config (dict): A dictionary containing model configuration settings.
    """
    meta_config = {
        "name": "black_lodge",
        "algorithm": "XGBRFRegressor", 
        "depvar": "ln_ged_sb_dep", 
        "queryset": "fatalities002_baseline",
        "level": "cm",
        "creator": "Sara",
        "preprocessing": "float_it", #new
        "data_train": "baseline002", #new    
        }
    return meta_config #formely model_config