# White Mustang Model
## Overview
This folder contains code for White Mustang model, an ensemble machine learning model designed for predicting fatalities. 

The model utilizes **latest** Lavender Haze (Hurdle Model LGBMClassifier+LGBMRegressor) and **latest** Blank Space (Hurdle Model LGBMClassifier+LGBMRegressor) for its predictions and is on pgm level of analysis.

The model uses log fatalities.

## Repository Structure
```
white_mustang/ # should follow the naming convention adjective_noun
|-- README.md
|-- requirements.txt
|
|-- artifacts/ # ensemble stepshifter models  
|   |-- model_metadata_dict.py # the standard meta data dict for models
|
|-- configs/ # ...
|   |-- config_deployment.py # configuration for deploying the model into different environments
|   |-- config_hyperparameters.py # hyperparameters for the model
|   |-- config_meta # metadata for the model (model architecture, name, target variable, and level of analysis)
|
|-- data/ # all input, processed, output data
|    |-- generated/ # Data generated - i.e. forecast/ evaluation
|    |-- processed/ # Data processed
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
    |-- dataloaders/ # scripts to get data from VIEWSER (and input drift detection)
    |
    |-- forecasting/
    |   |-- generate_forecast.py #script to genereate true-future fc.
    |
    |-- management/  
    |   |-- execute_model_runs.py # execute a single run
    |   |-- execute_model_tasks.py # execute various model-related tasks
    |
    |-- offline_evaluation/ # aka offline quality assurance
    |   |-- evaluate_ensemble.py # script to evaluate an ensemble model
    |
    |-- training/ 
    |   |-- train_ensemble.py # script to train an ensemble model
    |
    |-- utils/ # functions and classes 
    |   |-- utils_check.py # utils function to check if an ensemble is valid
    |   |-- utils_outputs.py # util functions to save outputs
    |   |-- utils_run.py # util functions for running models
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
python main.py -r your_run_type -a your_aggregation_mothod
```

Monitor progress and results using [Weights & Biases](https://wandb.ai/views_pipeline/white_snow).