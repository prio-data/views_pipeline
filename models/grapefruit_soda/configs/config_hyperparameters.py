def get_hyperparameters(): 
    """
    Specifies the finalized hyperparameters used for training (W&B specific).

    Returns:
    - hyperparameters (dict): A dictionary containing hyperparameters for the model.
    """
    hyperparameters = {
        "learning_rate": 0.05, #we don't have this in the Jupyter notebook
        "n_estimators": 100,
        "n_jobs": 2   
    }
    return hyperparameters #formerly hp_config
