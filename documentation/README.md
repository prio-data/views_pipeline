# THIS README SHOULD BE MINIMAL AND MOST OF THE STUFF BELOW BE MIGRATED TO ARDs, THE GLOSSARY, OR SIMILAR.



# Documentation of VIEWS Pipeline

This is a collection of high-level documentation for the entire repository/pipeline. We aim to also offer in-depth documentation in folder READMEs and docstrings of functions and classes within the code.

## Motivation and Rationale
The VIEWS early-warning system pipeline produces predictions on a monthly basis, for a variety of models. However, in the last months, several errors have occured that compromise the quality of our forecasts. Additionally, the pipeline does not yet adhere to best practices standards relating to the structure and implementation. As a result, the VIEWS Pipeline is being rewritten and improved during a 5-day hackathon. 

A diagram of the pipeline schematics is available [here](https://github.com/prio-data/views_pipeline/blob/main/documentation/pipeline_diagram001.pdf).

We aim to develop a minimal solution first, that can be further developed in the future to accommodate more needs and models. The initial models implemented during the hackathon in February 2024 are: 2 baseline models (all zero, no change), 2 production models (orange pasta, yellow pikachu), and 1 bespoke shadow model (Hydranet).

The most important changes relate to the following elements: standardizing  moving away from Notebooks and towards scripts; implementing alert gates for input and performance drift; using the platform Weights & Biases for logging and visualizing model outputs; using the platform Prefect to carry out the entire monthly run, from fetching the input data through a queryset to allocating predictions in the prediction store on Fimbulthul server.

## Goals of the pipeline

1. **Maintainability**:
    - **Continuous Maintenance**: the code should be adaptable and easy to update without needing to overhaul the entire code base. This approach ensures long-term sustainability.
    - **Accessibility**: The code should be understandable by any Python-proficient collaborator in the VIEWS team - not just specialists or the original authors.
    - **Documentation**: Well-specified documentation must accompany the code, detailing its purpose and functionality clearly, so that no additional information is needed for understanding.

2. **Flexibility**:
    - **Rapid Testing and Integration**: The pipeline should allow for quick experimentation with new models or ensembles, enabling their fast integration AND removal.
    - **Ease of Modification**: Adding, retiring, or modifying models and ensembles should be straightforward, even by (python-proficient) collaborators who are not the original model or pipeline authors.
    - **Adaptability and modularity**: The process of altering the model lineup should be modular and not require extensive reworking of the overall system/code base.

3. **Scalability**:
    - **Global Expansion**: The pipeline should support scaling up to handle data and models with global coverage - even at highly disaggregate temporal and spatial levels.
    - **Incorporating Uncertainty**: It must be capable of integrating quantification of uncertainty.
    - **Furture-ready** It must be ready for new Levels of Analysis (LOAs), novel models, more features, and additional targets.
    - **Handling Diverse Data**: The system should be versatile enough to include and process various kinds of data, including both structured (tabular) and unstructured data (image/text).

4. **Reliability**:
    - **Automated Execution**: The full production pipeline should run monthly with minimal human intervention.
    - **Robustness in Partial Failure**: In case of a breakdown in certain parts (model or data-pipe issues), the unaffected components should continue operating.
    - **Issue Identification**: Faulty or compromised elements should be easily detectable through quality assurance processes (see below).

5. **Quality Assurance (Monitoring)**:
    - **Input Monitoring**: There should be mechanisms to quickly assess input data for any drift each time forecasts are generated.
    - **Output Monitoring**: Similarly, the output of the models should be evaluated for drift each time forecasts are generated.
    - **Performance Assessment**: Lastly, continuous and timely evaluation of each model's and ensemble's performance is necessary to detect and address any performance drift.

In summary, our pipeline aims to be maintainable, flexible, scalable, reliable, and continuously monitored for quality, ensuring it can adapt, grow, and perform efficiently well into the foreseeable future.

## Definition of Key Terms

**Model** is defined as follows:

1) A specific instantiation of a machine learning algorithm, 
2) Trained using a predetermined and unique set of hyperparameters,
3) On a well-defined set of input features,
4) And targeting a specific outcome target.
5) In the case of stepshift models, a model is understood as **all** code and **all** artifacts necessary to generate a comprehensive 36 month forecast for the specified target.
6) Note that, two models, identical in all other aspects, will be deemed distinct if varying post-processing techniques are applied to their generated predictions. For instance, if one model's predictions undergo calibration or normalization while the other's do not.

**Run** is defined as follows:

A *run* is a complete execution of the pipeline orchestrated through Prefect. It involves generating forecasts using all deployed baseline, shadow, and production models, including both individual models and ensembles. Additionally, a run encompasses various quality assurance measures such as model monitoring, drift detection, and online evaluation.

Typically, a *run* occurs once a month. However, additional runs may be performed within a month if corrections or calibrations are necessary to meet the quality standards expected of a VIEWS system.

As runs are relatively infrequent events, each run is assigned a *meaningful* name following established conventions. The name format is as follows: `modelset_generation_monthid_iteration`. For example:`fatalities_003_413_a`.

In this example, the run includes all deployed models targeting fatalities, belonging to the third generation of VIEWS *fatality* models. The run corresponds to month number 413 using the standard VIEWS month ID format. The trailing *a* signifies that this is the first run created this month; subsequent runs would be denoted with *b*, *c*, and so on, indicating the order of execution within the given target, generation, and month.

## Standardization and Naming
We have agreed to standardize the pipeline in several ways. 

### Model Naming Conventions
**Models** will no longer carry descriptive titles (e.g., *transform_log_clf_name_LGBMClassifier_reg_name_LGBMRegressor*). As more and more models are developed over time, this would become too chaotic, long, and ultimately small differences could not be communicated properly through the title. Instead, the code and metadata of the model should be use to substantively differentiate them between each other. 

The new naming convention for models in the pipeline takes the form of *adjective_noun*, adding more models alphabetically. For example, the first model to be added can be named *amazing_apple*, the second model *bad_bunny*, etc. This is a popular practice, and Weights & Biases implements this naming convention automatically. 

### GitHub Repository Strucuture
The entire pipeline is contained in the repository "views-pipeline", which has a predefined structure stated in the readme. As such, this pipeline repository replaces "viewsforecasting" (pipeline 002) and "views-runs" (pipeline 001) (*TBC*). 

The structure is based on best practices commonly observed in the machine learning community. Resources and references that discuss similar project structures and best practices include Cookiecutter Data Science, Kaggle Kernels, and a variety of MLOps books.
For the most recent version of the repository and its explanation, always check the [README](https://github.com/prio-data/views_pipeline/blob/main/README.md) in the main branch.

### Jupyter Notebooks
Developers can use Jupyter Notebooks for experimentation and validation purposes. However, no operational code will be written in Jupyter Notebook format, only in modular .py scripts. 

# Pipeline Components

## Configuration Files (Config)
In the pipeline, you can configure parameters of the entire pipeline in **common_configs**, or individual models, in the model-specific **configs** folder. 
Configuration files define hyperparameters for model training and tuning, facilitating reproducibility and experimentation. You can also see model information to make sense of the model given the non-descriptive naming system.

## Utility Functions (Utils)
We aim to reduce repetitive boilerplate code in model source code. As such, functions and classes that can be used in multiple models are placed in **common_utils**. In certain cases, utils can also be model-specific, for example for models employing more custom architecture like purple_alien.

## Data Loaders
Data loaders retrieve input data from viewser, preprocess it (i.e., perform transformations), conduct input drift detection and prepare it for model training and evaluation. This is separate from running the pipeline. 

The relevant config files are:
- common_configs/set_partition.py
- common_configs/config_drift_detection.py
- {model}/configs/config_input_data.py

The source code modules are:
- common_utils/utils_dataloaders.py
- {model}/src/dataloaders/get_partitioned_data.py

Key features include:
- We want to ensure data is strictly separated into the pre-defined data partitions.
- The default setting is to fetch new data instead of using a saved data file, in order to ensure that the most up-to-date data is being used in modelling.
- In case you need to re-do a previous run, you are able to override using this month as the start of the month.
- The data loader also automatically performs input drift detection and integrity checking, which has been incorporated as a feature into [viewser](https://github.com/prio-data/viewser). Detailed and up-to-date documentation of the input drift detection can be found in its repository README. Alerts are logged in weights & biases.

Future Development: 
- Detect overlap
- Experiment with threshholds of input drift detection
- There is not yet automated triggering of corrective actions when deviations are detected. We would like a Slackbot.

## Architectures 
Architectures, relevant primarily for in-house developed models, define the underlying structure and configuration of machine learning models.

## Model Training
The model training component trains machine learning models using predefined datasets and hyperparameters, optimizing performance and accuracy. We aim to re-train our models only once a year, hence we save trained models as artifacts locally.

The relevant config files are:
- common_configs/set_partition.py
- {model}/configs/config_hyperparameters.py (hyperparameters should be set after conducting a sweep/hyperparameter tuning)

The source code modules are:
- Depending on the model type, the training script will call on different utils modules such as common_utils/hurdle_model.py
- {model}/src/training/train_model.py

Future Development:
- Save and version trained models in weights & biases as artifacts

## Offline Evaluation and Hyperparameter Tuning 
Offline evaluation evaluates model performance using a static dataset before deployment. We evaluate trained & saved models (as artifacts) on the calibration or test partition. 

Hyperparameter sweeps provide an organized and efficient way to pick the most accurate model among different configurations of hyperparameter values (e.g. learning rate, batch size, number of hidden layers, optimizer type). We use the platform Weights & Biases to run and log sweeps. Sweeps should only be done on the calibration partition.

The relevant config files are:
- common_configs/set_partition.py
- {model}/configs/config_sweep.py 
- {model}/configs/config_hyperparameters.py

The source code modules are:
- common_utils/utils_artifacts.py
- common_utils/utils_model_outputs.py
- common_utils/utils_evaluation_metrics.py
- {model}/src/offline evaluation/evaluate_model.py

Future Development:

## Generating Forecasts
This component encompasses the generation of forecasts using deployed models and ensembles. The source code loads a trained model artifact and performs true forecasting with the specified hyperparameters and true future partitions. It subsequently saves the predictions as pickle files to {model}/data/generated. 

The relevant config files are:
- common_configs/set_partition.py
- {model}/configs/config_hyperparameters.py

The source code module is:
- {model}/src/forecasting/generate_forecast.py

Future Development:
- Save to prediction store
- Predict with uncertainty

## Ensembling

Not yet implemented.

## Visualization
Not yet implemented. 

## Model Management
The management source code brings together all aspects of data loading, hyperparameter tuning, model training, model evaluation, and future predictions. This folder could also have been called 'execution' or 'model orchestration'.

Initially, these functions were defined and called in each model's main.py file. However, we decided to abstract this into a source code folder which is called in main.py.

The source code modules are:
- {model}/src/management/execute_model_runs.py
- {model}/src/management/execute_model_tasks.py

## Pipeline Orchestration
In views_pipeline, every model and ensemble has its own main.py execution file. These are collected by the main orchestration script (in the root directory) that incorporates Prefect, **orchestration.py**.
As such, you can run an individual model using its main.py file, or run all models with orchestration.py.

The primary purpose of the orchestration script is to streamline the execution of machine learning models represented by separate `main.py` files. By automating the execution process, the script simplifies the workflow for running multiple models, reducing manual effort and potential errors.




