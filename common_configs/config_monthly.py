def get_monthly_config():
    """
    Contains the meta data for the executing the monthly operational run of the pipeline.

    Adopted from viewsforecasting/MonthlyUpdates/cm_futurepredictions.ipynb

    Returns:
    - meta_config (dict): A dictionary containing pipeline meta configuration.
    """
    monthly_config = {
        "dev_id": "Fatalities002",
        "run_id": "dev_id", 
        "prod_id": "2024_06_t01", 
        "RunGeneticAlgo": False,
        "level": "pgm", #or cm
        "get_future": False
    }
    return monthly_config 