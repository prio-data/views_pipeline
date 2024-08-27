def get_sweep_config():
    """
    Configurations for hyperparameter sweeps during experimentation phases (W&B specific).

    Comment: add "criterion" and "max_depth" 
    """
    sweep_config = {
        "name": "electric_relaxation",
        "method": "grid" 
    }

    metric = {
        "name": "MSE",
        "goal": "minimize"   
    }

    sweep_config["metric"] = metric

    parameters_dict = {
        "n_estimators": {"values": [100, 200]},
        "learning_rate": {"values": [0.05]},
        "n_jobs": {"values": [12]}
    }

    sweep_config["parameters"] = parameters_dict

    return sweep_config