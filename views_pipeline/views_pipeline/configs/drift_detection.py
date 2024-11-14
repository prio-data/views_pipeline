drift_detection_partition_dict={
    'calibration':{
            'global_missingness': {'threshold': 0.01},
            'time_missingness':   {'threshold': 0.05},
            'space_missingness':   {'threshold': 0.05},
            'feature_missingness': {'threshold': 0.05},
            'global_zeros': {'threshold': 0.99},
            'time_zeros':   {'threshold': 0.95},
            'feature_zeros': {'threshold': 0.95},
            'standard_partition_length': 30,
            'test_partition_length': 1

             },
    'testing':{
        'global_missingness': {'threshold': 0.01},
        'time_missingness': {'threshold': 0.05},
        'space_missingness': {'threshold': 0.05},
        'feature_missingness': {'threshold': 0.05},
        'global_zeros': {'threshold': 0.99},
        'time_zeros': {'threshold': 0.95},
        'feature_zeros': {'threshold': 0.95},
        'standard_partition_length': 30,
        'test_partition_length': 1

    },

    'forecasting':{
        'delta_completeness':   {'threshold': 0.01},
        'delta_zeroes': {'threshold': 0.01},
#        'ks_drift': {'threshold': 100},
        'extreme_values': {'threshold': 5.0},
        'standard_partition_length': 30,
        'test_partition_length': 1
    }
}