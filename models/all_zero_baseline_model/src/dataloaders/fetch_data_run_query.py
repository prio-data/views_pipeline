from ..dataloaders.queryset import get_querysets
from pathlib import Path


def fetch_data():
    data = get_querysets()
    data.to_parquet(
        f"{Path(__file__).parent.parent.parent}/data/processed/processed.parquet")
    return data
