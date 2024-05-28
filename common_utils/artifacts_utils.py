import os

def get_latest_model_artifact(path, run_type):
    """
    Retrieve the latest model artifact for a given run type based on the modification time.

    Args:
        path (str): The model specifc directory path where artifacts are stored. 
        Where PATH_ARTIFACTS = setup_artifacts_paths(PATH) executed in the model specifc main.py script.
        and PATH = Path(__file__)
        
        run_type (str): The type of run (e.g., calibration, testing, forecasting).

    Returns:
        str: The path to the latest model artifact given the run type.

    Raises:
        FileNotFoundError: If no model artifacts are found for the given run type.
    """

    # List all model files for the given specific run_type with the expected filename pattern
    model_files = [f for f in os.listdir(path) if f.startswith(f"{run_type}_model_") and f.endswith('.pt')]
    
    if not model_files:
        raise FileNotFoundError(f"No model artifacts found for run type '{run_type}' in path '{path}'")
    
    # Sort the files based on the timestamp embedded in the filename. With format %Y%m%d_%H%M%S For example, '20210831_123456.pt'
    model_files.sort(reverse=True)

    #print statements for debugging
    print(model_files)
    print(model_files[0])
    
    # Return the latest model file
    return os.path.join(path, model_files[0])



