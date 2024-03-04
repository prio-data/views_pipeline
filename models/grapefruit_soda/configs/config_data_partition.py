#this might move to common utils in root

from ingester3.ViewsMonth import ViewsMonth

def get_data_partitions():
    """
    Retrieves the data partitions for the model, i.e., validation, testing, and forecasting.

    TBD: move to common_utils (or not..?)

    """
    data_partitions = {
        'steps': [*range(1, 36 + 1, 1)],
        'calib_partitioner_dict': {"train": (121, 396), "predict": (409, 456)},
        'test_partitioner_dict': {"train": (121, 456), "predict": (457, 504)},
        'future_partitioner_dict': {"train": (121, 504), "predict": (529, 529)},
        'FutureStart': 508, #not sure about this
    }
    return data_partitions