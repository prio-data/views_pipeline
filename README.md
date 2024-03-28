# views_pipeline
The Violence & Impacts Early Warning System (VIEWS) produces monthly predictions of future violent conflict. This repository contains code, configuration files, and documentation that encapsulates the entire process of developing, training, evaluating, and deploying the VIEWS machine learning model pipeline.

This pipeline is made up of a series of machine learning models, structured in their own sub-folders. 

> [!CAUTION]
> Please note that this pipeline is **actively under construction**. We're in the **early stages of development**, meaning it's **not yet ready for operational use**. We're working hard to bring you a robust and fully-functional tool, so stay tuned for updates!

<img alt="VIEWS pipeline schematics." src="https://github.com/prio-data/views_pipeline/blob/main/documentation/pipeline_diagram001.pdf" width="100%">


## Table of contents

<!-- toc -->
- [Repository Structure and Explanations](#repository-structure-and-explanations)
- [Pipeline Execution](#pipeline-execution)
- [Pipeline Documentation](#pipeline-documentation)
- [Other Documentation](#other-documentation)


<!-- tocstop -->

## Repository Structure and Explanations

<details>
  <summary>See repository structure and explanations below:</summary>

```
pipeline_root/
|
|-- README.md                                       # What you are looking at
|-- LICENSE.md                                      # Creative commons (CC BY-NC-SA 4.0)
|-- .gitignore                                      # In place to ensure no unwanted file types get pushed to GitHub
|
|-- models/                                         # Parent directory for all individual models (see documentation for definition of "model")
|   |-- exemplifying_model/                         # Each individual model subdirectory should follow the naming convention adjective_noun
|   |   |
|   |   |-- README.md                               # Concise description of the model and relevant details written in "plain language"
|   |   |-- requirements.txt                        # Python version and libraries - should rarely deviate from a standard well-maintained VIEWS_env.
|   |   |-- main.py                                 # Orchestration script to run a deployed model via Prefect as part of a full monthly basis
|   |   |
|   |   |-- configs/                                # All model specific config files
|   |   |   |-- config_model.py                     # Contains model architecture, name, target variable, level of analysis and deployment status
|   |   |   |-- config_hyperparameters.py           # Specifies the finalized hyperparameters used for training the deployed model (W&B specific)
|   |   |   |-- config_sweep.py                     # Configurations for hyperparameter sweeps during experimentation phases (W&B specific)
|   |   |   |-- config_input_data.py                # Defines the features to be pulled from the views and used - basically the queryset
|   |   |
|   |   |-- data/                                   # All input, processed, output data -> might be out phased later to go directly from/to server
|   |   |    |-- raw/                               # Data directly from VIEWSER
|   |   |    |-- processed/                         # Data processed
|   |   |    |-- generated/                         # Data generated - i.e., predictions/forecast
|   |   |
|   |   |-- artifacts/                              # Model artifacts. Step-shift models will have 36 of each. pth or pkl.
|   |   |   |-- evaluation_metrics.py               # A dictionary containing the evaluation metrics for all 36 steps found in the test partition
|   |   |   |-- model_calibration_partition.pth     # Model object for offline evaluation, trained on train set of calibration partition
|   |   |   |-- model_test_partition.pth            # Model object for offline evaluation, trained on train set of the test partition
|   |   |   |-- model_forecasting.pth               # Model object for online forecasting, trained on the forecasting partition
|   |   |
|   |   |-- notebooks/                              # Only for development experimentation, and trouble-shooting.
|   |   |
|   |   |-- reports/                                # Dissemination material - internal and external
|   |   |   |-- plots/                              # Plots for papers, reports, newsletters, and slides
|   |   |   |-- figures/                            # Figures for papers, reports, newsletters, and slides
|   |   |   |-- timelapse/                          # Plots to create timelapse and the timelapse
|   |   |   |-- papers/                             # Working papers, white papers, articles etc.
|   |   |   |-- slides/                             # Slides, presentation, and similar
|   |   |
|   |   |-- src/                                    # All source code needed to train, test, and forecast
|   |       |
|   |       |-- dataloaders/                        # Model specific scripts to get data from VIEWSER (input drift detection happens here)
|   |       |   |-- get_calibration_data.py         # The model specific data covering the standard calibration partition
|   |       |   |-- get_test_data.py                # The model specific data covering the standard test partition
|   |       |   |-- get_forecasting_data.py         # The model specific data for forecasting during deployment - first observed month to last observed month
|   |       |
|   |       |-- architectures/                      # Only relevant for models developed in-house
|   |       |   |-- network.py                      # E.g., a py script containing a PyTorch nn class
|   |       |
|   |       |-- utils/                              # Model sepcific Functions and classes (common utils should be in the common_utils in root)
|   |       |   |-- utils.py                        # A general utils.py for all utils function
|   |       |   |-- utils_torch.py                  # Sep. utils demanding more specific libraries
|   |       |   |-- utils_gpd.py                    # Sep. utils demanding more specific libraries
|   |       |
|   |       |-- visualization/                      # Scripts to create visualizations
|   |       |
|   |       |-- training/
|   |       |   |-- train_calibration_model.py      # Script for training the model on train set of the calibration partition  
|   |       |   |-- train_testing_model.py          # Script for training the model on the train set of the test partition
|   |       |   |-- train_forecasting_model.py      # Script for training the model on the full forecasting partition
|   |       |
|   |       |-- offline_evaluation/                 # Offline evaluation and quality assurance
|   |       |   |-- evaluate_model.py               # Script to evaluate a trained and saved model - can be calibration or test
|   |       |   |-- evaluate_sweep.py               # Script to run a wandb sweep - should only ever be used on the calibration partition
|   |       |
|   |       |-- online_evaluation/
|   |       |   |-- evaluate_forecast.py            # Continuous performance check of the deployed forecasting model (W&B Specific)
|   |       |
|   |       |-- forecasting/
|   |           |-- generate_forecast.py            # Script to generate true-future forecasts.
|   |
|   |-- different_model/                            # Next model, similar structure
|   |   |-- ...
|   |   ...
|   ...
|
|-- ensembles/
|   |-- exemplifying_ensemble/                      # Similar to model dir, with a few differences
|   |   |-- README.md                               # Concise description of the ensemble and relevant details written in "plain language"
|   |   |-- requirements.txt
|   |   |-- main.py                                 # Orchestration script to run a deployed ensemble as part of a full run via Prefect on a monthly basis
|   |   |
|   |   |-- configs/                                # All ensemble specific config files
|   |   |   |-- config_ensemble.py                  # Contains ensemble architecture, name, target variable, level of analysis and deployment status
|   |   |   |-- config_hyperparameters.py           # If applicable, specifies the finalized hyperparameters of the ensemble (W&B specific)
|   |   |   |-- config_sweep.py                     # If applicable, specifies the hyperparameter sweeps during experimentation phases (W&B specific)
|   |   |
|   |   |-- artifacts/                              # Ensemble's artifacts. Not applicable to all ensembles
|   |   |   |-- evaluation_metrics.py               # A dictionary containing the evaluation metrics for all 36 steps found in the test partition
|   |   |   |-- ensemble_calibration_partition.pth  # If applicable, ensemble object for offline evaluation, calibration partition
|   |   |   |-- ensemble_test_partition.pth         # If applicable, ensemble object for offline evaluation, test partition
|   |   |   |-- ensemble_forecasting.pth            # If applicable, ensemble object for online forecasting, forecasting partition
|   |   |
|   |   |-- notebooks/                              # Only for development experimentation, and trouble-shooting.
|   |   |
|   |   |-- reports/                                # Dissemination material - internal and external
|   |   |   |-- plots/                              # Plots for papers, reports, newsletters, and slides
|   |   |   |-- figures/                            # Figures for papers, reports, newsletters, and slides
|   |   |   |-- timelapse/                          # Plots to create timelapse and the timelapse
|   |   |   |-- papers/                             # Working papers, white papers, articles etc.
|   |   |   |-- slides/                             # Slides, presentation, and similar
|   |   |
|   |   |-- src/                                    # All source code needed to train, test, and forecast
|   |       |
|   |       |-- dataloaders/                        # In most cases, ensembles will only take outputs from other models as input
|   |       |   |-- get_model_outputs.py            # Get outputs from individual models instead of VIEWSER data
|   |       |
|   |       |-- architecture/                       # Some ensembles might have an architecture
|   |       |   |-- ensemble.py                     # Script for said architecture
|   |       |
|   |       |-- utils/                              # Ensemble specific utils
|   |       |   |-- utils.py                        
|   |       |   
|   |       |-- visualization/                      # Scripts to create visualizations
|   |       |
|   |       |-- training/                           # Some ensembles might need training
|   |       |   |-- train_ensemble.py               # Script for such potential training
|   |       |
|   |       |-- offline_evaluation/                 # Offline evaluation and quality assurance
|   |       |   |-- evaluate_ensemble.py            # Script to evaluate an ensemble - can be used with calibration or test models
|   |       |   |-- evaluate_sweep.py               # Script to run a wandb sweep - should only ever be used with the calibration partition
|   |       |
|   |       |-- online_evaluation/
|   |       |   |-- evaluate_forecast.py            # Continuous performance check of the deployed forecasting ensemble (W&B Specific)
|   |       |
|   |       |-- forecasting/
|   |           |-- generate_forecast.py            # Script to generate true-future forecasts
|   |       
|   |
|   |-- different_ensemble/                         # Next ensemble, similar structure
|   |   |-- ...
|   |   ...
|   ...
|
|-- orchestration.py                                # Orchestration for the entire pipeline (runs all deployed models and ensembles via Prefect)
|
|-- documentation/                                  # All relevant documentation (wiki to come)
|
|-- common_utils/                                   # Functions and classes used across multiple (but not necessarily all) models/ensembles  
|       |-- stepshifter.py                          # Updated stepshifter function
|       |-- set_paths.py                            # Sets all paths for imports, data, utils etc. Machine invariant.
|       |-- get_data.py                             # General function that takes the general get_partition and a model specific config_feature_set.py to fetch model specific data
|
|-- common_configs/                                 # Config files common to all (or multiple) models or the larger pipeline
|       |-- set_partition.py                        # Set data partitions for splits pertaining to validation, testing, and forecasting
|
|-- templates/                                      # For code templates. In the long run, most can be turned into common_utils/meta_tools (as functions or classes)
|
|-- meta_tools/                                     # Some of these should be added to GitHub action for good CI/CD
        |-- make_new_model_dir.py                   # Script to create a standard model directory
        |-- make_new_ensemble_dir.py                # Script to create a standard ensemble directory
        |-- assess_model_dir.py                     # Check structure and presence of obligatory scripts
        |-- assess_ensemble_dir.py                  # Check structure and presence of obligatory scripts  
```
</details>

## Pipeline Execution
> [!CAUTION]
> We are still in the process of migrating our models to this repository. Until then, the monthly VIEWS run is conducted with the [viewsforecasting repository](https://github.com/prio-data/viewsforecasting).

For the monthly run, ensure that the latest input data has been ingested into the VIEWS database before.

This pipeline uses two tools for logging relevant information, to enhance transparency and collaboration. For the individual models, we use Weights & Biases (W&B / wandb) as a centralized platform for logging and monitoring model outputs, system metrics, and experiment metadata. This is especially relevant when tuning hyperparameters, for which we conduct so-called sweeps. For the entire pipeline, we use Prefect to log as a "flow run". 

Follow the steps below to execute an entire run of the VIEWS pipeline.

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

3. **Make desired changes to common configs and utils**
For changing the months in data partitions, go to [common_utils/set_partition.py](https://github.com/prio-data/views_pipeline/blob/main/common_utils/set_partition.py).

4. **Run the Orchestration Script:**
Execute the Prefect flow script to run all models in this repository.
```bash
python orchestration.py
```
The script executes every main.py file in every model and ensemble folder. For every model, you will be prompted in the terminal to:
    a) Do sweep 
    b) Do one run and pickle results
To conduct the monthly run, type `b` and enter.

The progress of the pipeline execution will be logged online on Prefect.

5. **Monitor Pipeline Execution:**
Once the pipeline is initiated, you can monitor its execution using the Prefect UI dashboard or CLI. You can copy the link given in the terminal, go to the website, or use the following command to launch the Prefect UI:
```bash
prefect server start
```

Once models are run, you can also check their logs and visualizations in [Weights & Biases](https://wandb.ai/views_pipeline).

## Pipeline Documentation
More detailed documentation on the pipeline and its components can be found in the folder [`documentation`](https://github.com/prio-data/views_pipeline/tree/main/documentation). More specifically there are entries on:
- Beginner Guide
- Model
- Pipeline

## Other Documentation
This pipeline repository relies on a lot of previous work documented in other papers and repositories.

The fatalities model generates forecasts for state-based armed conflict during each month in a rolling 3-year window. 
The latest iteration, currently in production, is called [Fatalities002](https://viewsforecasting.org/early-warning-system/models/fatalities002/).

The following links cover **modelling documentation** for Fatalities002:
- [Prediction models and input variables in main ensemble](https://viewsforecasting.org/views_documentation_models_fatalities002/)
- [Levels of analysis and dependent variables](https://viewsforecasting.org/wp-content/uploads/VIEWS_documentation_LevelsandOutcomes.pdf)
- [Partitioning and time shifting data for training, calibration, testing/forecasting, model weighting, and out-of-sample evaluation](https://viewsforecasting.org/wp-content/uploads/VIEWS_Documentation_Partitioningandtimeshifting_Fatalities002.pdf)
- [Ensembling and calibration](https://viewsforecasting.org/wp-content/uploads/VIEWS_documentation_Ensembling_Fatalities002.pdf)

For VIEWS-specific **infrastructure documentation**, please refer to following GitHub repositories:
- [`ingester3`: Loading input data into the views database](https://github.com/UppsalaConflictDataProgram/ingester3)
- [`viewser`: Accessing input data from views database](https://github.com/prio-data/viewser)
- [`views_api`: Our API for accessing predictions](https://github.com/prio-data/views_api)
- [`ForecastDrift`: New forecasting data drift detection system created for this pipeline](https://github.com/prio-data/ForecastDrift)

