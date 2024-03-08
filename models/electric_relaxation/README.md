# electic_relaxation

## Overview
This folder contains code for the electric_relaxation model, as part of the VIEWS-ESCWA collaboration. The folder contains a series of modular scripts that were adapted from an initial Jupyter Notebook called ESCWA_model.

The model utilizes a Random Forest algorith, for its predictions and is on cm level of analysis. For more information, please check configs/config_model.py.

## How to run this model
Execute the model by running ´main.py´. If you want to adjust model configurations, these can be found under configs. No configurations should be hard coded.

If you are interested in specific aspects of the pipeline (data loading, model training/calibration, forecasting, evaluation), you can also execute the individual scripts under the folder src (source code). If you get errors when running main, this is also the best way to debug.

## Further Development
These are the areas where further development is needed:
- Implementing another version of this model with the new stepshifter module Xiaolong has developed
- Further develop readme generator in utils (this readme was hand-written)
- Improve structure of evaluate_model (move repetitive code into utils?)
- Integrating input and output drift detection
- Hyperparameter tuning
- Figure out standardised path solution

## Deviations from Model Repo Structure
- For src/dataloaders and src/training, I did not create 3 different scripts for calibration, testing, and forecasting. For the moment, I would find that redundant
- Not using common_utils and common_configs, but model-specific ones -- this worked in the initial stage while I was figuring everything out for the first time
