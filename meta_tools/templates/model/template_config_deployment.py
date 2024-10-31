from typing import Dict
from utils import utils_script_gen
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate(
    script_dir: Path,
    deployment_type: str = "shadow",
    additional_settings: Dict[str, any] = None,
) -> bool:
    """
    Generates a script that defines the `get_deployment_config` function for configuring the deployment status and settings.

    Parameters:
        script_dir (Path): The directory where the generated deployment configuration script will be saved.
                           This should be a valid writable path.
        deployment_type (str, optional):
            The type of deployment. Must be one of "shadow", "deployed", "baseline", or "deprecated".
            Default is "shadow".
            - "shadow": The deployment is shadowed and not yet active.
            - "deployed": The deployment is active and in use.
            - "baseline": The deployment is in a baseline state, for reference or comparison.
            - "deprecated": The deployment is deprecated and no longer supported.
        additional_settings (dict, optional):
            A dictionary of additional settings to include in the deployment configuration.
            These settings will be merged with the default configuration. Defaults to None.

    Raises:
    ValueError: If `deployment_type` is not one of the valid types.

    Returns:
    bool: True if the script was written and compiled successfully, False otherwise.
    """
    valid_types = {"shadow", "deployed", "baseline", "deprecated"}
    if deployment_type.lower() not in valid_types:
        logging.error(
            f"Invalid deployment_type: {deployment_type}. Must be one of {valid_types}."
        )
        raise ValueError(
            f"Invalid deployment_type: {deployment_type}. Must be one of {valid_types}."
        )

    deployment_config = {"deployment_status": deployment_type.lower()}

    # Merge additional settings if provided
    if additional_settings and isinstance(additional_settings, dict):
        deployment_config.update(additional_settings)

    # Generate the script code
    code = f"""\"\"\"
Deployment Configuration Script

This script defines the deployment configuration settings for the application. 
It includes the deployment status and any additional settings specified.

Deployment Status:
- shadow: The deployment is shadowed and not yet active.
- deployed: The deployment is active and in use.
- baseline: The deployment is in a baseline state, for reference or comparison.
- deprecated: The deployment is deprecated and no longer supported.

Additional settings can be included in the configuration dictionary as needed.

\"\"\"

def get_deployment_config():
    # Deployment settings
    deployment_config = {deployment_config}
    return deployment_config
"""
    return utils_script_gen.save_script(script_dir, code)
