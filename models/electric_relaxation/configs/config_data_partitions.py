def get_data_partitions():
    """
    Retrieves the data partitions for the model, i.e., validation, testing, and forecasting.

    TBD: move to common_utils (or not..?)

    """
    data_partitions = {
        'calib_partitioner_dict': {"train": (121, 396), "predict": (409, 456)},
        'test_partitioner_dict': {"train": (121, 456), "predict": (457, 504)},
        'future_partitioner_dict': {"train": (121, 504), "predict": (529, 529)},
        'FutureStart': 529, #not sure about this -- Jan 24
    }
    return data_partitions

def get_data_partitions_new(partition):
    """
    new method, not implemented yet

    """
    if partition == 'calibration':

        data_partitions = {"train":(121,396),"predict":(409, 456)} 

    if partition == 'testing':

        data_partitions = {"train":(121, 456),"predict":(457, 504)} 

    if partition == 'forecasting':

        data_partitions = {"train":(121, 504),"predict":(529, 529)}   
    
    return data_partitions
