def get_model_config():
    model_config = {
        "name": "orange_pasta",
        "algorithm": "LGBMRegressor",
        "depvar": "ged_sb_dep",
        "queryset": "fatalities003_pgm_baseline",
        "level": "pgm",
        'steps': [*range(1, 36 + 1, 1)],
    }
    return model_config