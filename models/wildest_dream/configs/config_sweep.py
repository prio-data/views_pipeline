def get_swep_config():
    sweep_config = {
        "name": "wildest_dream",
        'method': 'grid'
    }

    metric = {
        'name': 'MSE_calib',
        'goal': 'minimize'   
    }

    sweep_config['metric'] = metric

    parameters_dict = {
        "cls_max_iter": {"values": [100, 200]},
        "cls_learning_rate": {"values": [0.05]},
        "reg_max_iter": {"values": [100, 200]},
        "reg_learning_rate": {"values": [0.05]},
    }

    sweep_config['parameters'] = parameters_dict

    return sweep_config