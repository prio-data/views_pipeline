def get_common_config():
    common_config = {
        "name": "yellow_pikachu",
        "algorithm": "XGBRegressor",
        "depvar": "ged_sb_dep",
        "queryset": "fatalities003_pgm_conflict_treelag",
        "data_train": "conflict_treelag",
        "level": "pgm",
        'steps': [*range(1, 36 + 1, 1)],
    }
    return common_config