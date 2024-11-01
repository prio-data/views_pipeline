def get_hp_config(): 
    hp_config = {
        "steps": [*range(1, 36 + 1, 1)],
        "parameters": {
            "clf":{
                "n_estimators": 200,
                "n_jobs": 12
            },
            "reg":{
                "n_estimators":200,
                "n_jobs": 12
            }
        }
    }
    return hp_config