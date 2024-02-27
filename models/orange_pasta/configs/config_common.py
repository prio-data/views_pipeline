def get_common_config():
    common_config = {
        "name": "orange_pasta",
        "algorithm": "LGBMRegressor",
        "depvar": "ged_sb_dep",
        "queryset": "fatalities003_pgm_baseline",
        "data_train": "baseline",
        "level": "pgm",
        
        'steps': [*range(1, 36 + 1, 1)],
        'train_partitioner_dict': {"train": (121, 396), "predict": (397, 444)},
        'test_partitioner_dict': {"train": (121, 444), "predict": (445, 492)},
        'future_partitioner_dict': {"train": (121, 492), "predict": (493, 504)},
        'FutureStart': 508,
        'force_retrain': False
    }
    return common_config