def get_sweep_config():
    """
    Contains the configuration for hyperparameter sweeps using WandB.
    This configuration is "operational" so modifying it will change the search strategy, parameter ranges, and other settings for hyperparameter tuning aimed at optimizing model performance.

    Returns:
    - sweep_config (dict): A dictionary containing the configuration for hyperparameter sweeps, defining the methods and parameter ranges used to search for optimal hyperparameters.
    """

    sweep_config = {
        'method': 'grid',
    }

    # Example metric setup:
    metric = {
        'name': 'MSE',
        'goal': 'minimize'
    }
    sweep_config['metric'] = metric

    # Example parameters setup:
    parameters_dict = {
        'model': {
            'value': 'LightBGM' # Eg. "LSTM", "CNN", "Transformer"
        },
    }
    sweep_config['parameters'] = parameters_dict

    return sweep_config