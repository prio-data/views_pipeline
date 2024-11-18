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

    queryset = (Queryset('fatalities003_faostat','country_month')
    .with_column(Column('ln_ged_sb_dep', from_loa='country_month', from_column='ged_sb_best_sum_nokgi')
        .transform.ops.ln()
        .transform.missing.fill()
        )

    .with_column(Column('ln_ged_sb', from_loa='country_month', from_column='ged_sb_best_sum_nokgi')
        .transform.ops.ln()
        .transform.missing.fill()
        )

    .with_column(Column('gleditsch_ward', from_loa='country', from_column='gwcode')
        .transform.missing.fill()
        .transform.missing.replace_na()
        )

    .with_column(Column('consumer_prices_food_indices', from_loa='country_month', from_column='consumer_prices_food_indices')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('consumer_prices_general_indices', from_loa='country_month', from_column='consumer_prices_general_indices')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('food_price_inflation', from_loa='country_month', from_column='food_price_inflation')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('avg_adequate_diet', from_loa='country_year', from_column='avg_adequate_diet')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('avg_animalprotein_pcap_day', from_loa='country_year', from_column='avg_animalprotein_pcap_day')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('avg_fprod_value', from_loa='country_year', from_column='avg_fprod_value')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('avg_protein_pcap_day', from_loa='country_year', from_column='avg_protein_pcap_day')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('gdp_pc_ppp', from_loa='country_year', from_column='gdp_pc_ppp')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('kcal_pcap_day', from_loa='country_year', from_column='kcal_pcap_day')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('kcal_pcap_day_cerotu', from_loa='country_year', from_column='kcal_pcap_day_cerotu')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pcap_fprod_var', from_loa='country_year', from_column='pcap_fprod_var')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pcap_fsupply_var', from_loa='country_year', from_column='pcap_fsupply_var')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pct_arable_land', from_loa='country_year', from_column='pct_arable_land')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pct_cereal_import', from_loa='country_year', from_column='pct_cereal_import')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pct_fimport_merch', from_loa='country_year', from_column='pct_fimport_merch')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pct_modsevere_finsecurity', from_loa='country_year', from_column='pct_modsevere_finsecurity')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pct_pop_basicdrink', from_loa='country_year', from_column='pct_pop_basicdrink')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pct_pop_basicsani', from_loa='country_year', from_column='pct_pop_basicsani')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pct_pop_safedrink', from_loa='country_year', from_column='pct_pop_safedrink')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pct_pop_safesani', from_loa='country_year', from_column='pct_pop_safesani')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pct_severe_finsecurity', from_loa='country_year', from_column='pct_severe_finsecurity')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pct_und5_overweight', from_loa='country_year', from_column='pct_und5_overweight')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pct_und5_stunted', from_loa='country_year', from_column='pct_und5_stunted')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pct_und5_wasting', from_loa='country_year', from_column='pct_und5_wasting')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pct_undernourished', from_loa='country_year', from_column='pct_undernourished')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pol_stability', from_loa='country_year', from_column='pol_stability')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pop_modsevere_finsecurity', from_loa='country_year', from_column='pop_modsevere_finsecurity')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pop_severe_finsecurity', from_loa='country_year', from_column='pop_severe_finsecurity')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('pop_undernourished', from_loa='country_year', from_column='pop_undernourished')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('prev_adult_obesity', from_loa='country_year', from_column='prev_adult_obesity')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('prev_infant_bfeed', from_loa='country_year', from_column='prev_infant_bfeed')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('prev_lowbweight', from_loa='country_year', from_column='prev_lowbweight')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('prev_repr_anemia', from_loa='country_year', from_column='prev_repr_anemia')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('rail_density', from_loa='country_year', from_column='rail_density')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        )

    .with_column(Column('wdi_sp_pop_totl', from_loa='country_year', from_column='wdi_sp_pop_totl')
        .transform.missing.fill()
        .transform.temporal.tlag(12)
        .transform.missing.fill()
        .transform.missing.replace_na()
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
    
                             Queryset with baseline and faostat features
    
                             """)
    )
    return queryset
