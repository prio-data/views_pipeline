import numpy as np
from viewser import Queryset, Column

def get_input_data():
    
    thetacrit_spatial = 0.7
    return_values = 'distances'
    n_nearest = 1
    power = 0.0

    qs_broad = (Queryset("fatalities003_pgm_broad", "priogrid_month")

                # target variable
                .with_column(Column("ged_sb_dep", from_loa = "priogrid_month", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             # .transform.ops.ln()
                             )

                # timelags 0 of conflict variables, ged_best versions

                .with_column(Column("ged_sb", from_loa = "priogrid_month", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                .with_column(Column("ged_os", from_loa = "priogrid_month", from_column="ged_os_best_sum_nokgi")
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                .with_column(Column("ged_ns", from_loa = "priogrid_month", from_column="ged_ns_best_sum_nokgi")
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                # Spatial lag
                .with_column(Column("splag_1_1_sb_1", from_loa = "priogrid_month", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(24)
                             .transform.spatial.lag(1, 1, 0, 0)
                             .transform.missing.replace_na()
                             )

                # Decay functions
                # sb
                .with_column(Column("decay_ged_sb_5", from_loa = "priogrid_month", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.bool.gte(5)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(12)
                             .transform.missing.replace_na()
                             )
                # os
                .with_column(Column("decay_ged_os_5", from_loa = "priogrid_month", from_column="ged_os_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.bool.gte(5)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(12)
                             .transform.missing.replace_na()
                             )

                # ns
                .with_column(Column("decay_ged_ns_5", from_loa = "priogrid_month", from_column="ged_ns_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.bool.gte(5)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(12)
                             .transform.missing.replace_na()
                             )

                # Trees

                .with_column(Column("treelag_1_sb", from_loa = "priogrid_month", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.spatial.treelag(thetacrit_spatial, 1)
                             )

                .with_column(Column("treelag_2_sb", from_loa = "priogrid_month", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.spatial.treelag(thetacrit_spatial, 2)
                             )
                # sptime

                # continuous, sptime_dist, nu=1
                .with_column(Column("sptime_dist_k1_ged_sb", from_loa = "priogrid_month", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.spatial.sptime_dist(return_values, n_nearest, 1.0, power)
                             )

                .with_column(Column("sptime_dist_k1_ged_sb", from_loa = "priogrid_month", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.spatial.sptime_dist(return_values, n_nearest, 10.0, power)
                             )

                .with_column(Column("sptime_dist_k1_ged_sb", from_loa = "priogrid_month", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.spatial.sptime_dist(return_values, n_nearest, 0.01, power)
                             )

                # From natsoc
                .with_column(Column("ln_ttime_mean", from_loa = "priogrid_year", from_column="ttime_mean")
                             .transform.ops.ln()
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                .with_column(Column("ln_bdist3", from_loa = "priogrid_year", from_column="bdist3")
                             .transform.ops.ln()
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                .with_column(Column("ln_capdist", from_loa = "priogrid_year", from_column="capdist")
                             .transform.ops.ln()
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                .with_column(Column("dist_diamsec", from_loa="priogrid", from_column="dist_diamsec_s_wgs")
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                .with_column(Column("imr_mean", from_loa = "priogrid_year", from_column="imr_mean")
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                # From drought
                .with_column(Column("tlag1_dr_mod_gs", from_loa="priogrid",
                                    from_column="tlag1_dr_mod_gs")
                             .transform.missing.replace_na(0)
                             )

                .with_column(Column("spei1_gs_prev10_anom", from_loa="priogrid",
                                    from_column="spei1_gs_prev10_anom")
                             .transform.missing.replace_na(0)
                             )

                .with_column(Column("tlag_12_crop_sum", from_loa="priogrid",
                                    from_column="tlag_12_crop_sum")
                             .transform.missing.replace_na(0)
                             )

                .with_column(Column("spei1gsy_lowermedian_count", from_loa="priogrid",
                                    from_column="spei1gsy_lowermedian_count")
                             .transform.missing.replace_na(0)
                             )

                # Log population as control
                .with_column(Column("ln_pop_gpw_sum", from_loa = "priogrid_year", from_column="pop_gpw_sum")
                             .transform.ops.ln()
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                .with_theme("fatalities")
                .describe("""fatalities broad model, pgm level

                          Predicting ln(ged_best_sb), broad model

                          """)
                )
                    
    return qs_broad