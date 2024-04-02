# Documentation of Pipeline in VIEWS Pipeline

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

## Standardization
We have agreed to standardize the pipeline in several ways. 

### Model Naming Conventions
**Models** will no longer carry descriptive titles (e.g., *transform_log_clf_name_LGBMClassifier_reg_name_LGBMRegressor*). As more and more models are developed over time, this would become too chaotic, long, and ultimately small differences could not be communicated properly through the title. Instead, the code and metadata of the model should be use to substantively differentiate them between each other. 

The new naming convention for models in the pipeline takes the form of *adjective_noun*, adding more models alphabetically. For example, the first model to be added can be named *amazing_apple*, the second model *bad_bunny*, etc. This is a popular practice, and Weights & Biases implements this naming convention automatically. 

### GitHub Repository Strucuture
The entire pipeline is contained in the repository "views-pipeline", which has a predefined structure stated in the readme. As such, this pipeline repository replaces "viewsforecasting" (pipeline 002) and "views-runs" (pipeline 001) (*TBC*). 

The structure is based on best practices commonly observed in the machine learning community. Resources and references that discuss similar project structures and best practices include Cookiecutter Data Science, Kaggle Kernels, and a variety of MLOps books.
For the most recent version of the repository and its explanation, always check the [README](https://github.com/prio-data/views_pipeline/blob/main/README.md) in the main branch.

# Pipeline Components

## Configuration Files (Config)
In the pipeline, you can configure parameters of the entire pipeline in **common_configs**, or individual models, in the model-specific **configs** folder. 
Configuration files define hyperparameters for model training and tuning, facilitating reproducibility and experimentation. You can also see model information to make sense of the model given the non-descriptive naming system.

## Data Loaders
Data loaders retrieve input data from viewser, preprocess it, and prepare it for model training and evaluation.

The **get_data.py** script retrieves and preprocesses data for modeling from a database using the Viewser library. It then publishes the data and saves it to a Parquet file for later use.


## Architectures (Optional)
Architectures, relevant primarily for in-house developed models, define the underlying structure and configuration of machine learning models.

## Model Training
The model training component trains machine learning models using predefined datasets and hyperparameters, optimizing performance and accuracy.

## Ensembling
For ensembling in VIEWS, please refer to the [Fatalities002 documentation paper on Ensembling and Calibration](https://viewsforecasting.org/wp-content/uploads/VIEWS_documentation_Ensembling_Fatalities002.pdf).

In the pipeline, just like for individual models, ensemble models also have their own folder. Differences to the model include:
- In **src/dataloaders**, instead of calling a queryset, we get the outputs from the models contained in the ensemble.


## Monitor and Assess Model Performance
We use drift detection, online evaluation, and offline evaluation to monitor and assess model performance. Drift detection focuses on monitoring changes in the data distribution over time, online evaluation assesses model performance in real-time as it interacts with new data, and offline evaluation evaluates model performance using a static dataset before deployment. Each of these techniques plays a vital role in ensuring the effectiveness and reliability of our ML models.

### Offline Evaluation and Hyperparameter Tuning 
Offline evaluation evaluates model performance using a static dataset before deployment.

Hyperparameter sweeps provide an organized and efficient way to pick the most accurate model among different configurations of hyperparameter values (e.g. learning rate, batch size, number of hidden layers, optimizer type). We use the platform Weights & Biases to run and log so-called **hyperparameter sweeps**.

There is a data class for storing and managing evaluation metrics for time series forecasting models. See documentation [here](https://github.com/prio-data/views_pipeline/blob/main/common_utils/utils_evaluation_metrics.py).
Attributes are:
        MSE (Optional[float]): Mean Squared Error.
        MAE (Optional[float]): Mean Absolute Error.
        MSLE (Optional[float]): Mean Squared Logarithmic Error.
        KLD (Optional[float]): Kullback-Leibler Divergence.
        Jeffreys (Optional[float]): Jeffreys Divergence.
        CRPS (Optional[float]): Continuous Ranked Probability Score.
        Brier (Optional[float]): Brier Score.
        AP (Optional[float]): Average Precision.
        AUC (Optional[float]): Area Under the ROC Curve.
        ensemble_weight_reg (Optional[float]): Weight for regression ensemble models.
        ensemble_weight_class (Optional[float]): Weight for classification ensemble models.

Relevant scripts in model sub-folders:
- `evaluate_model.py` evaluates a trained and saved model. This can be used on the calibration or test partition.
- `evaluate_sweep.py` runs a wandb sweep to tune hyperparameters. This should only ever be used on the calibration partition.

### Online Evaluation
Online evaluation assesses model performance in real-time as it interacts with new data. To be implemented.

### Drift Detection (Alertgate)
Drift detection mechanisms monitor changes in data distribution and model performance, triggering corrective actions when deviations are detected. The results of the drift detection (alert gate) will also be logged on Weights & Biases.

### Check Input Data
Input data drift is monitored by analyzing dataframes for changes in missing values and distribution, ensuring data integrity and reliability.

This functionality has been incorporated into querysets in viewser.
The source code is in following scripts (currently in the branch `drift_detection`):

**`viewser/viewser/commands/queryset/config_drift.py`**

The `drift_config.py` file contains configuration settings related to drift detection in a system or process. These settings determine thresholds and partition lengths used in drift detection algorithms.

Configuration Settings:
- **threshold_global_nan_frac**: (float) Threshold for the fraction of missing values in the entire dataset.
- **threshold_feature_nan_frac**: (float) Threshold for the fraction of missing values in a single feature (column) of the dataset.
- **threshold_time_unit_nan_frac**: (float) Threshold for the fraction of missing values in a time unit (e.g., per day).
- **threshold_space_unit_nan_frac**: (float) Threshold for the fraction of missing values in a spatial unit (e.g., per region).
- **threshold_delta**: (float) Threshold for the magnitude of change between consecutive data points to detect drift.
- **standard_partition_length**: (int) Length of the standard partition used in drift detection algorithms.
- **test_partition_length**: (int) Length of the test partition used in drift detection algorithms.

These configuration settings are used to customize the behavior of drift detection algorithms according to specific requirements and constraints.

**`viewser/viewser/commands/queryset/drift_alert.py`**

Creates DriftAlert class, which:
- represents a notification for drift detection in a system or process
- encapsulates information about the entity responsible for the drift and any associated unusual operating activities (UOAs).

Attributes are:
- **offender**: (str) The entity responsible for the detected drift.
- **uoas**: (list) A list of Unusual Operating Activities (UOAs) associated with the detected drift.


**`viewser/viewser/commands/queryset/operations.py`**

The `queryset_operations.py` module provides operations related to managing and interacting with querysets, including the new drift detection functionality.

Drift Detection:
- **fetch_with_drift_detection(queryset_name:str, out_file: Optional[BufferedWriter] = None, start_date: Optional[date] = None, end_date: Optional[date] = None)**:
  - Fetches the specified queryset and performs drift detection.
  - **Parameters:**
    - queryset_name (str): Name of the queryset to fetch and analyze for drift.
    - out_file (BufferedWriter, optional): File to write queryset to.
    - start_date (Optional[date], optional): Start date for fetching queryset data.
    - end_date (Optional[date], optional): End date for fetching queryset data.
  - **Returns:**
    - Tuple[pd.DataFrame, drift_detection.InputGate]: A tuple containing the DataFrame corresponding to the queryset and the input alerts generated by drift detection.



### Check Output Data (ForecastDrift)
Output data drift is assessed using a bespoke alertgate package, developed to monitor and analyze forecast outputs for deviations from expected behavior.

Link to package including documentation: [ForecastDrift](https://github.com/prio-data/ForecastDrift)

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

## Generating Forecasts
This component encompasses the generation of forecasts using deployed models and ensembles, ensuring accuracy and timeliness in our predictions.

The **generate_forecasts.py** script generates forecasts using the Views Forecasts library. It retrieves predictions from a storage if available, otherwise, it generates forecasts using a specified prediction method and data.

### Functions:

#### `forecast(config)`:
This function generates forecasts using the Views Forecasts library.

- **Args**:
    - `config` (dict): A dictionary containing configuration parameters for forecasting.
        - Required keys:
            - `'storage_name'`: A string specifying the name of the storage to read/store forecasts.
            - `'RunResult'`: An object containing prediction method and data for forecasting.

- **Returns**:
    - None

### Dependencies:
- os
- warnings
- pandas (`pd`)
- Views Forecasts library

### Note:
The script sets up the environment to suppress warnings and silence Weights & Biases logging. It then attempts to read predictions from the specified storage. If no predictions are found, it generates forecasts using the prediction method specified in `config["RunResult"]` and the associated data, and stores the forecasts in the specified storage for future use.


## Orchestration: Executing the pipeline with Prefect
Orchestration, in the context of workflow management systems like Prefect, refers to the coordination and execution of a series of tasks or operations in a specified order. It involves managing the flow of data and control between different tasks to ensure that they are executed correctly and efficiently.

In views_pipeline, every model and ensemble has its own main.py execution file. These are collected by the main orchestration script (in the root directory) that incorporates Prefect, **orchestration.py**.
As such, you can still run an individual model using its main.py file, or run all models with orchestration.py.

The primary purpose of the orchestration script is to streamline the execution of machine learning models represented by separate `main.py` files. By automating the execution process, the script simplifies the workflow for running multiple models, reducing manual effort and potential errors.

### Model-specific main.py scripts

**Functions:**

#### `model_pipeline(config=None, project=None)`:
This function defines the model pipeline, including model training, forecasting, and evaluation. It initializes a Weights & Biases run with the specified project and configuration settings, and then executes the pipeline steps accordingly.

- **Args**:
    - `config` (dict): A dictionary containing configuration parameters for the model pipeline.
    - `project` (str): A string specifying the project name for Weights & Biases logging.

- **Returns**:
    - None

#### Dependencies:
- wandb
- pathlib (`Path`)
- `get_hp_config`, `get_swep_config`, `get_common_config` functions from respective configuration files
- `train`, `forecast`, `evaluate_model`, `evaluate_sweep`, `get_data` functions from respective modules

#### Note:
- The script initializes a Weights & Biases run with the specified project and configuration settings.
- It checks if raw data exists and loads it if not.
- Based on user input, it either conducts a hyperparameter sweep (`do_sweep == 'a'`) or performs a single model run (`do_sweep == 'b'`).
- For a hyperparameter sweep, it defines a sweep configuration using `wandb.sweep()` and runs the pipeline with the defined configuration using `wandb.agent()`.
- For a single model run, it runs the pipeline with the provided hyperparameters and project name.

### Pipeline orchestration.py script
The orchestration script, named `orchestration.py`, is a Python script designed to automate the execution of multiple machine learning models represented by `main.py` files located within the project's directory structure. 

**Logic:**
The orchestration script leverages the Prefect library, a workflow orchestration tool, to define and execute a Prefect Flow named `model_execution_flow`. This flow iterates over each `main.py` file found within the `models` directory and executes them as subprocesses using the `execute_main` task.

1. **Defining Paths:** The script uses the `pathlib` module to define the root directory where the `main.py` files are located (`root_dir`).

2. **Task Definition:** It defines a Prefect task (`execute_main`) responsible for executing a single `main.py` file as a subprocess.

3. **Flow Definition:** The `model_execution_flow` Prefect Flow is defined, which iterates over each `main.py` file found within the `models` directory and assigns the execution task to them.

4. **Execution:** Finally, the Prefect workflow (`model_execution_flow`) is executed, triggering the execution of each `main.py` file.


**Functions:**

### `execute_main`

- **Args:** 
    - `main_file`: Path to the main.py file of a machine learning model.

- **Returns:** 
    - None

### model_execution_flow

- **Args:** 
    - None

- **Returns:** 
    - None

#### Dependencies:
- Python (>= 3.6)
- Prefect library

#### Note:
The orchestration script automates the execution of machine learning models represented by `main.py` files. It leverages Prefect to define and execute a Prefect Flow named `model_execution_flow`, which iterates over each `main.py` file found within the `models` directory and executes them as subprocesses using the `execute_main` task.

# Future Developments

## Modelling
- Weighting models in the ensemble by some estimated weights (now it's just median ensemble)
- Calibration

## Evaluation
Decide on and implement online evaluation (offline and drift detection are implemented).

## Visualization
Some additional ideas for visualization data: https://docs.wandb.ai/guides/app/features/custom-charts/walkthrough, and https://docs.wandb.ai/guides/track/log/plots. Malika thinks linear plots might be easier to just make as we usually do and log them into wandb but they have some interesting built in things as well.

## Orchestration
Create VIEWS Prefect account with login details that team knows. Currently, Sara and Xiaolong are running on personal accounts.

