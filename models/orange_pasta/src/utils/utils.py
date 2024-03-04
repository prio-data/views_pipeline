
from pathlib import Path

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


