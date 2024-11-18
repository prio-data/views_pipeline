def get_sweep_config():
    sweep_config = {
        "name": "old_money",
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
        "reg_n_estimators": {"values": [100, 200]},
    }

    sweep_config["parameters"] = parameters_dict

    return sweep_config