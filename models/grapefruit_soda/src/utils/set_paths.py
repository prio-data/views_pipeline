import sys
from pathlib import Path


def set_paths():
       
    """
    Set the paths for various directories for the model, independently of (Mac, Linux) machine. 
    This structure assumes that this python script is located in root/models/example_model/src/utils.

    Next development: implement this from root. Not sure how to make the selected model path work there, though. 

    Returns:
        dict_values: A view object containing the values (paths) of the dictionary.
    """

    # Set the path to the root of the repo (for common configurations) and model (for model-specific configurations)
    root_path = Path(__file__).resolve().parents[4] #4 folders up from this file (i.e., utils > src > model > models > root)
    model_path = Path(__file__).resolve().parents[2] #2 folders up from this file (i.e., utils > src > model)

    # Define relative paths in a dictionary
    paths = {
        'common_utils': root_path / 'common_utils',
        'artifacts': model_path / 'src/artifacts',
        'configs': model_path / 'src/configs',
        'raw_data': model_path / 'src/data/raw',
        'processed_data': model_path / 'src/data/processed',
        'generated_data': model_path / 'src/data/generated',
        'dataloaders': model_path / 'src/dataloaders',
        'forecasting': model_path / 'src/forecasting',
        'offline_evaluation': model_path / 'src/offline_evaluation',
        'online_evaluation': model_path / 'src/online_evaluation',
        'training': model_path / 'src/training',
        'utils': model_path / 'src/utils',
        'visualization': model_path / 'src/visualization',
    }
    
    return root_path, model_path, paths.values()
    

def get_artifacts_path(partition_name):
    '''
    The artifacts are saved in src/artifacts/model_{partition_name}.pkl
    '''
    
    return Path(__file__).parent.parent.parent / "artifacts" / f"model_{partition_name}_partition.pkl"
    

def get_data_path(data_name):
    '''
    The data is saved in data/raw/raw.parquet
    '''

    return Path(__file__).parent.parent.parent / "data" / f"{data_name}" / f"{data_name}.parquet"