from viewser import Queryset, Column

def generate():

    qs_treelag = (Queryset('fatalities002_pgm_conflict_treelag','priogrid_month')
                  
                .with_column(Column('ged_gte_1', from_loa='priogrid_month', from_column='ged_sb_best_sum_nokgi')
                    .transform.bool.gte(1)
                    )

                .with_column(Column('ln_ged_sb_dep', from_loa='priogrid_month', from_column='ged_sb_best_sum_nokgi')
                    .transform.missing.replace_na()
                    .transform.ops.ln()
                    )

                .with_column(Column('treelag_1_sb', from_loa='priogrid_month', from_column='ged_sb_best_sum_nokgi')
                    .transform.missing.replace_na()
                    .transform.spatial.treelag(0.7,1)
                    )

                .with_column(Column('treelag_1_ns', from_loa='priogrid_month', from_column='ged_ns_best_sum_nokgi')
                    .transform.missing.replace_na()
                    .transform.spatial.treelag(0.7,1)
                    )

                .with_column(Column('treelag_1_os', from_loa='priogrid_month', from_column='ged_os_best_sum_nokgi')
                    .transform.missing.replace_na()
                    .transform.spatial.treelag(0.7,1)
                    )

                .with_column(Column('treelag_2_sb', from_loa='priogrid_month', from_column='ged_sb_best_sum_nokgi')
                    .transform.missing.replace_na()
                    .transform.spatial.treelag(0.7,2)
                    )

                .with_column(Column('treelag_2_ns', from_loa='priogrid_month', from_column='ged_ns_best_sum_nokgi')
                    .transform.missing.replace_na()
                    .transform.spatial.treelag(0.7,2)
                    )

                .with_column(Column('treelag_2_os', from_loa='priogrid_month', from_column='ged_os_best_sum_nokgi')
                    .transform.missing.replace_na()
                    .transform.spatial.treelag(0.7,2)
                    )

                )
    return qs_treelag