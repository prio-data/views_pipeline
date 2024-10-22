import logging
import sys
from pathlib import Path
from model_path import ModelPath
from ensemble_path import EnsemblePath

sys.path.append(str(Path(__file__).parent.parent))

from meta_tools.utils.utils_model_paths import get_model_name_from_path
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_model_path_instance(path) -> ModelPath:
    """
    Retrieve a cached instance of ModelPath or create a new one if not cached.

    This function checks if a ModelPath instance corresponding to the given path is already cached. 
    If not, it creates a new instance of either ModelPath or EnsemblePath based on the directory structure of the path.

    Parameters:
        path (Path): The path to create or retrieve the ModelPath instance for.

    Returns:
        ModelPath: The cached or newly created ModelPath instance.

    Raises:
        ValueError: If the ModelPath instance cannot be created due to missing model directory.
    """

    model_name = get_model_name_from_path(path)
    if "models" in path.parts:
        logger.debug(f"Getting ModelPath instance for path: {path}")
        model_path = ModelPath(model_name, force_cache_overwrite=False)
    if "ensembles" in path.parts:
        logger.debug(f"Getting EnsemblePath instance for path: {path}")
        model_path = EnsemblePath(model_name, force_cache_overwrite=False)
    return model_path




def setup_root_paths(PATH) -> Path:
    """
    Extract and return the root path up to and including the "views_pipeline" directory.

    This function identifies the root directory within the provided path and constructs a new path up to and including this directory.
    This is useful for setting up root paths for project-wide resources and utilities.

    Parameters:
        PATH (Path): The base path, typically the path of the script invoking this function (e.g., `PATH = Path(__file__)`).

    Returns:
        Path: The root path including the "views_pipeline" directory.

    Raises:
        ValueError: If the "views_pipeline" directory is not found in the provided path.
    """
    model_path = get_model_path_instance(PATH)
    if "views_pipeline" in PATH.parts:
        return model_path.root
    else:
        error_message = (
            "The 'views_pipeline' directory was not found in the provided path."
        )
        logger.warning(error_message)
        raise FileNotFoundError(error_message)


def setup_model_paths(PATH):
    """
    Extract and return the model-specific path including the "models" directory and its immediate subdirectory.

    This function identifies the "models" directory within the provided path and constructs a new path up to and including the next subdirectory after "models".
    This is useful for setting up paths specific to a model within the project.

    Parameters:
        PATH (Path): The base path, typically the path of the script invoking this function (e.g., `PATH = Path(__file__)`).

    Returns:
        Path: The path including the "models" directory and its immediate subdirectory.

    Raises:
        FileNotFoundError: If the "models" directory is not found in the provided path.
    """
    if "models" in PATH.parts:
        model_path = get_model_path_instance(PATH)
        return model_path.model_dir
    else:
        error_message = "The 'models' directory was not found in the provided path."
        logger.warning(error_message)
        raise FileNotFoundError(error_message)


def setup_ensemble_paths(PATH):
    """
    Extract and return the model-specific path including the "ensembles" directory and its immediate subdirectory.

    This function identifies the "ensembles" directory within the provided path and constructs a new path up to and including the next subdirectory after "ensembles".
    This is useful for setting up paths specific to a model within the project.

    Parameters:
        PATH (Path): The base path, typically the path of the script invoking this function (e.g., `PATH = Path(__file__)`).

    Returns:
        Path: The path including the "ensembles" directory and its immediate subdirectory.

    Raises:
        FileNotFoundError: If the "ensembles" directory is not found in the provided path.
    """
    if "ensembles" in PATH.parts:
        model_path = get_model_path_instance(PATH)
        return model_path.model_dir
    else:
        error_message = "The 'ensembles' directory was not found in the provided path."
        logger.warning(error_message)
        raise FileNotFoundError(error_message)


def setup_project_paths(PATH) -> None:
    """
    Configures project-wide access to common utilities, configurations, and model-specific paths by adjusting `sys.path`.

    This function should be called at the start of a script to ensure consistent and machine-agnostic path resolution throughout the project. It dynamically sets up paths relative to the specified base path, facilitating access to shared resources located in `common_utils` and `common_configs`, as well as model-specific directories within `models`.

    Args:
        PATH (Path): The base path, typically the path of the script invoking this function (i.e., `Path(__file__)`).
        Following the usage example below, this is automatically passed to the function by the script.

    Usage:
        To ensure all necessary project paths are accessible, add the following to the start of each project script:

        ```python
            import sys
            from pathlib import Path

            PATH = Path(__file__)
            sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS

            from set_path import setup_project_paths
            setup_project_paths(PATH)
        ```

    Note: Paths are only added to sys.path if they exist and are not already included `(e.g. PATH_COMMON_UTILS), to avoid redundancy.
    Disclaimer: A solution that avoids the insertion of the code above would be preferred.
    """
    model_path = get_model_path_instance(PATH)
    model_path.add_paths_to_sys()

def setup_data_paths(PATH) -> Path:
    """
    Return the raw, processed, and generated data paths for the specified model.

    Parameters:
        PATH (Path): The base path, typically the path of the script invoking this function (i.e., `Path(__file__)`).

    Returns:
        tuple: A tuple containing the raw, processed, and generated data paths.
    """
    model_path = get_model_path_instance(PATH)
    return (
        model_path.data_raw,
        model_path.data_processed,
        model_path.data_generated,
    )


def setup_artifacts_paths(PATH) -> Path:
    """
    Return the paths for the artifacts for the specified model.

    Parameters:
        PATH (Path): The base path, typically the path of the script invoking this function (i.e., `Path(__file__)`).

    Returns:
        Path: The path to the artifacts directory.
    """
    model_path = get_model_path_instance(PATH)
    return model_path.artifacts