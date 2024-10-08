def get_hp_config(): 
    """
    Specifies the finalized hyperparameters used for training.

    Returns:
    - hyperparameters (dict): A dictionary containing hyperparameters for the model.
    """
    hp_config = {
        "steps": [*range(1, 36 + 1, 1)],
        "parameters": {
            "n_estimators": 100,
            "n_jobs": 2
        }
    }
    return hp_config
