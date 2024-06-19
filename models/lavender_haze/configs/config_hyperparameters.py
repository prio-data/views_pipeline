def get_hp_config(): 
    hp_config = {
        "name": "lavender_haze",
        "algorithm": "HurdleRegression",
        "model_clf": "LGBMClassifier",
        "model_reg": "LGBMRegressor",
        "depvar": "ln_ged_sb_dep",
        "steps": [*range(1, 36 + 1, 1)],
        "parameters": {
            "clf":{
                "learning_rate": 0.05,
                "n_estimators": 100,
                "n_jobs": 12
            },
            "reg":{
                "learning_rate": 0.05,
                "n_estimators": 100,
                "n_jobs": 12
            }
        }
    }
    return hp_config