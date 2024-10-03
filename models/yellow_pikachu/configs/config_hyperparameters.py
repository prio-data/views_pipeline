def get_hp_config(): 
    hp_config = {
        "steps": [*range(1, 36 + 1, 1)],
        "parameters": {
            "tree_method": "hist",
            "n_estimators": 200,
            "n_jobs": 12,
        }
    }
    return hp_config