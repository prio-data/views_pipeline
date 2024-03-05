def get_common_config():
    common_config = {
        "name": "blank_space",
        "algorithm": "HurdleRegression",
        "clf_name":"XGBClassifier",
        "reg_name":"XGBRegressor",
        "depvar": "ged_sb_dep",
        "queryset": "fatalities003_pgm_natsoc",
        "level": "pgm",
        'steps': [*range(1, 36 + 1, 1)],
    }
    return common_config