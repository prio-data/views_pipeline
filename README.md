# views_pipeline
VIEWS forecasting pipeline for monthly prediction runs. Includes MLops and QA for all models/ensembles.

REPO STRUCTURE:

pipeline_root/
|
|-- README.md
|-- LICENCE.md
|-- .gitignore
|
|-- models/
|   |-- model_001/ # should follow the naming convention adjective_noun
|   |   |
|   |   |-- README.md
|   |   |-- requirements.txt
|   |   |
|   |   |-- configs/ # ...
|   |   |   |-- config_sweep.py # hyperparameters for test_sweep.py (WandB sweep)
|   |   |   |-- config_hyperparameters.py # hyperparameters train_model.py
|   |   |
|   |   |-- data/ # all input, processed, output data
|   |   |    |-- raw/ # Data directly from VIEWSER
|   |   |    |-- processed/ # Data processed
|   |   |    |-- generated/ # Data generated - i.e. predictions/forecast
|   |   |
|   |   |-- artifacts/ # step-shift models will have 36 of each. pth or pkl. 
|   |   |   |-- model_metadata_dict.py # the standard meta data dict for models
|   |   |   |-- model_train_partition.pth # for offline validation 
|   |   |   |-- model_test_partition.pth # for offline testing
|   |   |   |-- model_forecasting.pth # for online forecasting
|   |   |
|   |   |-- notebooks/
|   |   |
|   |   |-- reports/ # dissemination material - internal and external 
|   |   |   |-- plots/ # plots for papers, reports, newsletters, and slides
|   |   |   |-- timelapse/ # plots to create timelapse and the timelapse
|   |   |   |-- papers/ # working papers, white papers, articles ect.
|   |   |   |-- slides/ # slides, presentation and similar. 
|   |   |
|   |   |-- src/ # all source code needed to train, test, and forecast
|   |       |
|   |       |-- dataloaders/ # scripts to get data from VIEWSER
|   |       |   |-- get_partitioned_data.py # standard train/val/test partition
|   |       |   |-- get_latest_data.py # the lastest data
|   |       |   
|   |       |-- architectures/ # only relevant for models developed in-house
|   |       |   |-- network.py # e.g a py script containing a pytorch nn class
|   |       |
|   |       |-- utils/ # functions and classes 
|   |       |   |-- utils.py # a general utils.py for all utils function
|   |       |   |-- utils_torch.py # sep. utils demanding more specific libraries
|   |       |   |-- utils_gpd.py # sep. utils demanding more specific libraries
|   |       |
|   |       |-- visualization/ # scripts to create visualizations
|   |       |
|   |       |-- training/
|   |       |   |-- train_model.py # script to train, and save, a model
|   |       |
|   |       |-- offline_evaluation/ # aka offline quality assurance
|   |       |   |-- evaluate_model.py # script to evaluate a train and saved model
|   |       |   |-- evaluate_sweep.py # script to run a wandb sweep
|   |       |
|   |       |-- online_evaluation/
|   |       |   |-- evaluate_forecast.py # continues performance check
|   |       |  
|   |       |-- drift_detection/ # aka online evalation 
|   |       |   |-- drift_detection_input.py # check new latest data
|   |       |   |-- drift_detection_output.py # check new forecasts
|   |       |   |-- drift_detection_performance.py # check new performance
|   |       |
|   |       |-- forecasting/
|   |           |-- generate_forecast.py #script to genereate true-future fc.
|   |
|   |-- model_002/
|   |   |-- ...
|   |   ...
|   ...
|
|-- ensembles/
|   |--ensemble_001/ #similar to model dir, with a few differences
|   |   |-- README.md 
|   |   |-- requirements.txt   
|   |   |
|   |   |-- configs/
|   |   |   |-- config_sweep.py 
|   |   |   |-- config_hyperparameters.py
|   |   |
|   |   |-- artifacts/
|   |   |   |-- ensemble_metadata_dict.py
|   |   |   |-- ensemble_forecasting.pkl
|   |   |
|   |   |-- notebooks/
|   |   |
|   |   |-- reports/
|   |   |   |-- plots/
|   |   |   |-- timelapse/
|   |   |   |-- papers/
|   |   |   |-- slides/
|   |   |
|   |   |-- src/
|   |       |
|   |       |-- dataloaders/
|   |       |   |-- get_model_outputs.py # model outputs instead of VIEWSER data 
|   |       |
|   |       |-- architecture/ # some ensembles might have an architecture
|   |       |   |-- ensemble.py
|   |       |
|   |       |-- utils/
|   |       |   |-- utils.py
|   |       |   
|   |       |-- visualization/
|   |       |
|   |       |-- training/
|   |       |   |-- train_ensemble.py # some ensembles might need training
|   |       |
|   |       |-- offline_evaluation/ # we do not have a clear routine for this yet
|   |       |   |-- evaluate_ensemble.py 
|   |       |   |-- evaluate_sweep.py
|   |       |
|   |       |-- online_evaluation/
|   |       |   |-- evaluate_forecast.py # continues performance check
|   |       |  
|   |       |-- drift_detection/ # aka online evalation 
|   |       |   |-- drift_detection_input.py # check new latest data
|   |       |   |-- drift_detection_output.py # check new forecasts
|   |       |   |-- drift_detection_performance.py # check new performance
|   |       |
|   |       |-- forecasting/
|   |           |--generate_forecast.py #script to genereate true-future fc.
|   |       
|   |
|   |--ensemble_002/
|   |   |-- ...
|   |   ...
|   ...
|
|
|-- prefect/
|    |--scripts.py # orchestration
|
|-- documentation/
|
|-- meta_tools/
		|-- make_new_model_dir.py # script to create a standard model dir
    |-- make_new_ensemble_dir.py # script to create a standard ensemble dir
    |-- asses_model_dir.py # check structure and presence of obligatory scripts
    |-- asses_ensemble_dir.py # check structure and presence of obligatory scripts  
