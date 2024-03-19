def get_model_config():
    model_config = {
        "name": "yellow_pikachu",
        "algorithm": "XGBRegressor",
        "depvar": "ged_sb_dep",
        "queryset": "fatalities003_pgm_conflict_treelag",
        "level": "pgm",
        'steps': [*range(1, 36 + 1, 1)],
    }
    return model_config