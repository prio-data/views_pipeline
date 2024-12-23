def get_meta_config():
    """
    Contains the meta data for the model (model architecture, name, target variable, and level of analysis).
    This config is for documentation purposes only, and modifying it will not affect the model, the training, or the evaluation.

    Returns:
    - meta_config (dict): A dictionary containing model meta configuration.
    """
    meta_config = {
        "name": "lavender_haze",
        "algorithm": "HurdleRegression",
        "model_clf": "LGBMClassifier",
        "model_reg": "LGBMRegressor",
        "depvar": "ln_ged_sb_dep",  # IMPORTANT! The current stepshift only takes one target variable! Not compatiable with Simon's code!
        "queryset": "fatalities003_pgm_broad",
        "level": "pgm",
        "creator": "Xiaolong"
    }
    return meta_config