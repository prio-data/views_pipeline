    
def get_hp_config():

    """
    Contains the hyperparameter configurations for model training.
    This configuration is "operational" so modifying these settings will impact the model's behavior during training.

    Returns:
    - hyperparameters (dict): A dictionary containing hyperparameters for training the model, which determine the model's behavior during the training phase.
    """

    hyperparameters = {
    'sweep' : False, # no sweep for the zero baseline model
    'partitioner' : False, # True: if hardcoded months from set_partitioner.py are used, False: max months - time_steps
    'save_generated' : True, # save evaulation results in the generated folder 
    'time_steps' : 36, # 36 right?
   }
    return hyperparameters
