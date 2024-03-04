import numpy as np
from viewser import Queryset, Column

def get_queryset():
    qs_baseline = (Queryset("fatalities003_pgm_baseline", "priogrid_month")

                    # target variable
                    .with_column(Column("ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                    .transform.missing.replace_na()
                                    # .transform.ops.ln()
                                    )

                    # timelag 0 of target variable
                    .with_column(Column("ln_ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    )

                    # Decay functions
                    # sb
                    .with_column(Column("decay_ged_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(1)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.missing.replace_na()
                                    )

                    .with_column(Column("decay_ged_sb_25", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(25)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.missing.replace_na()
                                    )
                    # os
                    .with_column(Column("decay_ged_os_1", from_table="ged2_pgm", from_column="ged_os_best_sum_nokgi")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(1)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.missing.replace_na()
                                    )

                    # Spatial lag
                    .with_column(Column("splag_1_1_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(1)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.spatial.lag(1, 1, 0, 0)
                                    .transform.missing.replace_na()
                                    )

                    # Spatial lag decay
                    .with_column(Column("splag_1_decay_ged_sb_1", from_table="ged2_pgm",
                                        from_column="ged_sb_best_sum_nokgi")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(1)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.spatial.lag(1, 1, 0, 0)
                                    .transform.missing.replace_na()
                                    )

                    # Log population as control
                    .with_column(Column("ln_pop_gpw_sum", from_table="priogrid_year", from_column="pop_gpw_sum")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.missing.replace_na()
                                    )

                    .with_theme("fatalities")
                    .describe("""Fatalities conflict history, cm level
        
                                Predicting ln(fatalities) using conflict predictors, ultrashort
        
                                """)
                    )
    return qs_baseline