def get_common_config():
    """
    Retrieves the common configuration settings for the blue_wave model.

    Returns:
    - common_config (dict): A dictionary containing common configuration settings.
    """
    common_config = {
        "name": "grapefruit_soda",
        "algorithm": "RandomForestClassifier", 
        "depvar": "ged_sb_dep", 
        "queryset": "escwa001_cflong",
        "data_train": "", #? e.g. baseline, conflict_treelag
        "level": "cm",
        "sweep": False,
        
        'steps': [*range(1, 36 + 1, 1)],
        'calib_partitioner_dict': {"train": (121, 396), "predict": (409, 456)},
        'test_partitioner_dict': {"train": (121, 456), "predict": (457, 504)},
        'future_partitioner_dict': {"train": (121, 504), "predict": (529, 529)},
        'FutureStart': 508, #not sure about this
        'force_retrain': False
    }
    return common_config