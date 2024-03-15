# electic_relaxation

## Overview
This folder contains code for the electric_relaxation model, as part of the VIEWS-ESCWA collaboration. The folder contains a series of modular scripts that were adapted from an initial Jupyter Notebook called ESCWA_model.

The model utilizes a Random Forest algorithm for its predictions and is on cm level of analysis. For more information, please check configs/config_model.py.

## How to run this model
Execute the entire model by running ´main.py´. This is the main orchestration script that calls on all other relevant scripts specified in source code (src). The model run will also be logged on Weights & Biases. If you are interested in specific aspects of the pipeline (data loading, model training/calibration, forecasting, evaluation), you can also execute the individual scripts under the folder src (source code). If you get errors when running main, this is also the best way to debug.

## How to configure this model
If you want to adjust model configurations, these can be found under configs/config_model.py. Keep in mind that changing significant aspects of the model (input data, algorithm) warrants the creation of a new model.
No configurations should be hard coded inside the source code. Instead, only use the configuration files to change parameters, as outlined below:

```
|-- configs/                                        # All model specific config files
|   |   |   |-- config_model.py                     # Contains model architecture, name, target variable, level of analysis and deployment status
|   |   |   |-- config_hyperparameters.py           # Specifies the finalized hyperparameters used for training the deployed model (W&B specific)
|   |   |   |-- config_sweep.py                     # Configurations for hyperparameter sweeps during experimentation phases (W&B specific)
|   |   |   |-- config_input_data.py                # Defines the features to be pulled from the views and used (the queryset).

```

## How to look at outputs of scripts
Once the model has been run locally, outputs will be generated. Please refer to the data and artifacts if you want to check these. Note that these should not be pushed to Git, but only stored locally. We have included pickle files for the models and parquet files for the data in the gitignore for this reason.

```
|   |   |-- artifacts/                              # Model artifacts. Step-shift models will have 36 of each. pth or pkl.
|   |   |   |-- evaluation_metrics.py               # A dictionary containing the evaluation metrics for all 36 steps found in the test partition
|   |   |   |-- model_calibration_partition.pkl     # Model object for offline evaluation, trained on train set of calibration partition
|   |   |   |-- model_future_partition.pkl          # Model object for online forecasting, trained on the forecasting partition
|   |   |
|   |   |-- data/                                   # All input, processed, output data -> might be out phased later to go directly from/to server
|   |   |    |-- raw/                               # Data directly from VIEWSER
|   |   |       |-- raw.parquet                     # Input data from VIEWSER Queryset
|   |   |    |-- processed/                         # Data processed
|   |   |    |-- generated/                         # Data generated - i.e., predictions/forecast
|   |   |       |-- calibration_predictions.parquet # Predictions for calibration partition
|   |   |       |-- future_point_predictions.parquet# Point Predictions for future partition
|   |   |       |-- future_predictions.parquet      # Predictions for future partition

```

## Further Development
These are the areas where further development is needed:
- Implementing another version of this model with the new stepshifter module Xiaolong has developed
- Further develop readme generator in utils (this readme was hand-written)
- Improve structure of evaluate_model (move repetitive code into utils?) 
- At some point, evaluations need to be monthly metrics. Simon created a [script to create a standard container for them in common_utils](https://github.com/prio-data/views_pipeline/blob/main/common_utils/utils_evaluation_metrics.py)
- Integrating input and output drift detection
- Hyperparameter tuning
- Figure out standardised path solution

## Deviations from Model Repo Structure
- For src/dataloaders and src/training, I did not create 3 different scripts for calibration, testing, and forecasting. For the moment, I would find that redundant
- Not using common_utils and common_configs, but model-specific ones -- this worked in the initial stage while I was figuring everything out for the first time
