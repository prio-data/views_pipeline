def get_hp_config(): 
    hp_config = {
        "clf":{
            "learning_rate": 0.05,
            "max_iter": 200,
        },
        "reg":{
            "learning_rate": 0.05,
            "max_iter": 200,
        }
    }
    return hp_config