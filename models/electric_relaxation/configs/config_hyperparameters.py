def get_hp_config(): 
    """
    Specifies the finalized hyperparameters used for training.

    Returns:
    - hyperparameters (dict): A dictionary containing hyperparameters for the model.
    """
    hp_config = {
        "learning_rate": 0.05, #we don't have this in the Jupyter notebook
        "n_estimators": 100,
        "n_jobs": 2
        #"criterion": ,
        #"max_depth": 
    }
    return hp_config
