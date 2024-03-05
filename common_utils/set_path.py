from pathlib import Path

def get_artifacts_path(model_name, partition_name):
    '''
    The artifacts are saved in src/artifacts/model_{partition_name}.pkl
    '''
    
    return Path(__file__).parent.parent / f"models/{model_name}/artifacts/model_{partition_name}_partition.pkl"
    

def get_data_path(model_name, data_name):
    '''
    The data is saved in data/raw/raw.parquet
    '''

    return Path(__file__).parent.parent / f"models/{model_name}/data/{data_name}/{data_name}.parquet"


