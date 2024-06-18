def get_swep_config():

    """
    Contains the configuration for hyperparameter sweeps using WandB.
    This configuration is "operational" so modifying it will change the search strategy, parameter ranges, and other settings for hyperparameter tuning aimed at optimizing model performance.
    
    Returns:
    - sweep_config (dict): A dictionary containing the configuration for hyperparameter sweeps, defining the methods and parameter ranges used to search for optimal hyperparameters.
    """
 
    sweep_config = {
    'name': 'black_lodge',
    'method': 'country' #or grid 
    }

    metric = {
        'name': '36month_mean_squared_error',
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
        } #taken from xiaolong's code

    sweep_config['parameters'] = parameters_dict

    return sweep_config