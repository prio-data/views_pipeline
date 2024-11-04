from viewser import Queryset, Column

def generate():
    """
    Contains the configuration for the input data in the form of a viewser queryset. That is the data from viewser that is used to train the model.
    This configuration is "behavioral" so modifying it will affect the model's runtime behavior and integration into the deployment system.
    There is no guarantee that the model will work if the input data configuration is changed here without changing the model settings and algorithm accordingly.

    Returns:
    - queryset_base (Queryset): A queryset containing the base data for the model training.
    """
    
    # VIEWSER 6, Example configuration. Modify as needed.

    queryset = (Queryset('fatalities002_aquastat','country_month')
    .with_column(Column('ln_ged_sb_dep', from_loa='country_month', from_column='ged_sb_best_sum_nokgi')
        .transform.ops.ln()
        .transform.missing.fill()
        )

    .with_column(Column('ln_ged_sb', from_loa='country_month', from_column='ged_sb_best_sum_nokgi')
        .transform.ops.ln()
        .transform.missing.fill()
        )

    .with_column(Column('wdi_sp_pop_totl', from_loa='country_year', from_column='wdi_sp_pop_totl')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        .transform.missing.replace_na()
        )

    .with_column(Column('agr_withdrawal_pct_t48', from_loa='country_year', from_column='agr_withdrawal_pct')
        .transform.missing.fill()
        .transform.missing.replace_na()
        .transform.temporal.tlag(48)
        .transform.missing.fill()
        )

    .with_column(Column('dam_cap_pcap_t48', from_loa='country_year', from_column='dam_cap_pcap')
        .transform.missing.fill()
        .transform.missing.replace_na()
        .transform.temporal.tlag(48)
        .transform.missing.fill()
        )

    .with_column(Column('groundwater_export_t48', from_loa='country_year', from_column='groundwater_export')
        .transform.missing.fill()
        .transform.missing.replace_na()
        .transform.temporal.tlag(48)
        .transform.missing.fill()
        )

    .with_column(Column('fresh_withdrawal_pct_t48', from_loa='country_year', from_column='fresh_withdrawal_pct')
        .transform.missing.fill()
        .transform.missing.replace_na()
        .transform.temporal.tlag(48)
        .transform.missing.fill()
        )

    .with_column(Column('ind_efficiency_t48', from_loa='country_year', from_column='ind_efficiency')
        .transform.missing.fill()
        .transform.missing.replace_na()
        .transform.temporal.tlag(48)
        .transform.missing.fill()
        )

    .with_column(Column('irr_agr_efficiency_t48', from_loa='country_year', from_column='irr_agr_efficiency')
        .transform.missing.fill()
        .transform.missing.replace_na()
        .transform.temporal.tlag(48)
        .transform.missing.fill()
        )

    .with_column(Column('services_efficiency_t48', from_loa='country_year', from_column='services_efficiency')
        .transform.missing.fill()
        .transform.missing.replace_na()
        .transform.temporal.tlag(48)
        .transform.missing.fill()
        )

    .with_column(Column('general_efficiency_t48', from_loa='country_year', from_column='general_efficiency')
        .transform.missing.fill()
        .transform.missing.replace_na()
        .transform.temporal.tlag(48)
        .transform.missing.fill()
        )

    .with_column(Column('water_stress_t48', from_loa='country_year', from_column='water_stress')
        .transform.missing.fill()
        .transform.missing.replace_na()
        .transform.temporal.tlag(48)
        .transform.missing.fill()
        )

    .with_column(Column('renewable_internal_pcap_t48', from_loa='country_year', from_column='renewable_internal_pcap')
        .transform.missing.fill()
        .transform.missing.replace_na()
        .transform.temporal.tlag(48)
        .transform.missing.fill()
        )

    .with_column(Column('renewable_pcap_t48', from_loa='country_year', from_column='renewable_pcap')
        .transform.missing.fill()
        .transform.missing.replace_na()
        .transform.temporal.tlag(48)
        .transform.missing.fill()
        )

    .with_column(Column('decay_ged_sb_5', from_loa='country_month', from_column='ged_sb_best_sum_nokgi')
        .transform.missing.replace_na()
        .transform.bool.gte(5)
        .transform.temporal.time_since()
        .transform.temporal.decay(24)
        .transform.missing.replace_na()
        )

    .with_column(Column('decay_ged_os_5', from_loa='country_month', from_column='ged_os_best_sum_nokgi')
        .transform.missing.replace_na()
        .transform.bool.gte(5)
        .transform.temporal.time_since()
        .transform.temporal.decay(24)
        .transform.missing.replace_na()
        )

    .with_column(Column('splag_1_decay_ged_sb_5', from_loa='country_month', from_column='ged_sb_best_sum_nokgi')
        .transform.missing.replace_na()
        .transform.bool.gte(5)
        .transform.temporal.time_since()
        .transform.temporal.decay(24)
        .transform.spatial.countrylag(1,1,0,0)
        .transform.missing.replace_na()
        )

    .with_theme('fatalities002')
    .describe("""Predicting ln(fatalities), cm level
    
                             Queryset with baseline and aquastat features
    
                             """)
    )

    return queryset
