def get_swep_config():
    sweep_config = {
        "name": "lavender_haze",
        'method': 'grid'
    }

    metric = {
        'name': 'MSE_calib',
        'goal': 'minimize'   
    }

    sweep_config['metric'] = metric

    parameters_dict = {
        "cls_n_estimators": {"values": [100, 200]},
        "cls_learning_rate": {"values": [0.05]},
        "cls_n_jobs": {"values": [12]},
        "reg_n_estimators": {"values": [100, 200]},
        "reg_learning_rate": {"values": [0.05]},
        "reg_n_jobs": {"values": [12]}
    }

    sweep_config['parameters'] = parameters_dict

    return sweep_config