import numpy as np
from viewser import Queryset, Column

def get_queryset():
    return_values = 'distances'
    n_nearest = 1
    power = 0.0

    qs_sptime_dist = (Queryset("fatalities003_pgm_conflict_sptime_dist", "priogrid_month")
                      # target variable
                      .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.ops.ln()
                                   )

                      # dichotomous version, primarily for downsampling....
                      .with_column(Column("ged_gte_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                   .transform.bool.gte(1)
                                   )

                      # continuous, sptime_dist, nu=1
                      .with_column(Column("sptime_dist_k1_ged_sb", from_table="ged2_pgm",
                                          from_column="ged_sb_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 1.0, power)
                                   )

                      .with_column(Column("sptime_dist_k1_ged_os", from_table="ged2_pgm",
                                          from_column="ged_os_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 1.0, power)
                                   )

                      .with_column(Column("sptime_dist_k1_ged_ns", from_table="ged2_pgm",
                                          from_column="ged_ns_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 1.0, power)
                                   )

                      .with_column(Column("sptime_dist_k1_ged_sb", from_table="ged2_pgm",
                                          from_column="ged_sb_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 10.0, power)
                                   )

                      .with_column(Column("sptime_dist_k1_ged_os", from_table="ged2_pgm",
                                          from_column="ged_os_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 10.0, power)
                                   )

                      .with_column(Column("sptime_dist_k1_ged_ns", from_table="ged2_pgm",
                                          from_column="ged_ns_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 10.0, power)
                                   )

                      .with_column(Column("sptime_dist_k1_ged_sb", from_table="ged2_pgm",
                                          from_column="ged_sb_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 0.01, power)
                                   )

                      .with_column(Column("sptime_dist_k1_ged_os", from_table="ged2_pgm",
                                          from_column="ged_os_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 0.01, power)
                                   )

                      .with_column(Column("sptime_dist_k1_ged_ns", from_table="ged2_pgm",
                                          from_column="ged_ns_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 0.01, power)
                                   )
                      )

    return qs_sptime_dist