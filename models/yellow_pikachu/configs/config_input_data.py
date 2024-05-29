import numpy as np
from viewser import Queryset, Column
def get_input_data():
    thetacrit_spatial = 0.7
    qs_treelag = (Queryset("fatalities003_pgm_conflict_treelag", "priogrid_month")
                  # target variable
                  .with_column(Column("ged_sb_dep", from_loa = "priogrid_month", from_column="ged_sb_best_sum_nokgi")
                               .transform.missing.replace_na()
                               # .transform.ops.ln()
                               )

                  # dichotomous version, primarily for downsampling....
                  .with_column(Column("ged_gte_1", from_loa = "priogrid_month", from_column="ged_sb_best_sum_nokgi")
                               .transform.bool.gte(1)
                               )

                  .with_column(Column("treelag_1_sb", from_loa = "priogrid_month", from_column="ged_sb_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.treelag(thetacrit_spatial, 1)
                               )

                  .with_column(Column("treelag_1_ns", from_loa = "priogrid_month", from_column="ged_ns_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.treelag(thetacrit_spatial, 1)
                               )

                  .with_column(Column("treelag_1_os", from_loa = "priogrid_month", from_column="ged_os_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.treelag(thetacrit_spatial, 1)
                               )

                  .with_column(Column("treelag_2_sb", from_loa = "priogrid_month", from_column="ged_sb_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.treelag(thetacrit_spatial, 2)
                               )

                  .with_column(Column("treelag_2_ns", from_loa = "priogrid_month", from_column="ged_ns_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.treelag(thetacrit_spatial, 2)
                               )

                  .with_column(Column("treelag_2_os", from_loa = "priogrid_month", from_column="ged_os_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.treelag(thetacrit_spatial, 2)
                               )
                  )
    return qs_treelag