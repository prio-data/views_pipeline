# Green Goblin Model
## Overview
This folder contains code for Green Goblin model, a machine learning model designed for predicting fatalities. The model was implemented during the VIEWS 2024 Cabin Hackathon. The model utilizes XYZ algorithm for its predictions.

## Repository Structure
    models/orange_pasta/
        configs/: Configuration files for the model.
        data/: Data used for training and evaluation.
        src/: Source code for data loading, model training, forecasting, and evaluation.
        tests/: Unit tests for the model.
        .gitignore: Specifies files and directories to be ignored by Git.
        README.md: Overview and use instructions.

## Model Information
    Common Configuration: configs/config_common.py
    Hyperparameters: configs/config_hyperparameters.py
    Sweep Configuration: configs/config_sweep.py

## Setup Instructions
    Clone the repository.
    Install dependencies (pip install -r requirements.txt).

## Usage
    Ensure data is in models/green_goblin/data/raw/.
    Modify configurations in configs/.
    Run main.py.
    ```bash
    python main.py
    ```
    Monitor progress and results using Weights & Biases.