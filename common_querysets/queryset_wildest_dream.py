from viewser import Queryset, Column

def generate():
    

    qs_sptime_dist = (Queryset('fatalities002_pgm_conflict_sptime_dist','priogrid_month')
                      
                     .with_column(Column('ged_gte_1', from_loa='priogrid_month', from_column='ged_sb_best_sum_nokgi')
                            .transform.bool.gte(1)
                            )

                     .with_column(Column('ln_ged_sb_dep', from_loa='priogrid_month', from_column='ged_sb_best_sum_nokgi')
                            .transform.missing.replace_na()
                            .transform.ops.ln()
                            )

                     .with_column(Column('sptime_dist_k1_ged_sb', from_loa='priogrid_month', from_column='ged_sb_best_sum_nokgi')
                            .transform.missing.replace_na()
                            .transform.spatial.sptime_dist("distances",1,1.0,0.0)
                            )

                     .with_column(Column('sptime_dist_k1_ged_os', from_loa='priogrid_month', from_column='ged_os_best_sum_nokgi')
                            .transform.missing.replace_na()
                            .transform.spatial.sptime_dist("distances",1,1.0,0.0)
                            )

                     .with_column(Column('sptime_dist_k1_ged_ns', from_loa='priogrid_month', from_column='ged_ns_best_sum_nokgi')
                            .transform.missing.replace_na()
                            .transform.spatial.sptime_dist("distances",1,1.0,0.0)
                            )

                     .with_column(Column('sptime_dist_k10_ged_sb', from_loa='priogrid_month', from_column='ged_sb_best_sum_nokgi')
                            .transform.missing.replace_na()
                            .transform.spatial.sptime_dist("distances",1,10.0,0.0)
                            )

                     .with_column(Column('sptime_dist_k10_ged_os', from_loa='priogrid_month', from_column='ged_os_best_sum_nokgi')
                            .transform.missing.replace_na()
                            .transform.spatial.sptime_dist("distances",1,10.0,0.0)
                            )

                     .with_column(Column('sptime_dist_k10_ged_ns', from_loa='priogrid_month', from_column='ged_ns_best_sum_nokgi')
                            .transform.missing.replace_na()
                            .transform.spatial.sptime_dist("distances",1,10.0,0.0)
                            )

                     .with_column(Column('sptime_dist_k001_ged_sb', from_loa='priogrid_month', from_column='ged_sb_best_sum_nokgi')
                            .transform.missing.replace_na()
                            .transform.spatial.sptime_dist("distances",1,0.01,0.0)
                            )

                     .with_column(Column('sptime_dist_k001_ged_os', from_loa='priogrid_month', from_column='ged_os_best_sum_nokgi')
                            .transform.missing.replace_na()
                            .transform.spatial.sptime_dist("distances",1,0.01,0.0)
                            )

                     .with_column(Column('sptime_dist_k001_ged_ns', from_loa='priogrid_month', from_column='ged_ns_best_sum_nokgi')
                            .transform.missing.replace_na()
                            .transform.spatial.sptime_dist("distances",1,0.01,0.0)
                            )

                     )

    return qs_sptime_dist