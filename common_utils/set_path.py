import sys
from pathlib import Path

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

    PATH_ROOT  = Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) # The +1 is to include the "views_pipeline" part in the path
    PATH_MODEL = Path(*[i for i in PATH.parts[:PATH.parts.index("models")+2]]) # The +2 is to include the "models" and the individual model name in the path
    
    print(f"Root path: {PATH_ROOT}") # debug

    # Define common paths
    PATH_COMMON_UTILS = PATH_ROOT / "common_utils"
    PATH_COMMON_CONFIGS = PATH_ROOT / "common_configs"

    print(f"Common utils path: {PATH_COMMON_UTILS}") # debug
    print(f"Common configs path: {PATH_COMMON_CONFIGS}") # debug

    # Define model-specific paths - more can be added as needed
    PATH_CONFIGS = PATH_MODEL / "configs"
    PATH_ARTIFACTS = PATH_MODEL / "artifacts"
    PATH_DATA = PATH_MODEL / "data"
    PATH_SRC = PATH_MODEL / "src"
    
    # This way ensure that the paths stay machine-agnostic compared to say PATH_MODEL / "src/utils" 
    PATH_UTILS = PATH_SRC / "utils"
    PATH_ARCHITECTURES = PATH_SRC / "architectures"


    paths_to_add = [PATH_COMMON_UTILS, PATH_ARTIFACTS, PATH_DATA, PATH_COMMON_CONFIGS, PATH_CONFIGS, PATH_UTILS, PATH_ARCHITECTURES]

    for path in paths_to_add:
        path_str = str(path)
        if path.exists() and path_str not in sys.path: # whith the current implementation, PATH_COMMON_UTILS is already in sys.path and will not be added (or printed) again
            print(f"Adding {path_str} to sys.path") # debug
            sys.path.insert(0, path_str)


def setup_data_paths(PATH) -> None:

    """
    Returns the raw, processed, and generated data paths for the specified model.

    Args:
    PATH (Path): The base path, typically the path of the script invoking this function (i.e., `Path(__file__)`).
    config (str): The model configuration file.
    
    """    

    PATH_MODEL = Path(*[i for i in PATH.parts[:PATH.parts.index("models")+2]]) # The +2 is to include the "models" and the individual model name in the path
    
    PATH_DATA = PATH_MODEL / "data"
    PATH_RAW = PATH_DATA / "raw"
    PATH_PROCCEDS = PATH_DATA / "processed"
    PATH_GENERATED = PATH_DATA / "generated"

    return PATH_RAW, PATH_PROCCEDS, PATH_GENERATED