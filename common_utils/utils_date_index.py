from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate_date_from_index(target_index, start_index = 121, start_date = '01.1990'):
    """
    Calculates the month-year date for a given target index based on the start index and start date.

    Parameters:
    start_index (int): The index corresponding to the start date.
    start_date (str): The start date in 'MM.YYYY' format.
    target_index (int): The index for which the month-year date is required.

    Returns:
    str: The calculated month-year date corresponding to the target_index in 'MM.YYYY' format.
    """
    # Convert the start date to a datetime object
    base_date = datetime.strptime(start_date, '%m.%Y')
    
    # Calculate the difference in indices
    month_difference = target_index - start_index
    
    # Calculate the target date by adding the month difference
    target_date = base_date + relativedelta(months=month_difference)
    
    return target_date.strftime('%m.%Y')