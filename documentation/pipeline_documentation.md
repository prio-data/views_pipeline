# Documentation of VIEWS Pipeline 001 (i.e., Cabin Hackaton Pipeline)

## Motivation and Rationale
The VIEWS early-warning system pipeline produces predictions on a monthly basis, for a variety of models. However, in the last months, several errors have occured that compromise the quality of our forecasts. Additionally, the pipeline does not yet adhere to best practices standards relating to the structure and implementation. As a result, the VIEWS Pipeline is being rewritten and improved during a 5-day hackathon. 

We aim to develop a minimal solution first, that can be further developed in the future to accommodate more needs and models. The initial models implemented during the hackathon in February 2024 are: 2 baseline models (all zero, no change), 2 production models (orange pasta, yellow pikachu), and 1 bespoke model (Hydranet).

The most important changes relate to the following elements: standardizing  moving away from Notebooks and towards scripts; implementing alert gates for input and performance drift; using the platform Weights & Biases for logging and visualizing model outputs; using the platform Prefect to carry out the entire monthly run, from fetching the input data through a queryset to allocating predictions in the prediction store on Fimbulthul server.

## Definition of Key Terms

**Model** is understood as:

    1) A specific instantiation of a machine learning algorithm, 
    2) Trained using a predetermined and unique set of hyperpara.meters,
    3) On a well-defined set of input features,
    4) And targeting a specific outcome target.
    5) In the case of stepshift models, a model is understood as **all** code and **all** artifacts necessary to generate a comprehensive 36 month forecast for the specified target.
    6) Note that, two models, identical in all other aspects, will be deemed distinct if varying post-processing techniques are applied to their generated predictions. For instance, if one model's predictions undergo calibration or normalization while the other's do not.

**Run** is defined as follows:

    A *run* is a complete execution of the pipeline orchestrated through Prefect. It involves generating forecasts using all deployed baseline, shadow, and production models, including both individual models and ensembles. Additionally, a run encompasses various quality assurance measures such as model monitoring, drift detection, and online evaluation.

    Typically, a *run* occurs once a month. However, additional runs may be performed within a month if corrections or calibrations are necessary to meet the quality standards expected of a VIEWS system.

    As runs are relatively infrequent events, each run is assigned a *meaningful* name following established conventions. The name format is as follows: `target_generation_monthid_iteration`. For example:

    ```
    fatalities_003_413_a
    ```

    In this example, the run includes all deployed models targeting fatalities, belonging to the third generation of VIEWS *fatality* models. The run corresponds to month number 413 using the standard VIEWS month ID format. The trailing *a* signifies that this is the first run created this month; subsequent runs would be denoted with *b*, *c*, and so on, indicating the order of execution within the given target, generation, and month.

## Standardization
We have agreed to standardize the pipeline in several ways. 

### Model Naming Conventions
**Models** will no longer carry descriptive titles (e.g., *transform_log_clf_name_LGBMClassifier_reg_name_LGBMRegressor*). As more and more models are developed over time, this would become too chaotic, long, and ultimately small differences could not be communicated properly through the title. Instead, the code and metadata of the model should be use to substantively differentiate them between each other. 

The new naming convention for models takes the form of *adjective_noun*, adding more models alphabetically. For example, the first model to be added can be named *amazing_apple*, the second model *bad_bunny*, etc. This is a popular practice, and Weights & Biases implements this naming convention automatically. 

*To be clarified: how to "translate" when moving from model development to communicating results.*

### Model Metadata 
*There is general disagreement to the degree of automatic vs. manual entry & length of model metadata -- work in progress*

### GitHub Repository
The entire pipeline is contained in the repository "views-pipeline", which has a predefined structure stated in the readme. As such, this pipeline repository replaces "viewsforecasting" (*TBC*). 

The root (entire pipeline) contains folders for: models; ensembles; prefect; documentation; and meta-tools. 

First, within the **models folder**, there is a sub-folder for each model (as defined and named above). Essentially, everything related to a model is then contained: **config** files with hyperparameters for the test sweep conducted on Weights & Biases, as well as hyperparameters for model training.

Secondly, at least for the initial phase, the models folder also contains a sub-folder for **data**, with raw input, processed input, and generated data. 
*Question: Is this in terms of queryset code, or a file, e.g. parquet?*

Third, **artifacts** sub-folder contains model_metadata_dict.py (stores model metadata); model_train_partition.pth (for offline validation), model_test_partition.pth (for offline testing); and model_forecasting.pth (for online forecasting). 

Fourth, there is a **notebook** sub-folder where experimentation can go. All other code in the repository is in python script format.

Fifth, in the **reports** sub-folder we include internal and external dissemination material (if applicable) for the specific model.

# Pipeline Components

## Generating Forecasts

## Configuration Files for Hyperparameter Tuning (Config)

## Data Loaders

## Optional: Architectures

## Model Training

## Offline Evaluation
This includes a sweep in Weights & Biases, where the following metrics will be logged: 

- Mean Squared Error (MSE): Measures the average squared difference between predicted values and actual values.
- Mean Log Squared Error (MLSE): Similar to MSE, but operates on the logarithm of the predicted and actual values, useful for data with large variations.
- Jeffreys Divergence: A measure of the difference between two probability distributions, emphasizing sensitivity to small changes in probability.
- Jenson-Shannon Divergence: Quantifies the similarity between two probability distributions by measuring the average divergence of each from their average, providing a symmetric measure of similarity.

*Thus far for the production models, we only have MSE in the code though*

## Online Evaluation / Drift Detection
We are development an alertgate package that can be pip installed.

The results of the drift detection (alert gate) will also be logged on Weights & Biases.
### Check Input Data

### Check Output Data

### Check Performance

## Visualization
Visualizations are accessible on Weights & Biases. There is a suite of interactive plots (bar charts, line graphs, tables).

We also produce maps for predicted fatalities, with standardised design and tick labels (*work in progress*). The goal is to create a running gif across steps and publish on Weights & Biases reports, instead of looking at 36 single maps.

*At this stage, this does not replace the mapper plots of the monthly run*

# Glossary for Beginners

## Config File
Config files specify the settings and hyperparameters used to train machine learning models, allowing for easy experimentation and optimization without modifying the code – i.e., you don't want to hard code (i.e., write directly) hyperparameters into your model code.

## Hyperparameters
Hyperparameters are parameters or settings that are not directly learned from data during the training process of a machine learning model, but rather are set prior to training and influence the behavior and performance of the model. For example, hyperparameters could include the learning rate, number of estimators, number of jobs, and transformation of data.

## Sweep
A sweep configuration is a set of specifications defining how hyperparameters should be explored during a hyperparameter search, the hyperparameters to be tuned, and their respective ranges or values to be tried.

## Utils/Utility Functions
Collection of functions or tools that serve various general purposes and are commonly reused across different parts of a software project. These utility functions are often not specific to any particular domain or task but rather provide common functionalities that can be helpful in many different situations.

