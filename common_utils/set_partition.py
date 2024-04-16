from ingester3.ViewsMonth import ViewsMonth

def get_partitioner_dict(partion, step=36):

    """Returns the partitioner_dict for the given partion."""

    if partion == 'calibration':

        partitioner_dict = {"train":(121,396),"predict":(397,444)} # calib_partitioner_dict - (01/01/1990 - 12/31/2012) : (01/01/2013 - 31/12/2015)

    if partion == 'testing':

        partitioner_dict = {"train":(121,444),"predict":(445,492)} 

    if partion == 'forecasting':

        month_last =  ViewsMonth.now().id - 2 # minus 2 because the current month is not yet available. Verified but can be tested by chinging this and running the check_data notebook.

        partitioner_dict = {"train":(121, month_last),"predict":(month_last +1, month_last + 1 + step)}  # is it even meaningful to have a predict partition for forecasting? if not you can remove steps

    # print('partitioner_dict', partitioner_dict) 

    return partitioner_dict