def get_swep_config():
    sweep_config = {
        "name": "orange_pasta",
        "method": "bayes"
    }

    metric = {
        "name": "MSE_test",
        "goal": "minimize"   
    }

    sweep_config["metric"] = metric

    parameters_dict = {
        "n_estimators": {"values": [100, 150, 200]},
        "learning_rate": {"min": 0.01, "max": 0.1},
        "num_leaves": {"values": [31, 63, 127, 255]},
        "n_jobs": {"values": [12]}
    }

    sweep_config["parameters"] = parameters_dict

    early_terminate =  {
        'type': 'hyperband',
        'min_iter': 12,
        'eta': 4
    }

    sweep_config["early_terminate"] = early_terminate

    return sweep_config