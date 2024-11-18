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

    queryset = (Queryset('fatalities003_wdi_short','country_month')
        .with_column(Column('ln_ged_sb_dep', from_loa='country_month', from_column='ged_sb_best_sum_nokgi')
            .transform.ops.ln()
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('ln_ged_sb', from_loa='country_month', from_column='ged_sb_best_sum_nokgi')
            .transform.ops.ln()
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_ag_lnd_frst_k2', from_loa='country_year', from_column='wdi_ag_lnd_frst_k2')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_dt_oda_odat_pc_zs', from_loa='country_year', from_column='wdi_dt_oda_odat_pc_zs')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_ms_mil_xpnd_gd_zs', from_loa='country_year', from_column='wdi_ms_mil_xpnd_gd_zs')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_ms_mil_xpnd_zs', from_loa='country_year', from_column='wdi_ms_mil_xpnd_zs')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_nv_agr_totl_kd', from_loa='country_year', from_column='wdi_nv_agr_totl_kd')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_nv_agr_totl_kn', from_loa='country_year', from_column='wdi_nv_agr_totl_kn')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_ny_gdp_pcap_kd', from_loa='country_year', from_column='wdi_ny_gdp_pcap_kd')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_sp_dyn_le00_in', from_loa='country_year', from_column='wdi_sp_dyn_le00_in')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_se_enr_prim_fm_zs', from_loa='country_year', from_column='wdi_se_enr_prim_fm_zs')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_se_enr_prsc_fm_zs', from_loa='country_year', from_column='wdi_se_enr_prsc_fm_zs')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_se_prm_nenr', from_loa='country_year', from_column='wdi_se_prm_nenr')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_sh_sta_maln_zs', from_loa='country_year', from_column='wdi_sh_sta_maln_zs')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_sh_sta_stnt_zs', from_loa='country_year', from_column='wdi_sh_sta_stnt_zs')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_sl_tlf_totl_fe_zs', from_loa='country_year', from_column='wdi_sl_tlf_totl_fe_zs')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_sm_pop_refg_or', from_loa='country_year', from_column='wdi_sm_pop_refg_or')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_sm_pop_netm', from_loa='country_year', from_column='wdi_sm_pop_netm')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_sm_pop_totl_zs', from_loa='country_year', from_column='wdi_sm_pop_totl_zs')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_sp_dyn_imrt_in', from_loa='country_year', from_column='wdi_sp_dyn_imrt_in')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_sh_dyn_mort_fe', from_loa='country_year', from_column='wdi_sh_dyn_mort_fe')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_sp_pop_14_fe_zs', from_loa='country_year', from_column='wdi_sp_pop_0014_fe_zs')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_sp_pop_1564_fe_zs', from_loa='country_year', from_column='wdi_sp_pop_1564_fe_zs')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_sp_pop_65up_fe_zs', from_loa='country_year', from_column='wdi_sp_pop_65up_fe_zs')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_sp_pop_grow', from_loa='country_year', from_column='wdi_sp_pop_grow')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_sp_urb_totl_in_zs', from_loa='country_year', from_column='wdi_sp_urb_totl_in_zs')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('wdi_sp_pop_totl', from_loa='country_year', from_column='wdi_sp_pop_totl')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            .transform.missing.replace_na()
            )

        .with_column(Column('splag_wdi_sl_tlf_totl_fe_zs', from_loa='country_year', from_column='wdi_sl_tlf_totl_fe_zs')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.spatial.countrylag(1,1,0,0)
            .transform.missing.replace_na()
            )

        .with_column(Column('splag_wdi_sm_pop_refg_or', from_loa='country_year', from_column='wdi_sm_pop_refg_or')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.spatial.countrylag(1,1,0,0)
            .transform.missing.replace_na()
            )

        .with_column(Column('splag_wdi_sm_pop_netm', from_loa='country_year', from_column='wdi_sm_pop_netm')
            .transform.missing.fill()
            .transform.temporal.tlag(12)
            .transform.spatial.countrylag(1,1,0,0)
            .transform.missing.replace_na()
            )

        .with_column(Column('splag_wdi_ag_lnd_frst_k2', from_loa='country_year', from_column='wdi_ag_lnd_frst_k2')
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
        
                                Queryset with baseline and short list of wdi features
        
                                """)
        )

    return queryset
