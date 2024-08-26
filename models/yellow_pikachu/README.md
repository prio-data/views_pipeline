# Yellow Pikachu Model
## Overview
This folder contains code for Yellow Pikachu model, a machine learning model designed for predicting fatalities. 

The model utilizes XGBoost for its predictions and is on pgm level of analysis.

The modle uses non-log fatalities

## Repository Structure
```

yellow_pikachu/ # should follow the naming convention adjective_noun
|-- README.md
|-- requirements.txt
|
|-- artifacts/ # ensemble stepshifter models  
|   |-- model_metadata_dict.py # the standard meta data dict for models
|
|-- configs/ # ...
|   |-- config_deployment.py # configuration for deploying the model into different environments
|   |-- config_hyperparameters.py # hyperparameters for the model
|   |-- config_input_data.py # defined queryset as the input data
|   |-- config_meta # metadata for the model (model architecture, name, target variable, and level of analysis)
|   |-- config_sweep # sweeping parameters for weights & biases
|
|-- data/ # all input, processed, output data
|    |-- generated/ # Data generated - i.e. forecast/ evaluation
|    |-- processed/ # Data processed
|    |-- raw/ # Data directly from VIEiWSER
|
|-- notebooks/
|
|-- reports/ # dissemination material - internal and external 
|   |-- figures/ # figures for papers, reports, newsletters, and slides 
|   |-- papers/ # working papers, white papers, articles ect.
|   |-- plots/ # plots for papers, reports, newsletters, and slides
|   |-- slides/ # slides, presentation and similar
|   |-- timelapse/ # plots to create timelapse and the timelapse
|
|-- src/ # all source code needed to train, test, and forecast
    |
    |-- dataloaders/ 
    |   |-- get_data.py # script to get data from VIEWSER (and input drift detection)
    |
    |-- forecasting/
    |   |-- generate_forecast.py # script to genereate true-future fc
    |
    |-- management/  
    |   |-- execute_model_runs.py # execute a single run
    |   |-- execute_model_tasks.py # execute various model-related tasks
    |
    |-- offline_evaluation/ # aka offline quality assurance
    |   |-- evaluate_model.py # script to evaluate a single model
    |   |-- evaluate_sweep.py # script to evaluate a model during sweeping
    |
    |-- online_evaluation/
    |
    |-- training/
    |   |-- train_model.py # script to train a single model
    |
    |-- utils/ # functions and classes 
    |   |-- utils.py # a general utils function
    |   |-- utils_wandb.py # a w&b specific utils function  
    | 
    |-- visualization/ # scripts to create visualizations
        |-- visual.py 


```

## Setup Instructions
Clone the repository.

Install dependencies.

## Usage
Modify configurations in configs/.

Run main.py.

```
python main.py -r calibration -t -e
```

Monitor progress and results using [Weights & Biases](https://wandb.ai/views_pipeline/yellow_pikachu).