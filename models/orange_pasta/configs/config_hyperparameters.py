def get_hp_config(): 
    hp_config = {
        "name": "orange_pasta",
        "algorithm": "LGBMRegressor",
        "depvar": "ged_sb_dep",
        "steps": [*range(1, 36 + 1, 1)],
        "parameters": {
            "learning_rate": 0.01,
            "n_estimators": 100,
            "num_leaves": 31,
        }
    }
    return hp_config