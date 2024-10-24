import logging
import sys
from pathlib import Path

# Configure logging - don't know if this is necessary here
# logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def setup_root_paths(PATH) -> Path:
    """
    Extracts and returns the root path (pathlib path object) up to and including the "views_pipeline" directory from any given path.
    This function identifies the "views_pipeline" directory within the provided path and constructs a new path up to and including this directory.
    This is useful for setting up root paths for project-wide resources and utilities.

    Args:
        PATH (Path): The base path, typically the path of the script invoking this function (e.g., `PATH = Path(__file__)`).

    Returns:
        PATH_ROOT: The root path (pathlib path object) including the "views_pipeline" directory.

    Raises:
        ValueError: If the "views_pipeline" directory is not found in the provided path.
    """
    if "views_pipeline" in PATH.parts:
        PATH_ROOT = Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]])
        return PATH_ROOT
    else:
        error_message = "The 'views_pipeline' directory was not found in the provided path."
        logger.warning(error_message)
        raise ValueError(error_message)


def setup_model_paths(PATH):
    """
    Extracts and returns the model-specific path (pathlib path object) including the "models" directory and its immediate subdirectory.
    This function identifies the "models" (e.g. purple_alien or orange_pasta) directory within the provided path and constructs a new path up to and including the next subdirectory after "models".
    This is useful for setting up paths specific to a model within the project.

    Args:
        PATH (Path): The base path, typically the path of the script invoking this function (e.g., `PATH = Path(__file__)`).

    Returns:
        PATH_model: The path (pathlib path object) including the "models" directory and its immediate subdirectory.
    """

    if "models" in PATH.parts:
        PATH_MODEL = Path(*[i for i in PATH.parts[:PATH.parts.index("models") + 2]])
        return PATH_MODEL
    else:
        # error_message = "The 'models' directory was not found in the provided path."
        # logger.warning(error_message)
        # raise ValueError(error_message)
        return None
    

def setup_ensemble_paths(PATH):
    """
    Extracts and returns the model-specific path (pathlib path object) including the "ensembles" directory and its immediate subdirectory.
    This function identifies the "ensembles" (e.g. white_mustang) directory within the provided path and constructs a new path up to and including the next subdirectory after "ensembles".
    This is useful for setting up paths specific to a model within the project.

    Args:
        PATH (Path): The base path, typically the path of the script invoking this function (e.g., `PATH = Path(__file__)`).

    Returns:
        PATH_ENSEMBLE: The path (pathlib path object) including the "ensembles" directory and its immediate subdirectory.
    """
    if "ensembles" in PATH.parts:
        PATH_ENSEMBLE = Path(*[i for i in PATH.parts[:PATH.parts.index("ensembles") + 2]])
        return PATH_ENSEMBLE
    
    else:
        # error_message = "The 'ensembles' directory was not found in the provided path."
        # logger.warning(error_message)
        # raise ValueError(error_message)
        return None

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

    #    PATH_ROOT  = Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) # The +1 is to include the "views_pipeline" part in the path
    #    PATH_MODEL = Path(*[i for i in PATH.parts[:PATH.parts.index("models")+2]]) # The +2 is to include the "models" and the individual model name in the path

    PATH_ROOT = setup_root_paths(PATH)
    

    try:
        PATH_MODEL = setup_model_paths(PATH)
    except ValueError as e:
        PATH_MODEL = None
        logger.warning(e)

    try:
        PATH_ENSEMBLE = setup_ensemble_paths(PATH)
    except ValueError as e:
        PATH_ENSEMBLE = None
        logger.warning(e)

    # print(f"Root path: {PATH_ROOT}") # debug
    # print(f"Model path: {PATH_MODEL}") # debug

    # Define common paths
    PATH_COMMON_UTILS = PATH_ROOT / "common_utils"
    PATH_COMMON_CONFIGS = PATH_ROOT / "common_configs"
    PATH_COMMON_QUERYSETS = PATH_ROOT / "common_querysets"

    # print(f"Common utils path: {PATH_COMMON_UTILS}") # debug
    # print(f"Common configs path: {PATH_COMMON_CONFIGS}") # debug

    # Define model-specific paths
    if PATH_MODEL:
        PATH_CONFIGS = PATH_MODEL / "configs"
        PATH_SRC = PATH_MODEL / "src"
        PATH_UTILS = PATH_SRC / "utils"
        PATH_MANAGEMENT = PATH_SRC / "management" # added to keep the management scripts in a separate folder the utils according to Sara's point
        PATH_ARCHITECTURES = PATH_SRC / "architectures"
        PATH_TRAINING = PATH_SRC / "training"
        PATH_FORECASTING = PATH_SRC / "forecasting"
        PATH_OFFLINE_EVALUATION = PATH_SRC / "offline_evaluation"
        PATH_DATALOADERS = PATH_SRC / "dataloaders"
        paths_to_add = [PATH_ROOT, 
                        PATH_COMMON_UTILS, 
                        PATH_COMMON_CONFIGS, 
                        PATH_COMMON_QUERYSETS,
                        PATH_CONFIGS, 
                        PATH_UTILS, 
                        PATH_MANAGEMENT, 
                        PATH_ARCHITECTURES, 
                        PATH_TRAINING,
                        PATH_FORECASTING, 
                        PATH_OFFLINE_EVALUATION, 
                        PATH_DATALOADERS]

    # Define ensemble paths
    if PATH_ENSEMBLE:
        PATH_CONFIGS_E = PATH_ENSEMBLE / "configs"
        PATH_SRC_E = PATH_ENSEMBLE / "src"
        PATH_UTILS_E = PATH_SRC_E / "utils"
        PATH_MANAGEMENT_E = PATH_SRC_E / "management"  # added to keep the management scripts in a separate folder the utils according to Sara's point
        PATH_ARCHITECTURES_E = PATH_SRC_E / "architectures"
        PATH_TRAINING_E = PATH_SRC_E / "training"
        PATH_FORECASTING_E = PATH_SRC_E / "forecasting"
        PATH_OFFLINE_EVALUATION_E = PATH_SRC_E / "offline_evaluation"
        PATH_DATALOADERS_E = PATH_SRC_E / "dataloaders"
        paths_to_add = [PATH_ROOT,
                        PATH_COMMON_UTILS,
                        PATH_COMMON_CONFIGS,
                        PATH_COMMON_QUERYSETS,
                        PATH_CONFIGS_E,
                        PATH_UTILS_E,
                        PATH_MANAGEMENT_E,
                        PATH_ARCHITECTURES_E,
                        PATH_TRAINING_E,
                        PATH_FORECASTING_E,
                        PATH_OFFLINE_EVALUATION_E,
                        PATH_DATALOADERS_E]

    for path in paths_to_add:
        path_str = str(path)
        if not path.exists():
            path.mkdir(parents=True)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)


def setup_data_paths(PATH) -> Path:
    """
    Returns the raw, processed, and generated data paths (pathlib path object) for the specified model.

    Args:
    PATH (Path): The base path, typically the path of the script invoking this function (i.e., `Path(__file__)`).
    config (str): The model configuration file.

    """

    # PATH_MODEL = Path(*[i for i in PATH.parts[:PATH.parts.index("models")+2]]) # The +2 is to include the "models" and the individual model name in the path
    try:
        PATH_MODEL = setup_model_paths(PATH)
    except ValueError as e:
        PATH_MODEL = None
        logger.warning(e)

    try:
        PATH_ENSEMBLE = setup_ensemble_paths(PATH)
    except ValueError as e:
        PATH_ENSEMBLE = None
        logger.warning(e)

    PATH_DATA = PATH_MODEL / "data" if PATH_MODEL else PATH_ENSEMBLE / "data"
    PATH_RAW = PATH_DATA / "raw"
    PATH_PROCCEDS = PATH_DATA / "processed"
    PATH_GENERATED = PATH_DATA / "generated"

    return (
        PATH_RAW,
        PATH_PROCCEDS,
        PATH_GENERATED,
    )


def setup_artifacts_paths(PATH) -> Path:
    """
    Returns the paths (pathlib path object) for the artifacts for the specified model.

    Args:
    PATH (Path): The base path, typically the path of the script invoking this function (i.e., `Path(__file__)`).
    config (str): The model configuration file.

    """

    # PATH_MODEL = Path(*[i for i in PATH.parts[:PATH.parts.index("models")+2]]) # The +2 is to include the "models" and the individual model name in the path
    PATH_MODEL = setup_model_paths(PATH)

    PATH_ARTIFACTS = PATH_MODEL / "artifacts"
    return PATH_ARTIFACTS