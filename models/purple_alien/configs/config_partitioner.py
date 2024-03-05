from ingester3.ViewsMonth import ViewsMonth

def get_partitioner_dict(partion):

    """Returns the partitioner_dict for the given partion."""

    if partion == 'calibration':

        partitioner_dict = {"train":(121,396),"predict":(397,444)} # calib_partitioner_dict - (01/01/1990 - 12/31/2012) : (01/01/2013 - 31/12/2015)

    if partion == 'testing':

        partitioner_dict = {"train":(121,444),"predict":(445,492)} 

    if partion == 'forecasting':

        last_month =  ViewsMonth.now().id - 2

        partitioner_dict = {"train":(121, last_month),"predict":(last_month, last_month + 36)} # 36 should not be hard coded...  

    return partitioner_dict