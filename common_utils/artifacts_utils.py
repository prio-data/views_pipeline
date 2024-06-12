import os
from pathlib import Path

def get_artifact_files(PATH, run_type):
    """
    Retrieve artifact files from a directory that match the given run type and common extensions.

    Args:
        path (str): The directory path where model files are stored.
        run_type (str): The type of run (e.g., calibration, testing).

    Returns:
        list: List of matching model file paths.
    """
    # Define the common model file extensions - more can be added as needed
    common_extensions = ['.pt', '.pth', '.h5', '.hdf5', '.pkl', '.json', '.bst', '.txt', '.bin', '.cbm', '.onnx']

    # Retrieve files that start with run_type and end with any of the common extensions
    # artifact_files = [f for f in os.listdir(PATH) if f.startswith(f"{run_type}_model_") and any(f.endswith(ext) for ext in common_extensions)]
    
    # pathlib alternative
    artifact_files = [f for f in PATH.iterdir() if f.is_file() and f.stem.startswith(f"{run_type}_model_") and f.suffix in common_extensions]


    return artifact_files


def get_latest_model_artifact(PATH, run_type):
    """
    Retrieve the path (pathlib path object) latest model artifact for a given run type based on the modification time.

    Args:
        path (str): The model specifc directory path where artifacts are stored. 
        Where PATH_ARTIFACTS = setup_artifacts_paths(PATH) executed in the model specifc main.py script.
        and PATH = Path(__file__)
        
        run_type (str): The type of run (e.g., calibration, testing, forecasting).

    Returns:
        The path (pathlib path objsect) to the latest model artifact given the run type.

    Raises:
        FileNotFoundError: If no model artifacts are found for the given run type.
    """

    # List all model files for the given specific run_type with the expected filename pattern
    model_files = get_artifact_files(PATH, run_type) #[f for f in os.listdir(path) if f.startswith(f"{run_type}_model_") and f.endswith('.pt')]
    
    if not model_files:
        raise FileNotFoundError(f"No model artifacts found for run type '{run_type}' in path '{PATH}'")
    
    # Sort the files based on the timestamp embedded in the filename. With format %Y%m%d_%H%M%S For example, '20210831_123456.pt'
    model_files.sort(reverse=True)

    #print statements for debugging
    print(f"artifacts availible: {model_files}")
    print(f"artifact used: {model_files[0]}")
    
    # Return the latest model file
    #PATH_MODEL_ARTIFACT = os.path.join(path, model_files[0])

    # pathlib alternative
    PATH_MODEL_ARTIFACT = Path(PATH) / model_files[0]

    return PATH_MODEL_ARTIFACT

    # notes on stepshifted models:
    # There will be some thinking here in regards to how we store, denote (naming convention), and retrieve the model artifacts from stepshifted models.
    # It is not a big issue, but it is something to consider os we don't do something headless. 
    # A possible format could be: <run_type>_model_s<step>_<timestamp>.pt example: calibration_model_s00_20210831_123456.pt, calibration_model_s01_20210831_123456.pt, etc.
    # And the rest of the code maded in a way to handle this naming convention without any issues. Could be a simple fix.
    # Alternatively, we could store the model artifacts in a subfolder for each stepshifted model. This would make it easier to handle the artifacts, but it would also make it harder to retrieve the latest artifact for a given run type.
    # Lastly, the solution Xiaolong is working on might allow us the store multiple models (steps) in one artifact, which would make this whole discussion obsolete and be the best solution.

