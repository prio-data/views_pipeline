from sklearn.ensemble import RandomForestClassifier

def get_meta_config():
    """
    Contains the common configuration settings for the model (model architecture, name, target variable, level of analysis and deployment status).

    Returns:
    - model_config (dict): A dictionary containing model configuration settings.
    """
    meta_config = {
        "name": "electric_relaxation",
        "algorithm": RandomForestClassifier, 
        "target": "ged_sb_dep", #or depvar
        "queryset": "escwa001_cflong",
        "level": "cm",
        "sweep": False,
        "force_retrain": False,
        "steps": [*range(1, 36 + 1, 1)],
        "deployment_status": "shadow", #unsure
        "creator": "Sara" #new addition, could be useful for managing maintenance & transfer of ownership
    }
    return meta_config #formerly common_config and model_config