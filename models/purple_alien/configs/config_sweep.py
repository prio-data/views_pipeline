def get_swep_config():
    sweep_config = {
    'method': 'grid'
    }

    metric = {
        'name': '36month_mean_squared_error',
        'goal': 'minimize'   
        }

    sweep_config['metric'] = metric

    parameters_dict = {
        'model' : {'value' :'HydraBNUNet06_LSTM4'},
        'weight_init' : {'value' : 'xavier_norm'}, # ['xavier_uni', 'xavier_norm', 'kaiming_uni', 'kaiming_normal']
        'clip_grad_norm' : {'value': True},
        'scheduler' : {'value': 'WarmupDecay'}, #CosineAnnealingLR004  'CosineAnnealingLR' 'OneCycleLR'
        'total_hidden_channels': {'value': 32}, # you like need 32, it seems from qualitative results
        'min_events': {'value': 5},
        'samples': {'value': 10}, # 600 for run 10 for debug. should be a function of batches becaus batch 3 and sample 1000 = 3000....
        'batch_size': {'value':  3}, # just speed running here..
        "dropout_rate" : {'value' : 0.125},
        'learning_rate': {'value' :  0.001}, #0.001 default, but 0.005 might be better
        "weight_decay" : {'value' : 0.1},
        "slope_ratio" : {'value' : 0.75},
        "roof_ratio" : {'value' :  0.7},
        'input_channels' : {'value' : 3},
        'output_channels': {'value' : 1},
        'targets' : {'value' : 6}, # 3 class and 3 reg for now. And for now this parameter is only used in utils, and changing it does not change the model - so don't.
        'loss_class' : { 'value' : 'b'}, # det nytter jo ikke noget at du køre over gamma og alpha for loss-class a...
        'loss_class_gamma' : {'value' : 1.5},
        'loss_class_alpha' : {'value' : 0.75}, # should be between 0.5 and 0.95...
        'loss_reg' : { 'value' :  'b'},
        'loss_reg_a' : { 'value' : 256},
        'loss_reg_c' : { 'value' : 0.001},
        'test_samples': { 'value' :10}, # 128 for actual testing, 10 for debug
        'np_seed' : {'values' : [4,8]},
        'torch_seed' : {'values' : [4,8]},
        'window_dim' : {'value' : 32},
        'h_init' : {'value' : 'abs_rand_exp-100'},
        'un_log' : {'value' : False},
        'warmup_steps' : {'value' : 100},
        'first_feature_idx' : {'value' : 5},
        'norm_target' : {'value' : False},
        'freeze_h' : {'value' : "hl"},
        'time_steps' : {'value' : 36}
        }

    sweep_config['parameters'] = parameters_dict

    return sweep_config
