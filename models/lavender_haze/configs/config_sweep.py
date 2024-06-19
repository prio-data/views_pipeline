def get_sweep_config():
    sweep_config = {
        "name": "lavender_haze",
        "method": "grid"
    }

    metric = {
        "name": "MSE",
        "goal": "minimize"   
    }

    sweep_config["metric"] = metric

    parameters_dict = {
        "algorithm": {"values": ["HurdleRegression"]},
        "model_cls": {"values": ["LGBMClassifier"]},
        "model_reg": {"values": ["LGBMRegressor"]},
        "depvar": {"values": ["ln_ged_sb_dep"]},
        "steps": {"values": [[*range(1, 36 + 1, 1)]]},
        "cls_n_estimators": {"values": [100, 200]},
        "cls_learning_rate": {"values": [0.05]},
        "cls_n_jobs": {"values": [12]},
        "reg_n_estimators": {"values": [100, 200]},
        "reg_learning_rate": {"values": [0.05]},
        "reg_n_jobs": {"values": [12]}
    }

    sweep_config["parameters"] = parameters_dict

    return sweep_config