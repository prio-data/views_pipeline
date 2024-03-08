def get_data_partitions():
    """
    Retrieves the data partitions for the model, i.e., validation, testing, and forecasting.

    Notes:
    - We have a data_partitions in common_utils, BUT for testing purposes I will keep this here to "override"

    """
    data_partitions = {
        'calib_partitioner_dict': {"train": (121, 396), "predict": (409, 456)},
        'test_partitioner_dict': {"train": (121, 456), "predict": (457, 504)},
        'future_partitioner_dict': {"train": (121, 504), "predict": (529, 529)},
        'FutureStart': 529, #Jan 24
    }
    return data_partitions
