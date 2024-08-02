from datetime import datetime

def print_dataset_dates(df, continue_on_missing=True):

    """
    Print summary information about the minimum and maximum dates in a dataset.

    This function prints the following information for a given DataFrame:
        - Minimum and maximum `month_id` (The unique identifier for the month)
        - Minimum and maximum `year_id` (which is just the year)
        - The formatted date of the first month of the first year (The month name and year)
        - The formatted date of the last month of the last year (The month name and year)

    If the required columns (`month_id`, `month`, `year_id`) are missing, the function will either:
        - Print a warning and skip processing if `continue_on_missing` is set to `True`.
        - Raise a `ValueError` if `continue_on_missing` is set to `False`.

    Parameters:
    ----------
    df : pandas.DataFrame
        The DataFrame containing the dataset. It must include the following columns:
        - 'month_id': Integer representing the unique month id.
        - 'month': Integer representing the month (1-12), for formatting the date.
        - 'year_id': Integer representing the year.

    continue_on_missing : bool, optional
        If set to `True`, the function will continue processing and print a warning if required columns are missing.
        If set to `False`, the function will raise a `ValueError` if required columns are missing. 
        The default is `True`.

    Returns:
    -------
    None
        This function does not return any value. It prints the results directly to the console.

    Raises:
    ------
    ValueError
        If `continue_on_missing` is `False` and one or more required columns are missing from the DataFrame.
    
    Examples:
    --------
    >>> print_dataset_dates(views_df_c)
    >>> print_dataset_dates(views_df_t, continue_on_missing=False)
    """

    print("\n" + "-"*40 + "\n")

    print("Summary of the dates from the downloaded dataset:")

    columns_needed = ['month_id', "month", 'year_id']
    
    # Check if the needed columns are present in the df
    missing_cols = [col for col in columns_needed if col not in df.columns]
    if missing_cols:
        print(f"Missing columns: {missing_cols}. Cannot print the start and end dates of the dataset.")
        
        if continue_on_missing:
            print("!!! Continuing with the rest of the operation, but proceed with caution !!!")
        else:
            raise ValueError(f"Dataset is missing required columns: {missing_cols}")

        return

    # Print min/max month_id and year_id
    print(f"Minimum month_id: {df['month_id'].min()}")
    print(f"Maximum month_id: {df['month_id'].max()}")
    print(f"Minimum year: {df['year_id'].min()}")
    print(f"Maximum year: {df['year_id'].max()}")

    # Get the first month and year
    first_year = df['year_id'].min()
    first_month = df[df['year_id'] == first_year]['month'].min()
    first_date = datetime(first_year, first_month, 1).strftime("%B %Y")
    print(f"First date (first month of the first year): {first_date}")

    # Get the last month and year
    last_year = df['year_id'].max()
    last_month = df[df['year_id'] == last_year]['month'].max()
    last_date = datetime(last_year, last_month, 1).strftime("%B %Y")
    print(f"Last date (last month of the last year): {last_date}")
    print("\n" + "-"*40 + "\n")

    return
