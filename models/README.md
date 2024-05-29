# Model Overview

| model | algorithm | queryset | 
| -------------------------------------------------- | ------ | ------ |
| [black_lodge](https://github.com/prio-data/views_pipeline/tree/main/models/black_lodge) | XGBRFRegressor | fatalities002_baseline |
| [blank_space](https://github.com/prio-data/views_pipeline/tree/main/models/blank_space) | HurdleRegression | fatalities003_pgm_natsoc |
| [electric_relaxation](https://github.com/prio-data/views_pipeline/tree/main/models/electric_relaxation) | RandomForestClassifier | escwa001_cflong |
| [lavender_haze](https://github.com/prio-data/views_pipeline/tree/main/models/lavender_haze) | HurdleRegression | fatalities003_pgm_broad |
| [orange_pasta](https://github.com/prio-data/views_pipeline/tree/main/models/orange_pasta) | LGBMRegressor | fatalities003_pgm_baseline |
| [purple_alien](https://github.com/prio-data/views_pipeline/tree/main/models/purple_alien) | HydraNet | simon_tests |
| [wildest_dream](https://github.com/prio-data/views_pipeline/tree/main/models/wildest_dream) | HurdleRegression | fatalities003_pgm_conflict_sptime_dist |
| [yellow_pikachu](https://github.com/prio-data/views_pipeline/tree/main/models/yellow_pikachu) | XGBRegressor | fatalities003_pgm_conflict_treelag |

# Model Definition
In the context of the VIEWS pipeline, a model should be understood as:

1) A specific instantiation of a machine learning algorithm, 
2) Trained using a predetermined and unique set of hyperparameters,
3) On a well-defined set of input features,
4) And targeting a specific outcome target.
5) In the case of stepshift models, a model is understood as **all** code and **all** artifacts necessary to generate a comprehensive 36 month forecast for the specified target.
6) Note that, two models, identical in all other aspects, will be deemed distinct if varying post-processing techniques are applied to their generated predictions. For instance, if one model's predictions undergo calibration or normalization while the other's do not.