def get_meta_config():
    """
    Contains the metadata for the model (model architecture, name, target variable, and level of analysis).
    This config is for documentation purposes only, and modifying it will not affect the model, the training, or the evaluation.

    Returns:
    - meta_config (dict): A dictionary containing model meta configuration.
    """
    meta_config = {
        "name": "white_mustang",
        "models": ["lavender_haze", "blank_space"],
        "depvar": "ln_ged_sb_dep",  # Double-check the target variables of each model
        "level": "pgm",
        "creator": "Xiaolong"
    }
    return meta_config