import numpy as np
from viewser import Queryset, Column

def get_input_data():
    """"
    Contains viewser queryset to fetch input data (queryset name, target variable, level of analysis, transformations, and theme).

    Returns:
    - qs_baseline (Queryset): Fatalities conflict history, cm level. Predicting ln(fatalities) using conflict predictors, ultrashort.

    Note:
    - Queryset taken from [viewsforecasting/Tools/cm_querysets.py](https://github.com/prio-data/viewsforecasting/blob/4dbc2cd2b6edb3169fc585f7dbb868b65fab0e2c/Tools/cm_querysets.py#L16)
    - Queryset will be used in src/dataloaders/get_data.py to fetch data.
    """

    qs_baseline = (Queryset("fatalities002_baseline", "country_month")

               # target variable
               .with_column(Column("ln_ged_sb_dep", from_loa="country_month", from_column="ged_sb_best_sum_nokgi")
                            .transform.ops.ln()
                            .transform.missing.fill()
                            )

               # timelag 0 of target variable
               .with_column(Column("ln_ged_sb", from_loa="country_month", from_column="ged_sb_best_sum_nokgi")
                            .transform.ops.ln()
                            .transform.missing.fill()
                            )
               # Decay functions
               # state-based (sb)
               .with_column(Column("decay_ged_sb_5", from_loa="country_month", from_column="ged_sb_best_sum_nokgi")
                            .transform.missing.replace_na()
                            .transform.bool.gte(5)
                            .transform.temporal.time_since()
                            .transform.temporal.decay(24)
                            .transform.missing.replace_na()
                            )
               # one-sided (os)
               .with_column(Column("decay_ged_os_5", from_loa="country_month", from_column="ged_os_best_sum_nokgi")
                            .transform.missing.replace_na()
                            .transform.bool.gte(5)
                            .transform.temporal.time_since()
                            .transform.temporal.decay(24)
                            .transform.missing.replace_na()
                            )
               # Spatial lag decay
               .with_column(Column("splag_1_decay_ged_sb_5", from_loa="country_month",
                                   from_column="ged_sb_best_sum_nokgi")
                            .transform.missing.replace_na()
                            .transform.bool.gte(5)
                            .transform.temporal.time_since()
                            .transform.temporal.decay(24)
                            .transform.spatial.countrylag(1, 1, 0, 0)
                            .transform.missing.replace_na()
                            )

               # From WDI

               .with_column(Column("wdi_sp_pop_totl", from_loa="country_year", from_column="wdi_sp_pop_totl")
                            .transform.missing.fill()
                            .transform.temporal.tlag(12)
                            .transform.missing.fill()
                            .transform.missing.replace_na()
                            )

               .with_theme("fatalities")
               .describe("""Fatalities conflict history, cm level

               Predicting ln(fatalities) using conflict predictors, ultrashort

                         """)
               )
    return qs_baseline