def get_hp_config(): 
    hp_config = {
        "steps": [*range(1, 36 + 1, 1)],
        "parameters": {
            "clf": {
                "n_estimators": 200,
            },
            "reg": {
                "n_estimators": 200,
            }
        }
    }
    return hp_config