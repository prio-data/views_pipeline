def get_sweep_config():
    sweep_config = {
        "name": "orange_pasta",
        "method": "bayes"
    }

    metric = {
        "name": "MSE",
        "goal": "minimize"   
    }

    sweep_config["metric"] = metric

    parameters_dict = {
        "algorithm": {"values": ["LGBMRegressor"]},
        "depvar": {"values": ["ged_sb_dep"]},
        "steps": {"values": [[*range(1, 36 + 1, 1)]]},
        "n_estimators": {"values": [100, 150, 200]},
        "learning_rate": {"min": 0.01, "max": 0.1},
        "num_leaves": {"values": [31, 63, 127, 255]},
        "n_jobs": {"values": [12]}

    }

    sweep_config["parameters"] = parameters_dict

    return sweep_config