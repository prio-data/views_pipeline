def get_model_config():
    model_config = {
        "name": "lavender_haze",
        "algorithm": "HurdleRegression",
        "clf_name":"LGBMClassifier",
        "reg_name":"LGBMRegressor",
        "depvar": "ln_ged_sb_dep",
        "queryset": "fatalities003_pgm_broad",
        "level": "pgm",
        'steps': [*range(1, 36 + 1, 1)],
    }
    return model_config