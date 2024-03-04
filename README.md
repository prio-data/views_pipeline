

---

# 🚧 Early Access Alert! 🚧

Welcome to our project! Please note that this pipeline is **actively under construction**. We're in the **early stages of development**, meaning it's **not yet ready for operational use**. We're working hard to bring you a robust and fully-functional tool, so stay tuned for updates!

---

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

Once models are run, you can also check their logs and visualizations in [Weights & Biases](https://wandb.ai/views_pipeline).

## Repository Structure and Explanations

```
pipeline_root/
|
|-- README.md
|-- LICENCE.md
|-- .gitignore
|
|-- models/
|   |-- exemplifying_model/                        # Should follow the naming convention adjective_noun
|   |   |
|   |   |-- README.md
|   |   |-- requirements.txt
|   |   |-- main.py                                 # Orchestration script (running the model via Prefect)
|   |   |
|   |   |-- configs/                                # All model specific config files
|   |   |   |-- config_model.py                     # Contains model architecture, name, target variable, and level of analysis (previous config_common minus partition info)
|   |   |   |-- config_hyperparameters.py           # Specifies the finalized hyperparameters used for training the deployed model (W&B specific).
|   |   |   |-- config_sweep.py                     # Configurations for hyperparameter sweeps during experimentation phases (W&B specific).
|   |   |   |-- config_feature_set.py               # Defines the features to be pulled from the views - basically the queryset. 
|   |   |   |-- config_deployment.py                # Status of the model regarding its lifecycle. I.e. is it in production, shadow mode, or a baseline model (or ESCWA...).
|   |   |
|   |   |-- data/                                   # all input, processed, output data -> might be out phased later to go directly from/to server
|   |   |    |-- raw/                               # Data directly from VIEiWSER
|   |   |    |-- processed/                         # Data processed
|   |   |    |-- generated/                         # Data generated - i.e. predictions/forecast
|   |   |
|   |   |-- artifacts/                              # Model artifacts. Step-shift models will have 36 of each. pth or pkl. 
|   |   |   |-- evelaution_metrics.py               # A dictionary containing the evaluation metrics for all 36 steps found in the test partetion. Potential weights.
|   |   |   |-- model_calibration_partition.pth     # Trained model object for offline evaluation during calibration and experimentation (trained on train set of calibration partition)
|   |   |   |-- model_test_partition.pth            # Trained model object for offline evaluation during final testing (trained on train set of the test calibration) 
|   |   |   |-- model_forecasting.pth               # Trained model object for online forecasting - i.e. the model object to be deployed and called during orcestration (train on forecasting partition)
|   |   |
|   |   |-- notebooks/                              # Only for developemt experimentation, and trouble-shooting. 
|   |   |
|   |   |-- reports/                                # dissemination material - internal and external 
|   |   |   |-- plots/                              # plots for papers, reports, newsletters, and slides
|   |   |   |-- figures/                            # figures for papers, reports, newsletters, and slides 
|   |   |   |-- timelapse/                          # plots to create timelapse and the timelapse
|   |   |   |-- papers/                             # working papers, white papers, articles ect.
|   |   |   |-- slides/                             # slides, presentation and similar. 
|   |   |
|   |   |-- src/                                    # all source code needed to train, test, and forecast
|   |       |
|   |       |-- dataloaders/                        # Model specfic scripts to get data from VIEWSER (input drift detection happens here)
|   |       |   |-- get_calibration_data.py         # The model specific data covering the standard calibration pertition
|   |       |   |-- get_test_data.py                # The model specific data covering the standard test pertition
|   |       |   |-- get_forecasting_data.py         # The model spefific date for forecasting during deployment - first observed month to last observed month
|   |       |
|   |       |-- architectures/                      # only relevant for models developed in-house
|   |       |   |-- network.py                      # e.g a py script containing a pytorch nn class
|   |       |
|   |       |-- utils/                              # functions and classes 
|   |       |   |-- utils.py                        # a general utils.py for all utils function
|   |       |   |-- utils_torch.py                  # sep. utils demanding more specific libraries
|   |       |   |-- utils_gpd.py                    # sep. utils demanding more specific libraries
|   |       |
|   |       |-- visualization/                      # scripts to create visualizations
|   |       |
|   |       |-- training/
|   |       |   |-- train_calibration_model.py      # Script for traning the model on train set of the calibration partition  
|   |       |   |-- train_testing_model.py          # Script for training the model on the train set of the test partition
|   |       |   |-- train_forecasting_model.py      # 
|   |       |
|   |       |-- offline_evaluation/                 # aka offline quality assurance
|   |       |   |-- evaluate_model.py               # script to evaluate a trained and saved model - can be calibration or test.
|   |       |   |-- evaluate_sweep.py               # script to run a wandb sweep - should only ever be used on the calibration partition
|   |       |
|   |       |-- online_evaluation/
|   |       |   |-- evaluate_forecast.py            # continues performance check of the deployed model (forecasting)
|   |       |
|   |       |-- forecasting/
|   |           |-- generate_forecast.py            # Script to genereate true-future forecasts.
|   |
|   |-- model_002/
|   |   |-- ...
|   |   ...
|   ...
|
|-- ensembles/
|   |--ensemble_001/                                # Similar to model dir, with a few differences
|   |   |-- README.md 
|   |   |-- requirements.txt
|   |   |-- main.py                                 # Orchestration script (running the ensemble)     
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
|   |       |   |-- get_model_outputs.py            # model outputs instead of VIEWSER data 
|   |       |
|   |       |-- architecture/                       # some ensembles might have an architecture
|   |       |   |-- ensemble.py
|   |       |
|   |       |-- utils/
|   |       |   |-- utils.py
|   |       |   
|   |       |-- visualization/
|   |       |
|   |       |-- training/
|   |       |   |-- train_ensemble.py               # some ensembles might need training
|   |       |
|   |       |-- offline_evaluation/                 # we do not have a clear routine for this yet
|   |       |   |-- evaluate_ensemble.py 
|   |       |   |-- evaluate_sweep.py
|   |       |
|   |       |-- online_evaluation/
|   |       |   |-- evaluate_forecast.py            # continues performance check
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
|-- orchestration.py # orchestration for entire pipeline (runs all models on Prefect)
|
|-- documentation/
|
|-- common_utils/ # Functions and classes used across multiple (but not necessary all) models  
|       |-- stepshifter.py # Updated stepshifter function
|       |-- set_paths.py # Sets all paths for imports, data, utils ect. Machine invariant. 
|       |-- get_data.py # General function that takes the general get_partion and a model specific config_feature_set.py to fetch model specific data.
|       |-- get_partion.py # Get data partitions for spilts pertaining to validation, testing, and forecasting. (Some of what were in config_common, but with a variable end point for forecast.) 
|
|-- templetes/ # For code templets. In the long run, most can been turn into common_utils (functions or classes), but might be useful for now.
|
|-- meta_tools/
		|-- make_new_model_dir.py # script to create a standard model dir
        |-- make_new_ensemble_dir.py # script to create a standard ensemble dir
        |-- asses_model_dir.py # check structure and presence of obligatory scripts
        |-- asses_ensemble_dir.py # check structure and presence of obligatory scripts  
```