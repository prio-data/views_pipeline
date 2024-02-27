# views_pipeline
VIEWS forecasting pipeline for monthly prediction runs. For more detailed documentation of rationale and components see **`documentation/pipeline_documentation.md`**

## How to Run This Pipeline
### Prerequisites

- Python 3.x
- Required Python packages: scikit-learn, pandas, TensorFlow, Prefect, wandb, viewser, ingester3, stepshift

### Execution Steps

1. **Clone the Repository:**

   ```bash
   git clone <https://github.com/prio-data/views_pipeline>

2. **Make sure Prefect is set up**

In your viewser environment, make sure prefect is pip installed.
You can check with ```pip show prefect```

To login to your account write:
```bash
prefect cloud login
```
and subsequently login online.

3. **Find Orchestration Script:**

Open the Python script containing the Prefect orchestration flow. 
Currently, it is in [views_pipeline/orchestration.py (in branch production_models)](https://github.com/prio-data/views_pipeline/blob/production_models/orchestration.py).

At this point you could configure the script.

4. **Run the Orchestration Script:**
Execute the Prefect flow script to run the ML pipeline.
```bash
python orchestration.py
```
The script executes every main.py file in every model and ensemble folder. For every model, you will be prompted in the terminal to:
    a) Do sweep 
    b) Do one run and pickle results
To conduct the monthly run, type `b` and enter.

The progress will be logged online on Prefect.

5. **Monitor Pipeline Execution:**
Once the pipeline is initiated, you can monitor its execution using the Prefect UI dashboard or CLI. You can copy the link given in the terminal, go to the website, or use the following command to launch the Prefect UI:
```bash
prefect server start
```

Once models are run, you can also check their logs and visualisations in [Weights & Biases](https://wandb.ai/views_pipeline).

## Repository Structure and Explanations

```
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
|   |   |   |-- config_partitioner.py OR config_common # calibration, test, forecasting partitions

|   |   |
|   |   |-- data/ # all input, processed, output data
|   |   |    |-- raw/ # Data directly from VIEiWSER
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
|   |   |   |-- figures/ # figures for papers, reports, newsletters, and slides 
|   |   |   |-- timelapse/ # plots to create timelapse and the timelapse
|   |   |   |-- papers/ # working papers, white papers, articles ect.
|   |   |   |-- slides/ # slides, presentation and similar. 
|   |   |
|   |   |-- src/ # all source code needed to train, test, and forecast
|   |       |
|   |       |-- dataloaders/ # scripts to get data from VIEWSER (and input drift detection)
|   |       |   |-- get_calibration_data.py # calibration training data
|   |       |   |-- get_forecasting_data.py # the forecasting data
|   |       |   |-- get_test_data.py # the testing data
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
|   |       |   |-- train_calibration_model.py # 
|   |       |   |-- train_testing_model.py # 
|   |       |   |-- train_forecasting_model.py # 
|   |       |
|   |       |-- offline_evaluation/ # aka offline quality assurance
|   |       |   |-- evaluate_model.py # script to evaluate a train and saved model
|   |       |   |-- evaluate_sweep.py # script to run a wandb sweep
|   |       |
|   |       |-- online_evaluation/
|   |       |   |-- evaluate_forecast.py # continues performance check
|   |       |
|   |       |-- drift detection/ #monitor changes in model performance
|   |       |   |-- drift_detection_output # check new forecasts
|   |       |   |-- drift_detection_performance # check new performance
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
```