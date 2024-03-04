def sweep_config():
    """
    Configurations for hyperparameter sweeps during experimentation phases (W&B specific).
    """
    sweep_config = {
        "name": "grapefruit_soda",
        'method': 'grid' #cm?
    }

    metric = {
        'name': 'mse',
        'goal': 'minimize'   
    }

    sweep_config['metric'] = metric

    parameters_dict = {
        "n_estimators": {"values": [100, 200]},
        "learning_rate": {"values": [0.05]},
        "n_jobs": {"values": [12]}
    }

    sweep_config['parameters'] = parameters_dict

    return sweep_config