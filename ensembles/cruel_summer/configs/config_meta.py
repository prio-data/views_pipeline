def get_meta_config():
    """
    Contains the metadata for the model (model architecture, name, target variable, and level of analysis).
    This config is for documentation purposes only, and modifying it will not affect the model, the training, or the evaluation.

    Returns:
    - meta_config (dict): A dictionary containing model meta configuration.
    """
    meta_config = {
        "name": "cruel_summer",
        "models": ["chunky_cat", "bad_blood"],
        "depvar": "ln_ged_sb_dep", 
        "level": "pgm", 
        "aggregation": "median", 
        "creator": "Xiaolong" 
    }
    return meta_config
