def get_sweep_config():
    sweep_config = {
        "name": "yellow_pikachu",
        "method": "bayes"
    }

    metric = {
        "name": "MSE",
        "goal": "minimize"   
    }

    sweep_config["metric"] = metric

    parameters_dict = {
        "steps": {"values": [[*range(1, 36 + 1, 1)]]},
        "n_estimators": {"values": [100, 150, 200]},
        "learning_rate": {"min": 0.01, "max": 0.1},
        "n_jobs": {"values": [12]}
    }

    sweep_config["parameters"] = parameters_dict

    return sweep_config