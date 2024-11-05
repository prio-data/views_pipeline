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

    queryset = (Queryset('fatalities002_vdem_short','country_month')
        .with_column(Column('ln_ged_sb_dep', from_loa='country_month', from_column='ged_sb_best_sum_nokgi')
            .transform.ops.ln()
            .transform.missing.fill()
            )

        .with_column(Column('ln_ged_sb', from_loa='country_month', from_column='ged_sb_best_sum_nokgi')
            .transform.ops.ln()
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_delibdem', from_loa='country_year', from_column='vdem_v2x_delibdem')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_egaldem', from_loa='country_year', from_column='vdem_v2x_egaldem')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_libdem', from_loa='country_year', from_column='vdem_v2x_libdem')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_libdem_48', from_loa='country_year', from_column='vdem_v2x_libdem')
            .transform.missing.fill()
            .transform.temporal.tlag(60)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_partip', from_loa='country_year', from_column='vdem_v2x_partip')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_partipdem', from_loa='country_year', from_column='vdem_v2x_partipdem')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_accountability', from_loa='country_year', from_column='vdem_v2x_accountability')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_civlib', from_loa='country_year', from_column='vdem_v2x_civlib')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_clphy', from_loa='country_year', from_column='vdem_v2x_clphy')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_cspart', from_loa='country_year', from_column='vdem_v2x_cspart')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_divparctrl', from_loa='country_year', from_column='vdem_v2x_divparctrl')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_edcomp_thick', from_loa='country_year', from_column='vdem_v2x_edcomp_thick')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_egal', from_loa='country_year', from_column='vdem_v2x_egal')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_execorr', from_loa='country_year', from_column='vdem_v2x_execorr')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_frassoc_thick', from_loa='country_year', from_column='vdem_v2x_frassoc_thick')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_gencs', from_loa='country_year', from_column='vdem_v2x_gencs')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_gender', from_loa='country_year', from_column='vdem_v2x_gender')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_genpp', from_loa='country_year', from_column='vdem_v2x_genpp')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_horacc', from_loa='country_year', from_column='vdem_v2x_horacc')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_neopat', from_loa='country_year', from_column='vdem_v2x_neopat')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_pubcorr', from_loa='country_year', from_column='vdem_v2x_pubcorr')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_rule', from_loa='country_year', from_column='vdem_v2x_rule')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_veracc', from_loa='country_year', from_column='vdem_v2x_veracc')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_ex_military', from_loa='country_year', from_column='vdem_v2x_ex_military')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_ex_party', from_loa='country_year', from_column='vdem_v2x_ex_party')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_freexp', from_loa='country_year', from_column='vdem_v2x_freexp')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xcl_acjst', from_loa='country_year', from_column='vdem_v2xcl_acjst')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xcl_dmove', from_loa='country_year', from_column='vdem_v2xcl_dmove')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xcl_prpty', from_loa='country_year', from_column='vdem_v2xcl_prpty')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xcl_rol', from_loa='country_year', from_column='vdem_v2xcl_rol')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xcl_slave', from_loa='country_year', from_column='vdem_v2xcl_slave')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xdd_dd', from_loa='country_year', from_column='vdem_v2xdd_dd')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xdl_delib', from_loa='country_year', from_column='vdem_v2xdl_delib')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xeg_eqdr', from_loa='country_year', from_column='vdem_v2xeg_eqdr')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xeg_eqprotec', from_loa='country_year', from_column='vdem_v2xeg_eqprotec')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xel_frefair', from_loa='country_year', from_column='vdem_v2xel_frefair')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xel_regelec', from_loa='country_year', from_column='vdem_v2xel_regelec')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xme_altinf', from_loa='country_year', from_column='vdem_v2xme_altinf')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xnp_client', from_loa='country_year', from_column='vdem_v2xnp_client')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xnp_regcorr', from_loa='country_year', from_column='vdem_v2xnp_regcorr')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xpe_exlecon', from_loa='country_year', from_column='vdem_v2xpe_exlecon')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xpe_exlpol', from_loa='country_year', from_column='vdem_v2xpe_exlpol')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xpe_exlgeo', from_loa='country_year', from_column='vdem_v2xpe_exlgeo')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xpe_exlgender', from_loa='country_year', from_column='vdem_v2xpe_exlgender')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xpe_exlsocgr', from_loa='country_year', from_column='vdem_v2xpe_exlsocgr')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xps_party', from_loa='country_year', from_column='vdem_v2xps_party')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xcs_ccsi', from_loa='country_year', from_column='vdem_v2xcs_ccsi')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xnp_pres', from_loa='country_year', from_column='vdem_v2xnp_pres')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2xeg_eqaccess', from_loa='country_year', from_column='vdem_v2xeg_eqaccess')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2x_diagacc', from_loa='country_year', from_column='vdem_v2x_diagacc')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('vdem_v2clrgunev', from_loa='country_year', from_column='vdem_v2clrgunev')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('wdi_sm_pop_netm', from_loa='country_year', from_column='wdi_sm_pop_netm')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )

        .with_column(Column('wdi_sp_dyn_imrt_in', from_loa='country_year', from_column='wdi_sp_dyn_imrt_in')
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

        .with_column(Column('splag_vdem_v2x_libdem', from_loa='country_year', from_column='vdem_v2x_libdem')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.spatial.countrylag(1,1,0,0)
            .transform.missing.replace_na()
            )

        .with_column(Column('splag_vdem_v2xcl_dmove', from_loa='country_year', from_column='vdem_v2xcl_dmove')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.spatial.countrylag(1,1,0,0)
            .transform.missing.replace_na()
            )

        .with_column(Column('splag_vdem_v2x_accountability', from_loa='country_year', from_column='vdem_v2x_accountability')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.spatial.countrylag(1,1,0,0)
            .transform.missing.replace_na()
            )

        .with_column(Column('splag_vdem_v2xpe_exlsocgr', from_loa='country_year', from_column='vdem_v2xpe_exlsocgr')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.spatial.countrylag(1,1,0,0)
            .transform.missing.replace_na()
            )

        .with_column(Column('splag_vdem_v2xcl_rol', from_loa='country_year', from_column='vdem_v2xcl_rol')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.spatial.countrylag(1,1,0,0)
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
        
                                Queryset with baseline and short list of vdem features
        
                                """)
        )

    return queryset
