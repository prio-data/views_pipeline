# Common utility functions

This folder contains reusable functions and classes to be used across multiple or all models (i.e., the entire pipeline). Model-specific utils can be found in the respective model source code (src).

Overview of utils scripts:
- `hurdle_model.py`: Class defining hurdle models, i.e., regression model which handles excessive zeros by fitting a two-part model and combining predictions
- `set_path.py`: Functions for machine-agnostic extracting and returning paths for root, models, data, artifacts.
- `utils_artifacts.py`: Functions to retrieve the path of model artifact
- `utils_cli_parser.py`: Fuctions for command-line-interface parser for model specific main.py scripts
- `utils_dataloaders.py`: Functions to create or load input data
- `utils_df_to_volume.py`: Functions to convert data frames and volumes (used in purple_alien)
- `utils_evaluation_metrics.py`: Class defining evaluation metrics
- `utils_model_outputs.py`: Class for storing and managing model outputs for evaluation and true forcasting

