def get_meta_config():
    """
    Contains the meta data for the model (model architecture, name, target variable, and level of analysis).
    This config is for documentation purposes only, and modifying it will not affect the model, the training, or the evaluation.

    Returns:
    - meta_config (dict): A dictionary containing model meta configuration.
    """
    meta_config = {
        "name": "hazel_rabbit",
        "algorithm": "zero baseline", 
        "target(S)": ["ln_sb_best", "ln_ns_best", "ln_os_best", "ln_sb_best_binarized", "ln_ns_best_binarized", "ln_os_best_binarized"], 
        "queryset": "hazel_rabbit",
        "level": "pgm",
        "creator": "Borbala" 
    }
    return meta_config 