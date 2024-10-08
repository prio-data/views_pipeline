from ingester3.ViewsMonth import ViewsMonth

def get_partitioner_dict(partition, step=36):

    """Returns the partitioner_dict for the given partition."""

    if partition == 'calibration':

        partitioner_dict = {"train":(121,396),"predict":(397,444)} # calib_partitioner_dict - (01/01/1990 - 12/31/2012) : (01/01/2013 - 31/12/2015)

    if partition == 'testing':

        partitioner_dict = {"train":(121,444),"predict":(445,492)} 

    if partition == 'forecasting':

        month_last = ViewsMonth.now().id - 2 # minus 2 because the current month is not yet available. Verified but can be tested by chinging this and running the check_data notebook.

        partitioner_dict = {"train":(121, month_last),"predict":(month_last +1, month_last + 1 + step)}  # is it even meaningful to have a predict partition for forecasting? if not you can remove steps

    # print('partitioner_dict', partitioner_dict) 

    return partitioner_dict

# currently these differ from the ones in the config_data_partitions.py file for the stepshifted models (see below). This needs to be sorted out asap.

#    data_partitions = {
#        'calib_partitioner_dict': {"train": (121, 396), "predict": (409, 456)},   # Does not make sense that the eval set starts at 409, it should start at 397, no?
#        'test_partitioner_dict': {"train": (121, 456), "predict": (457, 504)},
#        'future_partitioner_dict': {"train": (121, 504), "predict": (529, 529)}, # NO HARD CODIGN THE FUTURE START DATE
#        'FutureStart': 529, #Jan 24 # THIS SHOULD NOT BE HARD CODED!!!! Whatever the right partitions are for calibration and testing, the forecasting should be automatically infered from the current date.
#    }