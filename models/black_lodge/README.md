# black_lodge
## Overview
This folder contains code for black_lodge model, a baseline random forest for predicting fatalities, also known as fatalities002_baseline_rf in the [documentation paper of fatalities002](https://viewsforecasting.org/wp-content/uploads/VIEWS_documentation_models_Fatalities002.pdf).

The model input data is the qs_baseline, and its algorithm is a random forest regressor with an XGBoost implementation (XGBRFRegressor). 

This is very simple model with only five data columns (each column representing one feature): The number of fatalities in the same country at $t-1$, three decay functions of time since there was at least five fatalities in a single month, for each of the UCDP conflict types -- state-based, one-sided, or non-state conflict -- and log population size (Hegre2020RP,Pettersson2021JPR).The features in the baseline are included in all the models described below. This ensures that all models in the ensemble provides at least moderately good predictions, while guaranteeing diversity in feature sets and modelling approaches.

## To-Dos
- [x] Take over model configs from [viewsforecasting](https://github.com/prio-data/viewsforecasting/blob/4dbc2cd2b6edb3169fc585f7dbb868b65fab0e2c/SystemUpdates/ModelDefinitions.py#L36)
- [x] Tidy config files 
- [x] Dataloader: Rewrite queryset for vimur
- [x] Training script
- [ ] Forecasting script
- [ ] Evaluation script
- [ ] Test management script
- [ ] Test main.py
- [ ] Log on wandb