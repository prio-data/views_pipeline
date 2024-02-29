def get_hp_config(): 
    """
    Retrieves the hyperparameter configuration for model training.

    Returns:
    - hp_config (dict): A dictionary containing hyperparameters for the model.

    Notes:
    - The function returns a dictionary with hyperparameters such as learning rate, number of estimators, and number of jobs.
    - Hyperparameters are commonly used in machine learning algorithms to control the learning process.
    """
    hp_config = {
        "learning_rate": 0.05, #we don't have this in the Jupyter notebook
        "n_estimators": 100,
        "n_jobs": 2   
    }
    return hp_config
