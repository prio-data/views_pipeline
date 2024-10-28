def get_hp_config():
    """
    Contains the hyperparameter configurations for model training.
    This configuration is "operational" so modifying these settings will impact the model's behavior during the training.

    Returns:
    - hyperparameters (dict): A dictionary containing hyperparameters for training the model, which determine the model's behavior during the training phase.
    """
    
    hyperparameters = {
        'model': 'LightBGM',  # The model algorithm used. Eg. "LSTM", "CNN", "Transformer"
        # Add more hyperparameters as needed
    }
    return hyperparameters
