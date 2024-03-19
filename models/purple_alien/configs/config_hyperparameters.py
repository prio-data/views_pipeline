    
def get_hp_config():
    
    hyperparameters = {
    'model' : 'HydraBNUNet06_LSTM4', #'BNUNet',
    'weight_init' : 'xavier_norm',
    'clip_grad_norm' : True,
    'scheduler' : 'WarmupDecay', #  'CosineAnnealingLR' 'OneCycleLR'
    'total_hidden_channels' : 32,
    'min_events' : 5,
    'samples': 600, # 10 just for debug
    'batch_size': 3, 
    'dropout_rate' : 0.125,
    'learning_rate' :  0.001,
    'weight_decay' :  0.1,
    'slope_ratio' : 0.75,
    'roof_ratio' : 0.7,
    'input_channels' : 3,
    'output_channels' : 1,
    'targets' : 6, # 3 class and 3 reg for now. And for now this parameter is only used in utils, and changing it does not change the model - so don't.
    'loss_class': 'b',  # band c are is still unstable... c is old, d = FocalLoss_new
    'loss_class_gamma' : 1.5, # 0 and 2 works. But 2 gives a lot of noise. "If you want to prioritize hard cases in your training and make your model focus more on misclassified or uncertain examples, you should consider setting gamma to a value greater than 1""
    'loss_class_alpha' : 0.75, #An alpha value of 0.75 means that you are assigning more weight to the minority class during training.
    'loss_reg': 'b',
    'loss_reg_a' : 258, 
    'loss_reg_c' :  0.001, # 0.05 works...
    'test_samples': 128,
    'np_seed' : 4,
    'torch_seed' : 4,
    'window_dim' : 32,
    'h_init' : 'abs_rand_exp-100',
    'un_log' : False, # right now this is just as a note to self. Can't change it here} and it is not true..
    'warmup_steps' : 100,
    'first_feature_idx' : 5,
    'norm_target' : False,
    'freeze_h' : "hl", # "all", "random", "hl", "hs", "none" - you should use "hl" for now!
    'time_steps' : 36, # 36 right?
   }
    return hyperparameters
