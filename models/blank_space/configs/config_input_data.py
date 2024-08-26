import numpy as np
from viewser import Queryset, Column

def get_input_data():
    
    qs_natsoc = (Queryset("fatalities003_pgm_natsoc", "priogrid_month")

                 # target variable
                 .with_column(Column("ln_ged_sb_dep", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                              .transform.missing.replace_na()
                              .transform.ops.ln()
                              )

                 # timelag 0 of target variable
                 .with_column(Column("ln_ged_sb", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                              .transform.ops.ln()
                              .transform.missing.fill()
                              )

                 # Decay functions
                 # sb
                 .with_column(Column("decay_ged_sb_1", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                              .transform.missing.replace_na()
                              .transform.bool.gte(1)
                              .transform.temporal.time_since()
                              .transform.temporal.decay(24)
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("decay_ged_sb_25", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                              .transform.missing.replace_na()
                              .transform.bool.gte(25)
                              .transform.temporal.time_since()
                              .transform.temporal.decay(24)
                              .transform.missing.replace_na()
                              )

                 # os
                 .with_column(Column("decay_ged_os_1", from_loa="priogrid_month", from_column="ged_os_best_sum_nokgi")
                              .transform.missing.replace_na()
                              .transform.bool.gte(1)
                              .transform.temporal.time_since()
                              .transform.temporal.decay(24)
                              .transform.missing.replace_na()
                              )

                 # Spatial lag
                 .with_column(Column("splag_1_1_sb_1", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                              .transform.missing.replace_na()
                              .transform.bool.gte(1)
                              .transform.temporal.time_since()
                              .transform.temporal.decay(24)
                              .transform.spatial.lag(1, 1, 0, 0)
                              .transform.missing.replace_na()
                              )

                 # Spatial lag decay
                 .with_column(Column("splag_1_decay_ged_sb_1", from_loa="priogrid_month",
                                     from_column="ged_sb_best_sum_nokgi")
                              .transform.missing.replace_na()
                              .transform.bool.gte(1)
                              .transform.temporal.time_since()
                              .transform.temporal.decay(24)
                              .transform.spatial.lag(1, 1, 0, 0)
                              .transform.missing.replace_na()
                              )

                 # Log population as control
                 .with_column(Column("ln_pop_gpw_sum", from_loa="priogrid_year", from_column="pop_gpw_sum")
                              .transform.ops.ln()
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 # from priogrid table:

                 .with_column(Column("ln_ttime_mean", from_loa="priogrid_year", from_column="ttime_mean")
                              .transform.ops.ln()
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("ln_gcp_mer", from_loa="priogrid_year", from_column="gcp_mer")
                              .transform.ops.ln()
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("imr_mean", from_loa="priogrid_year", from_column="imr_mean")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("ln_bdist3", from_loa="priogrid_year", from_column="bdist3")
                              .transform.ops.ln()
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("ln_capdist", from_loa="priogrid_year", from_column="capdist")
                              .transform.ops.ln()
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("mountains_mean", from_loa="priogrid_year", from_column="mountains_mean")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("dist_diamsec", from_loa="priogrid", from_column="dist_diamsec_s_wgs")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("dist_petroleum", from_loa="priogrid", from_column="dist_petroleum_s_wgs")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("agri_ih", from_loa="priogrid_year", from_column="agri_ih")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("barren_ih", from_loa="priogrid_year", from_column="barren_ih")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("forest_ih", from_loa="priogrid_year", from_column="forest_ih")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("pasture_ih", from_loa="priogrid_year", from_column="pasture_ih")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("savanna_ih", from_loa="priogrid_year", from_column="savanna_ih")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("shrub_ih", from_loa="priogrid_year", from_column="shrub_ih")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("urban_ih", from_loa="priogrid_year", from_column="urban_ih")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("greq_1_excluded", from_loa="priogrid_year", from_column="excluded")
                              .transform.bool.gte(1)
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_theme("fatalities")
                 .describe("""Fatalities natural and social geography, pgm level

                           Predicting ln(fatalities) using natural and social geography features

                           """)
                 )
                    
    return qs_natsoc