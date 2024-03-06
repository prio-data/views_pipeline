# Wildest Dream Model
## Overview
This folder contains code for Blank Space model, a machine learning model designed for predicting fatalities. 

The model utilizes Hurdle Model (XGBClassifier+XGBRegressor) for its predictions and is on pgm level of analysis.

## Repository Structure
```

blank_space/ # should follow the naming convention adjective_noun
|-- README.md
|-- requirements.txt
|
|-- configs/ # ...
|   |-- config_sweep.py # hyperparameters for test_sweep.py (WandB sweep)
|   |-- config_hyperparameters.py # hyperparameters train_model.py
|   |-- config_partitioner.py OR config_common # calibration, test, forecasting partitions
|   |-- config_queryset # queryset definition
|
|-- data/ # all input, processed, output data
|    |-- raw/ # Data directly from VIEiWSER
|    |-- processed/ # Data processed
|    |-- generated/ # Data generated - i.e. predictions/forecast
|
|-- artifacts/ # step-shift models will have 36 of each. pth or pkl. 
|   |-- model_metadata_dict.py # the standard meta data dict for models
|   |-- model_calib_partition.pth # for offline validation 
|   |-- model_train_partition.pth # for offline testing
|   |-- model_future_partition.pth # for online forecasting
|
|-- notebooks/
|
|-- reports/ # dissemination material - internal and external 
|   |-- plots/ # plots for papers, reports, newsletters, and slides
|   |-- figures/ # figures for papers, reports, newsletters, and slides 
|   |-- timelapse/ # plots to create timelapse and the timelapse
|   |-- papers/ # working papers, white papers, articles ect.
|   |-- slides/ # slides, presentation and similar. 
|
|-- src/ # all source code needed to train, test, and forecast
    |
    |-- dataloaders/ # scripts to get data from VIEWSER (and input drift detection)
    |   |-- get_data.py 
    |
    |-- utils/ # functions and classes 
    |   |-- utils.py # a general utils.py for all utils function
    |
    |-- visualization/ # scripts to create visualizations
    |   |-- visual.py
    |
    |-- training/
    |   |-- train_model.py
    |
    |-- offline_evaluation/ # aka offline quality assurance
    |   |-- evaluate_model.py # script to evaluate a train and saved model
    |   |-- evaluate_sweep.py # script to run a wandb sweep
    |
    |-- online_evaluation/
    |   |-- evaluate_forecast.py # continues performance check
    |
    |-- drift detection/ #monitor changes in model performance
    |   |-- drift_detection_output # check new forecasts
    |   |-- drift_detection_performance # check new performance
    |
    |-- forecasting/
        |-- generate_forecast.py #script to genereate true-future fc.
```

## Model Information
    Common Configuration: configs/config_common.py
    Hyperparameters: configs/config_hyperparameters.py
    Sweep Configuration: configs/config_sweep.py
    Queryset Configuration: configs/config_queryset.py

## Setup Instructions
Clone the repository.

Install dependencies.

## Usage
Modify configurations in configs/.

Run main.py.

```
python main.py
```

For every model, type in the terminal: a) Do sweep b) Do one run and pickle results.
Monitor progress and results using [Weights & Biases](https://wandb.ai/views_pipeline/orange_pasta).