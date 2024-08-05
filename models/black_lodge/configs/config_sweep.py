def get_sweep_config():

    """
    Contains the configuration for hyperparameter sweeps using WandB.
    This configuration is "operational" so modifying it will change the search strategy, parameter ranges, and other settings for hyperparameter tuning aimed at optimizing model performance.
    
    Returns:
    - sweep_config (dict): A dictionary containing the configuration for hyperparameter sweeps, defining the methods and parameter ranges used to search for optimal hyperparameters.
    """
 
    sweep_config = {
    'name': 'black_lodge',
    'method': 'grid' 
    }

    metric = {
        'name': '36month_mean_squared_error',
        'goal': 'minimize'   
        }

    sweep_config['metric'] = metric

    parameters_dict = {        
        "n_estimators": {"values": [100, 200]},
        "learning_rate": {"values": [0.05]},
        "n_jobs": {"values": [12]},
        } #taken from xiaolong's code

    sweep_config['parameters'] = parameters_dict

    return sweep_config