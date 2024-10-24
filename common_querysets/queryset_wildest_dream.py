from viewser import Queryset, Column

def generate():
    return_values = 'distances'
    n_nearest = 1
    power = 0.0

    qs_sptime_dist = (Queryset("fatalities003_pgm_conflict_sptime_dist", "priogrid_month")
                      # target variable
                      .with_column(Column("ln_ged_sb_dep", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.ops.ln()
                                   )

                      # dichotomous version, primarily for downsampling....
                      .with_column(Column("ged_gte_1", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                                   .transform.bool.gte(1)
                                   )

                      # continuous, sptime_dist, nu=1
                      .with_column(Column("sptime_dist_k1_1_ged_sb", from_loa="priogrid_month",
                                          from_column="ged_sb_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 1.0, power)
                                   )

                      .with_column(Column("sptime_dist_k1_1_ged_os", from_loa="priogrid_month",
                                          from_column="ged_os_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 1.0, power)
                                   )

                      .with_column(Column("sptime_dist_k1_1_ged_ns", from_loa="priogrid_month",
                                          from_column="ged_ns_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 1.0, power)
                                   )

                      .with_column(Column("sptime_dist_k1_2_ged_sb", from_loa="priogrid_month",
                                          from_column="ged_sb_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 10.0, power)
                                   )

                      .with_column(Column("sptime_dist_k1_2_ged_os", from_loa="priogrid_month",
                                          from_column="ged_os_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 10.0, power)
                                   )

                      .with_column(Column("sptime_dist_k1_2_ged_ns", from_loa="priogrid_month",
                                          from_column="ged_ns_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 10.0, power)
                                   )

                      .with_column(Column("sptime_dist_k1_3_ged_sb", from_loa="priogrid_month",
                                          from_column="ged_sb_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 0.01, power)
                                   )

                      .with_column(Column("sptime_dist_k1_3_ged_os", from_loa="priogrid_month",
                                          from_column="ged_os_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 0.01, power)
                                   )

                      .with_column(Column("sptime_dist_k1_3_ged_ns", from_loa="priogrid_month",
                                          from_column="ged_ns_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 0.01, power)
                                   )
                      )

    return qs_sptime_dist