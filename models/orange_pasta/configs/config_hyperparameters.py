def get_hp_config(): 
    hp_config = {
        "steps": [*range(1, 36 + 1, 1)],
        "parameters": {
            "learning_rate": 0.01,
            "n_estimators": 100,
            "num_leaves": 31,
        }
    }
    return hp_config