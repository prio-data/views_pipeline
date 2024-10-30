from utils import utils_script_gen
from pathlib import Path


def generate(script_dir: Path, model_name: str) -> bool:
    """
    Generates a Python script that defines the `generate` function for configuring input data for model training
    using the viewser library.

    Args:
        script_dir (Path): The directory where the generated deployment configuration script will be saved.
                           This should be a valid writable path.
        model_name (str): The name of the model for which the input data configuration is being generated.
                          This name is used to identify the relevant data in the viewser queryset.

    Returns:
        bool: True if the script was successfully generated and saved, False otherwise.
    """
    code = f"""from viewser import Queryset, Column

def generate():
    \"""
    Contains the configuration for the input data in the form of a viewser queryset. That is the data from viewser that is used to train the model.
    This configuration is "behavioral" so modifying it will affect the model's runtime behavior and integration into the deployment system.
    There is no guarantee that the model will work if the input data configuration is changed here without changing the model settings and algorithm accordingly.

    Returns:
    - queryset_base (Queryset): A queryset containing the base data for the model training.
    \"""
    
    # VIEWSER 6, Example configuration. Modify as needed.

    queryset_base = (Queryset("{model_name}", "priogrid_month")
        # Create a new column 'ln_sb_best' using data from 'priogrid_month' and 'ged_sb_best_count_nokgi' column
        # Apply logarithmic transformation, handle missing values by replacing them with NA
        .with_column(Column("ln_sb_best", from_loa="priogrid_month", from_column="ged_sb_best_count_nokgi")
            .transform.ops.ln().transform.missing.replace_na())
        
        # Create a new column 'ln_ns_best' using data from 'priogrid_month' and 'ged_ns_best_count_nokgi' column
        # Apply logarithmic transformation, handle missing values by replacing them with NA
        .with_column(Column("ln_ns_best", from_loa="priogrid_month", from_column="ged_ns_best_count_nokgi")
            .transform.ops.ln().transform.missing.replace_na())
        
        # Create a new column 'ln_os_best' using data from 'priogrid_month' and 'ged_os_best_count_nokgi' column
        # Apply logarithmic transformation, handle missing values by replacing them with NA
        .with_column(Column("ln_os_best", from_loa="priogrid_month", from_column="ged_os_best_count_nokgi")
            .transform.ops.ln().transform.missing.replace_na())
        
        # Create columns for month and year_id
        .with_column(Column("month", from_loa="month", from_column="month"))
        .with_column(Column("year_id", from_loa="country_year", from_column="year_id"))
        
        # Create columns for country_id, col, and row
        .with_column(Column("c_id", from_loa="country_year", from_column="country_id"))
        .with_column(Column("col", from_loa="priogrid", from_column="col"))
        .with_column(Column("row", from_loa="priogrid", from_column="row"))
    )

    return queryset_base
"""
    return utils_script_gen.save_script(script_dir, code)
