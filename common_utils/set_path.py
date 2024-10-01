import sys
from pathlib import Path


def setup_root_paths(PATH) -> Path:
    """
    Extracts and returns the root path (pathlib path object) up to and including the "views_pipeline" directory from any given path.
    This function identifies the "views_pipeline" directory within the provided path and constructs a new path up to and including this directory.
    This is useful for setting up root paths for project-wide resources and utilities.

    Args:
        PATH (Path): The base path, typically the path of the script invoking this function (e.g., `PATH = Path(__file__)`).

    Returns:
        PATH_ROOT: The root path (pathlib path object) including the "views_pipeline" directory.
    """

    PATH_ROOT = Path(
        *[i for i in PATH.parts[: PATH.parts.index("views_pipeline") + 1]]
    )  # The +1 is to include the "views_pipeline" part in the path
    return PATH_ROOT


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

    PATH_MODEL = Path(
        *[i for i in PATH.parts[: PATH.parts.index("models") + 2]]
    )  # The +2 is to include the "models" and the individual model name in the path
    return PATH_MODEL


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
    PATH_MODEL = setup_model_paths(PATH)

    # print(f"Root path: {PATH_ROOT}") # debug
    # print(f"Model path: {PATH_MODEL}") # debug

    # Define common paths
    PATH_COMMON_UTILS = PATH_ROOT / "common_utils"
    PATH_COMMON_CONFIGS = PATH_ROOT / "common_configs"

    # print(f"Common utils path: {PATH_COMMON_UTILS}") # debug
    # print(f"Common configs path: {PATH_COMMON_CONFIGS}") # debug

    # Define model-specific paths
    PATH_CONFIGS = PATH_MODEL / "configs"
    PATH_SRC = PATH_MODEL / "src"
    PATH_UTILS = PATH_SRC / "utils"
    PATH_MANAGEMENT = (
        PATH_SRC / "management"
    )  # added to keep the management scripts in a separate folder the utils according to Sara's point
    PATH_ARCHITECTURES = PATH_SRC / "architectures"
    PATH_TRAINING = PATH_SRC / "training"
    PATH_FORECASTING = PATH_SRC / "forecasting"
    PATH_OFFLINE_EVALUATION = PATH_SRC / "offline_evaluation"
    PATH_DATALOADERS = PATH_SRC / "dataloaders"

    # new
    # PATH_ARTIFACTS = PATH_MODEL / "artifacts"
    # alredy defined in setup_artifacts_paths

    PATH_NOTEBOOKS = PATH_MODEL / "notebooks"
    PATH_REPORTS = PATH_MODEL / "reports"
    PATH_VISUALIZATION = PATH_SRC / "visualization"
    PATH_ONLINE_EVALUATION = PATH_SRC / "online_evaluation"

    paths_to_add = [
        PATH_ROOT,
        PATH_COMMON_UTILS,
        PATH_COMMON_CONFIGS,
        PATH_CONFIGS,
        PATH_UTILS,
        PATH_MANAGEMENT,
        PATH_ARCHITECTURES,
        PATH_TRAINING,
        PATH_FORECASTING,
        PATH_OFFLINE_EVALUATION,
        PATH_DATALOADERS,
    ]

    for path in paths_to_add:
        path_str = str(path)
        if (
            path.exists() and path_str not in sys.path
        ):  # whith the current implementation, PATH_COMMON_UTILS is already in sys.path and will not be added (or printed) again
            # print(f"Adding {path_str} to sys.path") # debug
            sys.path.insert(0, path_str)


def setup_data_paths(PATH) -> Path:
    """
    Returns the raw, processed, and generated data paths (pathlib path object) for the specified model.

    Args:
    PATH (Path): The base path, typically the path of the script invoking this function (i.e., `Path(__file__)`).
    config (str): The model configuration file.

    """

    # PATH_MODEL = Path(*[i for i in PATH.parts[:PATH.parts.index("models")+2]]) # The +2 is to include the "models" and the individual model name in the path
    PATH_MODEL = setup_model_paths(PATH)

    PATH_DATA = PATH_MODEL / "data"
    PATH_RAW = PATH_DATA / "raw"
    PATH_PROCCEDS = PATH_DATA / "processed"
    PATH_GENERATED = PATH_DATA / "generated"

    return (
        PATH_RAW,
        PATH_PROCCEDS,
        PATH_GENERATED,
    )  # added in accordance with Sara's escwa branch


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
    # print(f"Artifacts path: {PATH_ARTIFACTS}")
    return PATH_ARTIFACTS
