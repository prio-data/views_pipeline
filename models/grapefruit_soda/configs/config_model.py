def get_model_config():
    """
    Retrieves the common configuration settings for the model.

    Returns:
    - common_config (dict): A dictionary containing model configuration settings.
    """
    model_config = {
        "name": "grapefruit_soda",
        "algorithm": "RandomForestClassifier", 
        "target": "ged_sb_dep", #or depvar? 
        "queryset": "escwa001_cflong",
        "data_train": "baseline", #? e.g. baseline, conflict_treelag
        "level": "cm",
        "sweep": False,
        "force_retrain": False
    }
    return model_config #formerly common_config