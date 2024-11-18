
def get_hp_config():
    """
    Contains the hyperparameter configurations for model training.
    This configuration is "operational" so modifying these settings will impact the model's behavior during the training.

    Returns:
    - hyperparameters (dict): A dictionary containing hyperparameters for training the model, which determine the model's behavior during the training phase.
    """
    
    hyperparameters = {
        "steps": [*range(1, 36 + 1, 1)],
        "parameters": {
            "clf": {
                "n_estimators": 100,
                "learning_rate": 0.05,
                "n_jobs": -2
            },
            "reg": {
                "n_estimators": 100,
                "learning_rate": 0.05,
                "n_jobs": -2
            }
        }
    }
    return hyperparameters
