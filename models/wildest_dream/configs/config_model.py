def get_model_config():
    model_config = {
        "name": "wildest_dream",
        "algorithm": "HurdleRegression",
        "clf_name":"HistGradientBoostingClassifier",
        "reg_name":"HistGradientBoostingRegressor",
        "depvar": "ln_ged_sb_dep",
        "queryset": "fatalities003_pgm_conflict_sptime_dist",
        "level": "pgm",
        'steps': [*range(1, 36 + 1, 1)],
    }
    return model_config