def get_sweep_config():
    sweep_config = {
        "name": "wildest_dream",
        "method": "grid"
    }

    metric = {
        "name": "MSE",
        "goal": "minimize"   
    }

    sweep_config["metric"] = metric

    parameters_dict = {
        "steps": {"values": [[*range(1, 36 + 1, 1)]]},
        "cls_n_estimators": {"values": [100, 200]},
        "cls_n_jobs": {"values": [12]},
        "reg_n_estimators": {"values": [100, 200]},
        "reg_n_jobs": {"values": [12]}
    }

    sweep_config["parameters"] = parameters_dict

    return sweep_config