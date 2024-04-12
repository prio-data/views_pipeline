from sklearn.ensemble import RandomForestClassifier

def get_model_config():
    """
    Contains the common configuration settings for the model (model architecture, name, target variable, level of analysis and deployment status).

    Returns:
    - model_config (dict): A dictionary containing model configuration settings.
    """
    model_config = {
        "name": "electric_relaxation",
        "algorithm": RandomForestClassifier, 
        "depvar": "ged_sb_dep", #or target? 
        "queryset": "escwa001_cflong",
        "level": "cm",
        "sweep": False,
        "force_retrain": False,
        "steps": [*range(1, 36 + 1, 1)],
        "deployment_status": "shadow", #unsure
        "creator": "Sara" #new addition, could be useful for managing maintenance & transfer of ownership
    }
    return model_config #formerly common_config