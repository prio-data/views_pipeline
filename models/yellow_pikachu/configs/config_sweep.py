def get_swep_config():
    sweep_config = {
        "name": "yellow_pikachu",
        'method': 'grid'
    }

    metric = {
        'name': 'MSE_test',
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