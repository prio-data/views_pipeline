# Documentation of Models in VIEWS Pipeline

## Definition
In the context of the VIEWS pipeline, a model should be understood as:

1) A specific instantiation of a machine learning algorithm, 
2) Trained using a predetermined and unique set of hyperparameters,
3) On a well-defined set of input features,
4) And targeting a specific outcome target.
5) In the case of stepshift models, a model is understood as **all** code and **all** artifacts necessary to generate a comprehensive 36 month forecast for the specified target.
6) Note that, two models, identical in all other aspects, will be deemed distinct if varying post-processing techniques are applied to their generated predictions. For instance, if one model's predictions undergo calibration or normalization while the other's do not.

## Obligations
In the context of the VIEWS pipeline, a model directory needs to conform to a certain structure, and a number of specific scripts must exist. In essences:

- The structure must adhere to the standard structure as defined in the root README.md. This structure can quickly be replicated by running meta_tools/make_new_model_dir.

- To generate monthly forecasts, all model directories must as a minimum, at the appropriate locations, contain the following scripts:
    - configs/config_hyperparameters.py
    - src/artifacts/metadata_dict.py
    - src/dataloaders/get_latest_data.py
    - src/training/train_pipeline_model.py
    - src/online_evaluation/evaluate_forecast.py
    - src/drift_detection/drift_detection_input.py
    - src/drift_detection/drift_detection_output.py 
    - src/drift_detection/drift_detection_performance.py 
    - src/forecasting/generate_forecast.py 

- Additionally, to adhere to the conventional framework for model experimentation, model directories must as a minimum, at the appropriate locations, contain the following scripts:
    - src/dataloaders/get_partitioned_data.py
    - src/training/train_experimental_model.py
    - src/offline_evaluation/evaluate_model.py
    - src/offline_evaluation/evaluate_sweep.py

- Furthermore, the following artifacts need to be present for experimentation and forecasting respectively.  
    - artifacts/model_train_partition.pth # or .pkl
    - artifacts/model_test_partition.pth # or .pkl
    - artifacts/model_forecasting.pth # or .pkl

- Outputs
    - The final output from the forecasting/generate_forecast.py should a an ...... array/pandas? of to quantify uncertainty list
