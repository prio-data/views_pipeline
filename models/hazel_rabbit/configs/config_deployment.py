def get_deployment_config():

    """
    Contains the configuration for deploying the model into different environments.
    This configuration is "behavioral" so modifying it will affect the model's runtime behavior and integration into the deployment system.

    Returns:
    - deployment_config (dict): A dictionary containing deployment settings, determining how the model is deployed, including status, endpoints, and resource allocation.
    """

    # More deployment settings can/will be added here
    deployment_config = {
       "deployment_status": "baseline", # shadow, deployed, baseline, or deprecated
    }

    return deployment_config