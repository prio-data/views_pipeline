from lightgbm import LGBMRegressor

common_config = {
    'level': 'pgm',
    'run_id': 'Fatalities002',
    'steps': [*range(1, 36 + 1, 1)],
    'calib_partitioner_dict': {"train": (121, 396), "predict": (397, 444)},
    'test_partitioner_dict': {"train": (121, 444), "predict": (445, 492)},
    'future_partitioner_dict': {"train": (121, 492), "predict": (493, 504)},
    'FutureStart': 508,
    'get_future': False,
    'force_retrain': False,
    'force_rewrite': True,
    'store_remote': False
}

model = {
            'modelname': 'fatalities002_pgm_baseline_Hackathon',
            'algorithm': LGBMRegressor(n_estimators=250),
            'depvar': "ln_ged_sb_dep",
            'queryset': 'fatalities002_pgm_baseline',
            'data_train': 'baseline',
            'level':            'pgm',
            'preprocessing': 'float_it'

}
