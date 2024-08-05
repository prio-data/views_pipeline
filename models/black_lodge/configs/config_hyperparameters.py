def get_hp_config(): 
    hp_config = {
        "steps": [*range(1, 36 + 1, 1)],
        "parameters": {
            "n_estimators": 300,
            "n_jobs": 12
        }
    }
    return hp_config