import numpy as np
from viewser import Queryset, Column

from pathlib import Path


def get_querysets():
    '''
    This function fetches the data from database and saves it to a parquet file.
    
    Returns:
    data: The data fetched from the querysets.
    
    '''

    allzero_query = (Queryset("pgm_allzero", "priogrid_month")

                     # target variable
                     .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                  .transform.missing.fill()))

    data = allzero_query.publish().fetch()

    # save to parquet using pathlib
    data.to_parquet(
        f"{Path(__file__).parent.parent.parent}/data/raw/raw.parquet")
    # data["ln_ged_sb_dep"] = 0
    return data
