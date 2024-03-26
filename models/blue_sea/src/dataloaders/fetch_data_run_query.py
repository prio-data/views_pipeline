from ..dataloaders.queryset import get_querysets
from pathlib import Path


def fetch_data():
    '''
    This function is a wrapper for processing raw data from the database.
    
    Returns:
    data: The data fetched from the querysets.
    
    '''
    data = get_querysets()
    data.to_parquet(
        f"{Path(__file__).parent.parent.parent}/data/processed/processed.parquet")
    return data
