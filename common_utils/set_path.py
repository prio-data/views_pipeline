import logging
import sys
from pathlib import Path
from model_path import ModelPath
from ensemble_path import EnsemblePath

sys.path.append(str(Path(__file__).parent.parent))

from meta_tools.utils.utils_model_paths import get_model_name_from_path

# Configure logging - don't know if this is necessary here
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
_model_path_cache = {}


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
    if model_name not in _model_path_cache:
        logger.info(f"{model_name} not found in cache. Creating new instance...")
        if "models" in path.parts:
            logger.info(f"Creating ModelPath instance for path: {path}")
            model = ModelPath(model_name)
        if "ensembles" in path.parts:
            logger.info(f"Creating EnsemblePath instance for path: {path}")
            model = EnsemblePath(model_name)
        # model = ModelPath(model_name)
        _model_path_cache[model_name] = model
    else:
        model = _model_path_cache[model_name]
    if model.model_dir is None:
        error_message = f"Unable to create ModelPath/EnsemblePath instance for {model_name}. "
        logger.warning(error_message)
        raise ValueError(error_message)
    logger.info(f"Returning cached ModelPath/EnsemblePath instance for path: {path}")
    logger.info(f"Model name: {model.model_name}")
    logger.info(f"Model directory: {model.model_dir}")
    print(_model_path_cache)
    return model


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
    model = get_model_path_instance(PATH)
    MODEL_NAME = model.model_name
    if "views_pipeline" in PATH.parts:
        PATH_ROOT = model.root
        return PATH_ROOT
    else:
        error_message = (
            "The 'views_pipeline' directory was not found in the provided path."
        )
        logger.warning(error_message)
        raise FileNotFoundError(error_message)


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
        # PATH_MODEL = Path(*[i for i in PATH.parts[:PATH.parts.index("models") + 2]])
        model = get_model_path_instance(PATH)
        PATH_MODEL = model.model_dir
        return PATH_MODEL
    else:
        error_message = "The 'models' directory was not found in the provided path."
        logger.warning(error_message)
        raise FileNotFoundError(error_message)


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
        model = get_model_path_instance(PATH)
        PATH_ENSEMBLE = model.model_dir

        return PATH_ENSEMBLE

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

    #    PATH_ROOT  = Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) # The +1 is to include the "views_pipeline" part in the path
    #    PATH_MODEL = Path(*[i for i in PATH.parts[:PATH.parts.index("models")+2]]) # The +2 is to include the "models" and the individual model name in the path
    # print(f"setup_project_paths :: Path : {PATH}")
    model = get_model_path_instance(PATH)
    # PATH_ROOT = model.root
    # PATH_MODEL = None
    # PATH_ENSEMBLE = None
    # if "models" in PATH.parts:
    #     try:
    #         PATH_MODEL = model.model_dir
    #     except ValueError as e:
    #         logger.warning(e)
    # if "ensembles" in PATH.parts:
    #     try:
    #         PATH_ENSEMBLE = model.model_dir
    #     except ValueError as e:       
    #         logger.warning(e)

    # print(f"Root path: {PATH_ROOT}") # debug
    # print(f"Model path: {PATH_MODEL}") # debug

    # Define common paths

    # print(f"Common utils path: {PATH_COMMON_UTILS}") # debug
    # print(f"Common configs path: {PATH_COMMON_CONFIGS}") # debug
    # Define model-specific paths
    # if PATH_MODEL:
        # PATH_COMMON_UTILS = model.common_utils
        # PATH_COMMON_CONFIGS = model.common_configs
        # PATH_COMMON_QUERYSETS = model.common_querysets
        # PATH_CONFIGS = model.configs
        # PATH_SRC = model.src
        # PATH_UTILS = model.utils
        # PATH_MANAGEMENT = model.management # added to keep the management scripts in a separate folder the utils according to Sara's point
        # PATH_ARCHITECTURES = model.architectures
        # PATH_TRAINING = model.training
        # PATH_FORECASTING = model.forecasting
        # PATH_OFFLINE_EVALUATION = model.offline_evaluation
        # PATH_DATALOADERS = model.dataloaders
        # paths_to_add = [PATH_ROOT,
        #                 PATH_COMMON_UTILS,
        #                 PATH_COMMON_CONFIGS,
        #                 PATH_COMMON_QUERYSETS,
        #                 ]
        # extended_paths = model.get_directories().values()
        # extended_paths = [Path(path) for path in paths_to_add if path is not None]
        # paths_to_add.extend(extended_paths)
        # sys.path = model.remove_paths_from_sys(current_sys_path=sys.path)
    model.add_paths_to_sys()

    # Define ensemble paths
    # if PATH_ENSEMBLE:
        # PATH_COMMON_UTILS = PATH_ROOT / "common_utils"
        # PATH_COMMON_CONFIGS = PATH_ROOT / "common_configs"
        # PATH_COMMON_QUERYSETS = PATH_ROOT / "common_querysets"
        # PATH_CONFIGS_E = PATH_ENSEMBLE / "configs"
        # PATH_SRC_E = PATH_ENSEMBLE / "src"
        # PATH_UTILS_E = PATH_SRC_E / "utils"
        # PATH_MANAGEMENT_E = (
        #     PATH_SRC_E / "management"
        # )  # added to keep the management scripts in a separate folder the utils according to Sara's point
        # PATH_ARCHITECTURES_E = PATH_SRC_E / "architectures"
        # PATH_TRAINING_E = PATH_SRC_E / "training"
        # PATH_FORECASTING_E = PATH_SRC_E / "forecasting"
        # PATH_OFFLINE_EVALUATION_E = PATH_SRC_E / "offline_evaluation"
        # PATH_DATALOADERS_E = PATH_SRC_E / "dataloaders"
        # paths_to_add = [
        #     PATH_ROOT,
        #     PATH_COMMON_UTILS,
        #     PATH_COMMON_CONFIGS,
        #     PATH_COMMON_QUERYSETS,
        #     PATH_CONFIGS_E,
        #     PATH_UTILS_E,
        #     PATH_MANAGEMENT_E,
        #     PATH_ARCHITECTURES_E,
        #     PATH_TRAINING_E,
        #     PATH_FORECASTING_E,
        #     PATH_OFFLINE_EVALUATION_E,
        #     PATH_DATALOADERS_E,
        # ]

        # for path in paths_to_add:
        #     # path_str = str(path)
        #     if not Path(path).exists():
        #         Path(path).mkdir(parents=True)
        #     if path not in sys.path:
        #         sys.path.insert(0, str(path))
        # model.add_paths_to_sys()
    # print(f"{sys.path}")


def setup_data_paths(PATH) -> Path:
    """
    Returns the raw, processed, and generated data paths (pathlib path object) for the specified model.

    Args:
    PATH (Path): The base path, typically the path of the script invoking this function (i.e., `Path(__file__)`).
    config (str): The model configuration file.

    """

    # PATH_MODEL = Path(*[i for i in PATH.parts[:PATH.parts.index("models")+2]]) # The +2 is to include the "models" and the individual model name in the path
    # PATH_MODEL = None
    # PATH_ENSEMBLE = None
    # if "models" in PATH.parts:
    #     try:
    #         PATH_MODEL = model.model_dir
    #     except ValueError as e:
    #         logger.warning(e)
    # if "ensembles" in PATH.parts:
    #     try:
    #         PATH_ENSEMBLE = setup_ensemble_paths(PATH)
    #     except ValueError as e:       
    #         logger.warning(e)

    model = get_model_path_instance(PATH)
    # PATH_DATA = model.data
    PATH_RAW = model.data_raw
    PATH_PROCCEDS = model.data_processed
    PATH_GENERATED = model.data_generated

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
    # PATH_MODEL = setup_model_paths(PATH)
    model = get_model_path_instance(PATH)
    PATH_ARTIFACTS = model.artifacts
    return PATH_ARTIFACTS