def get_common_config():
    common_config = {
        "name": "wildest_dream",
        "algorithm": "HurdleRegression",
        "clf_name":"HistGradientBoostingClassifier",
        "reg_name":"HistGradientBoostingRegressor",
        "depvar": "ged_sb_dep",
        "queryset": "fatalities003_pgm_conflict_sptime_dist",
        "level": "pgm",
        'steps': [*range(1, 36 + 1, 1)],
    }
    return common_config