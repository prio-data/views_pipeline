from pathlib import Path
import logging
import sys

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
sys.path.append(str(Path(__file__).parent))

def find_project_root(marker="LICENSE.md") -> Path:
    """
    Finds the base directory of the project by searching for a specific marker file or directory.
    Args:
        marker (str): The name of the marker file or directory that indicates the project root.
                    Defaults to 'LICENSE.md'.
    Returns:
        Path: The path of the project root directory.
    Raises:
        FileNotFoundError: If the marker file/directory is not found up to the root directory.
    """
    # Start from the current directory and move up the hierarchy
    current_path = Path(__file__).resolve().parent
    while current_path != current_path.parent:  # Loop until we reach the root directory
        if (current_path / marker).exists():
            return current_path
        current_path = current_path.parent
    raise FileNotFoundError(
        f"{marker} not found in the directory hierarchy. Unable to find project root."
    )

def get_model_name_from_path(path) -> str:
    """
    Returns the model name based on the provided path.

    Args:
        PATH (Path): The base path, typically the path of the script invoking this function (e.g., `Path(__file__)`).

    Returns:
        str: The model name extracted from the provided path.

    Raises:
        ValueError: If the model name is not found in the provided path.
    """
    from utils_model_naming import validate_model_name  # Local import to avoid circular dependency

    path = Path(path)
    logger.info(f"Extracting model name from Path: {path}")
    if "models" in path.parts and "ensembles" not in path.parts:
        try:
            model_idx = path.parts.index("models")
            model_name = path.parts[model_idx + 1]
            if validate_model_name(model_name):
                logger.info(f"Valid model name {model_name} found in path {path}")
                return str(model_name)
            else:
                error_message = f"Invalid model name `{model_name}` found in path {path}. Please provide a valid model name that follows the lowercase 'adjective_noun' format."
                logger.error(error_message)
                raise ValueError(error_message)
        except Exception as e:
            logger.error(f"Could not find model name in path: {e}")
    if "ensembles" in path.parts and "models" not in path.parts:
        try:
            ensemble_idx = path.parts.index("ensembles")
            ensemble_name = path.parts[ensemble_idx + 1]
            if validate_model_name(ensemble_name):
                logger.info(f"Valid model name {ensemble_name} found in path {path}")
                return str(ensemble_name)
            else:
                error_message = f"Invalid ensemble name `{ensemble_name}` found in path. Please provide a valid ensemble name that follows the lowercase 'adjective_noun' format."
                logger.error(error_message)
                raise ValueError(error_message)
        except Exception as e:
            logger.error(f"Could not find ensemble name in path: {e}")  
    else:
        error_message = (
            "No model or ensemble directory found in path. Please provide a valid path."
        )
        logger.warning(error_message)
        raise ValueError(error_message)