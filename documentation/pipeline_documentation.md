# Documentation of VIEWS Pipeline 003 (i.e., Cabin Hackaton Pipeline)
[Link to readme](https://github.com/prio-data/views_pipeline/blob/main/README.md)

A series of other VIEWS-developed tools are relevant:
- For documentation of our data ingestion package (i.e., how to add input data to viewser), refer to [ingester3](https://github.com/UppsalaConflictDataProgram/ingester3).
- For documentation of accessing data on viewser, refer to [viewser](https://github.com/prio-data/viewser).
- For documentation of stepshifted models, refer to [stepshift](https://github.com/prio-data/stepshift)(*Work in Progress*).
- Please do not use the views-runs package. Views-runs is a previous attempt at a placeholder pipeline with notebooks. As such, it should not be used in the current pipeline due to incompatibilities in implementation.

## How to Run This Pipeline
This machine learning (ML) pipeline produces the monthly run of the VIEWS conflict forecasts. At this stage, it produces 5 models and is to be expanded gradually.

A single run of this pipeline is carried out using the workflow management system *Prefect*. 

### Prerequisites
Before running the ML pipeline, ensure that you have the following prerequisites installed:
    Python 3.x
    Prefect (install using ´pip install prefect´)
    Required Python packages for the ML pipeline (scikit-learn, pandas, TensorFlow, viewser, ingester3, stepshift)
### Steps to Launch the ML Pipeline Run
*work in progress*
1. **Clone the Repository:**
Clone the repository containing the ML pipeline code to your local machine.
```bash
git clone <https://github.com/prio-data/views_pipeline>
```
2. **Navigate to the Project Directory**
Navigate to the directory where your ML pipeline code is located.
```bash
cd <project_directory>
```
3. **Configure Prefect Flow:**
Open the Python script containing your Prefect flow (e.g., ml_pipeline.py) and configure it according to your pipeline requirements. Ensure that all necessary tasks, dependencies, and parameters are defined correctly.
4. **Run the ML Pipeline:**
Execute the Prefect flow script to run the ML pipeline.
```bash
python ml_pipeline.py
```
5. **Monitor Pipeline Execution:**
Once the pipeline is initiated, you can monitor its execution using the Prefect UI dashboard or CLI. Use the following command to launch the Prefect UI:
```bash
prefect server start
```

### Additional Notes


## Motivation and Rationale
The VIEWS early-warning system pipeline produces predictions on a monthly basis, for a variety of models. However, in the last months, several errors have occured that compromise the quality of our forecasts. Additionally, the pipeline does not yet adhere to best practices standards relating to the structure and implementation. As a result, the VIEWS Pipeline is being rewritten and improved during a 5-day hackathon. 

A diagram of the pipeline schematics is available [here](https://github.com/prio-data/views_pipeline/blob/main/documentation/pipeline_diagram001.pdf).

We aim to develop a minimal solution first, that can be further developed in the future to accommodate more needs and models. The initial models implemented during the hackathon in February 2024 are: 2 baseline models (all zero, no change), 2 production models (orange pasta, yellow pikachu), and 1 bespoke model (Hydranet).

The most important changes relate to the following elements: standardizing  moving away from Notebooks and towards scripts; implementing alert gates for input and performance drift; using the platform Weights & Biases for logging and visualizing model outputs; using the platform Prefect to carry out the entire monthly run, from fetching the input data through a queryset to allocating predictions in the prediction store on Fimbulthul server.

## Definition of Key Terms

**Model** is [defined](https://github.com/prio-data/views_pipeline/blob/main/documentation/model_definition.md) as:

    1) A specific instantiation of a machine learning algorithm, 
    2) Trained using a predetermined and unique set of hyperpara.meters,
    3) On a well-defined set of input features,
    4) And targeting a specific outcome target.
    5) In the case of stepshift models, a model is understood as **all** code and **all** artifacts necessary to generate a comprehensive 36 month forecast for the specified target.
    6) Note that, two models, identical in all other aspects, will be deemed distinct if varying post-processing techniques are applied to their generated predictions. For instance, if one model's predictions undergo calibration or normalization while the other's do not.

**Run** is [defined](https://github.com/prio-data/views_pipeline/blob/main/documentation/run_definition.md) as follows:

    A *run* is a complete execution of the pipeline orchestrated through Prefect. It involves generating forecasts using all deployed baseline, shadow, and production models, including both individual models and ensembles. Additionally, a run encompasses various quality assurance measures such as model monitoring, drift detection, and online evaluation.

    Typically, a *run* occurs once a month. However, additional runs may be performed within a month if corrections or calibrations are necessary to meet the quality standards expected of a VIEWS system.

    As runs are relatively infrequent events, each run is assigned a *meaningful* name following established conventions. The name format is as follows: `modelset_generation_monthid_iteration`. For example:`fatalities_003_413_a`.

    In this example, the run includes all deployed models targeting fatalities, belonging to the third generation of VIEWS *fatality* models. The run corresponds to month number 413 using the standard VIEWS month ID format. The trailing *a* signifies that this is the first run created this month; subsequent runs would be denoted with *b*, *c*, and so on, indicating the order of execution within the given target, generation, and month.

## Standardization
We have agreed to standardize the pipeline in several ways. 

### Model Naming Conventions
**Models** will no longer carry descriptive titles (e.g., *transform_log_clf_name_LGBMClassifier_reg_name_LGBMRegressor*). As more and more models are developed over time, this would become too chaotic, long, and ultimately small differences could not be communicated properly through the title. Instead, the code and metadata of the model should be use to substantively differentiate them between each other. 

The new naming convention for models takes the form of *adjective_noun*, adding more models alphabetically. For example, the first model to be added can be named *amazing_apple*, the second model *bad_bunny*, etc. This is a popular practice, and Weights & Biases implements this naming convention automatically. 

*To be clarified: how to "translate" when moving from model development to communicating results.*

### Model Metadata 
*There is general disagreement to the degree of automatic vs. manual entry & length of model metadata -- work in progress*

### GitHub Repository Strucuture
The entire pipeline is contained in the repository "views-pipeline", which has a predefined structure stated in the readme. As such, this pipeline repository replaces "viewsforecasting" (pipeline 002) and "views-runs" (pipeline 001) (*TBC*). 

The structure is based on best practices commonly observed in the machine learning community. Resources and references that discuss similar project structures and best practices include Cookiecutter Data Science, Kaggle Kernels, and a variety of MLOps books.

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
|   |       |   |-- train_experimental_model.py # train on the standard pertitions
|   |       |   |-- train_pipeline_model.py # train a model on all availible data
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

```

The root (entire pipeline) contains folders for: models; ensembles; prefect; documentation; and meta-tools. 

First, within the **models folder**, there is a sub-folder for each model (as defined and named above). Essentially, everything related to a model is then contained: **config** files with hyperparameters for the test sweep conducted on Weights & Biases, as well as hyperparameters for model training.

Secondly, at least for the initial phase, the models folder also contains a sub-folder for **data**, with raw input, processed input, and generated data. 

Third, **artifacts** sub-folder contains model_metadata_dict.py (stores model metadata); model_train_partition.pth (for offline validation), model_test_partition.pth (for offline testing); and model_forecasting.pth (for online forecasting). 

Fourth, there is a **notebook** sub-folder where experimentation can go. All other code in the repository is in python script format.

Fifth, in the **reports** sub-folder we include internal and external dissemination material (if applicable) for the specific model.

Sixth, every model folder contains a source code (src) sub-folder, with code for loading data from viewser, optional pytorch architecture for in-house bespoke models, utils containing functions and classes, visualization scripts, training scripts, evaluation scripts (online, offline, drift detection), as well as the final script to generate the forecasts.

# Pipeline Components

## Configuration Files for Hyperparameter Tuning (Config)
Configuration files define hyperparameters for model training and tuning, facilitating reproducibility and experimentation.

## Data Loaders
Data loaders retrieve input data from viewser, preprocess it, and prepare it for model training and evaluation.

## Architectures (Optional)
Architectures, relevant primarily for in-house developed models, define the underlying structure and configuration of machine learning models.

## Model Training
The model training component trains machine learning models using predefined datasets and hyperparameters, optimizing performance and accuracy.

## Logging on Weights & Biases
Weights & Biases serves as a centralized platform for logging and monitoring model outputs, system metrics, and experiment metadata, enhancing transparency and collaboration.

The chosen platform is Weights & Biases (W&B / wandb). W&B automatically logs the following information during a W&B Experiment:
- System metrics: CPU and GPU utilization, network, etc. These are shown in the System tab on the run page. For the GPU, these are fetched with nvidia-smi.
- Command line: The stdout and stderr are picked up and show in the logs tab on the run page.

Other logged objects include:
- Plots: Using wandb.plot with wandb.log to track charts. 
- Tables: Using wandb.Table to log data to visualize and query with W&B
- Configuration information: Log hyperparameters, link to dataset, or  name of architecture used as config parameters
- Metrics: Use wandb.log to see metrics from your model. 


## Monitor and Assess Model Performance
We use drift detection, online evaluation, and offline evaluation to monitor and assess model performance. Drift detection focuses on monitoring changes in the data distribution over time, online evaluation assesses model performance in real-time as it interacts with new data, and offline evaluation evaluates model performance using a static dataset before deployment. Each of these techniques plays a vital role in ensuring the effectiveness and reliability of our ML models.

### Offline Evaluation
This includes a sweep in Weights & Biases, where the following metrics will be logged: 

- Mean Squared Error (MSE): Measures the average squared difference between predicted values and actual values.
- Mean Log Squared Error (MLSE): Similar to MSE, but operates on the logarithm of the predicted and actual values, useful for data with large variations.
- Jeffreys Divergence: A measure of the difference between two probability distributions, emphasizing sensitivity to small changes in probability.
- Jenson-Shannon Divergence: Quantifies the similarity between two probability distributions by measuring the average divergence of each from their average, providing a symmetric measure of similarity.

*Thus far for the production models, we only have MSE in the code though*

### Online Evaluation

### Drift Detection (Alertgate)
Drift detection mechanisms monitor changes in data distribution and model performance, triggering corrective actions when deviations are detected. The results of the drift detection (alert gate) will also be logged on Weights & Biases.


#### Check Input Data
Input data drift is monitored by analyzing dataframes for changes in missing values and distribution, ensuring data integrity and reliability.

*Will probably be put into viewser*

#### Check Output Data (ForecastDrift)
Output data drift is assessed using a bespoke alertgate package, developed to monitor and analyze forecast outputs for deviations from expected behavior.

Link to package: [ForecastDrift](https://github.com/prio-data/ForecastDrift)

**Installation**
```bash
pip install ForecastDrift
```

```Python
from ForecastDrift import ForecastDrift
```

There are two kinds of drift detection:
1. Current Predictions for a model compared to immediate predecessor run
    Alerts if models drift beyond a fixed user-specified threshhold.
2. Current predictions for a model compared to time series of previous runs using aggregate functions
    Alerts if models drift beyond a number of user-specified standard deviations from the mean of the previous prediction tables. Note that both dispersion function and the centrality function can be changed by user.

Users can specify any metrics, as long as it conforms to scikitlearn metrics. You pass a function to the package.
Package contains extra metrics, e.g., "Markov Anomaly" (values becoming NA).

Alerts are built as an independent class and can be easily extended and inherited from.
Forecast drift is test-driven development.

There is a print log as well.

## Visualization
Visualizations are accessible on Weights & Biases. There is a suite of interactive plots (bar charts, line graphs, tables).

We also produce maps for predicted fatalities, with standardised design and tick labels (*work in progress*). The goal is to create a running gif across steps and publish on Weights & Biases reports, instead of looking at 36 single maps.

*At this stage, this does not replace the mapper plots of the monthly run*

## Generating Forecasts
This component encompasses the generation of forecasts using deployed models and ensembles, ensuring accuracy and timeliness in our predictions.

## Orchestration/Deploying the pipeline with Prefect
Orchestration, in the context of workflow management systems like Prefect, refers to the coordination and execution of a series of tasks or operations in a specified order. It involves managing the flow of data and control between different tasks to ensure that they are executed correctly and efficiently.

The workflow tasks are:
For each model
1. Classify as baseline, shadow, production
    Look at artifacts/model_metadata_dict
2. Run src/forecasting/generate_forecast.py 
    For this to work, src/dataloaders/get_latest_data.py needs to be in generate_forecast

# Future Developments


# Glossary for Beginners

## Config File
Config files specify the settings and hyperparameters used to train machine learning models, allowing for easy experimentation and optimization without modifying the code – i.e., you don't want to hard code (i.e., write directly) hyperparameters into your model code.

## Orchestration
The Prefect Flow coordinates the execution of tasks, ensuring that they are executed in the correct order based on their dependencies.

## Hyperparameters
Hyperparameters are parameters or settings that are not directly learned from data during the training process of a machine learning model, but rather are set prior to training and influence the behavior and performance of the model. For example, hyperparameters could include the learning rate, number of estimators, number of jobs, and transformation of data.

## Prefect
Prefect is used for workflow orchestration, defining the sequence of tasks (task1, task2, task3) and their dependencies.

## Sweep
A sweep configuration is a set of specifications defining how hyperparameters should be explored during a hyperparameter search, the hyperparameters to be tuned, and their respective ranges or values to be tried.

## Weights & Biases (wandb)
Weights & Biases (W&B) is used to log relevant information (such as data, transformations, and results) produced by each task during the execution of the workflow. W&B logging within each task enables tracking and monitoring of the workflow's progress and outputs, enhancing visibility and reproducibility.

## Utils/Utility Functions
Collection of functions or tools that serve various general purposes and are commonly reused across different parts of a software project. These utility functions are often not specific to any particular domain or task but rather provide common functionalities that can be helpful in many different situations.

