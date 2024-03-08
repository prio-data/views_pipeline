def get_common_config():
    common_config = {
        "name": "orange_pasta",
        "algorithm": "LGBMRegressor",
        "depvar": "ged_sb_dep",
        "queryset": "fatalities003_pgm_baseline",
        "data_train": "baseline",
        "level": "pgm",
        'steps': [*range(1, 36 + 1, 1)],
    }
    return common_config