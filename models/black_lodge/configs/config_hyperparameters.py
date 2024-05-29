def get_hp_config(): 
    hp_config = {
        "clf":{
            "n_estimators": 300,
            "n_jobs": 12
        },
        "reg":{
            "n_estimators": 300,
            "n_jobs": 12
        }
    }
    return hp_config