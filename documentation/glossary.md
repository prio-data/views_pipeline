# Glossary

| Info         | Details  |
|--------------|----------|
| Last updated | 30 .07.2024 |
| By author    | Simon    |


## Key Technical Terms

### Config File
Config files specify the settings and hyperparameters used to train machine learning models, allowing for easy experimentation and optimization without modifying the code – i.e., you don't want to hard code (i.e., write directly) hyperparameters into your model code.

### Orchestration
The Prefect Flow coordinates the execution of tasks, ensuring that they are executed in the correct order based on their dependencies.

### Hyperparameters
Hyperparameters are parameters or settings that are not directly learned from data during the training process of a machine learning model, but rather are set prior to training and influence the behavior and performance of the model. For example, hyperparameters could include the learning rate, number of estimators, number of jobs, and transformation of data.

For more information, see the [Weights & Biases article "Intro to MLOps: Hyperparameter Tuning"](https://wandb.ai/site/articles/intro-to-mlops-hyperparameter-tuning).

### Prefect
Prefect is used for workflow orchestration, defining the sequence of tasks (task1, task2, task3) and their dependencies.

See the Quickstart guide [here](https://docs.prefect.io/latest/getting-started/quickstart/).

### Sweep
A sweep configuration is a set of specifications defining how hyperparameters should be explored during a hyperparameter search, the hyperparameters to be tuned, and their respective ranges or values to be tried. 

### Weights & Biases (wandb)
Weights & Biases (W&B) is used to log relevant information (such as data, transformations, and results) produced by each task during the execution of the workflow. W&B logging within each task enables tracking and monitoring of the workflow's progress and outputs, enhancing visibility and reproducibility.

See the Quickstart guide [here](https://docs.wandb.ai/quickstart).

### Utils/Utility Functions
Collection of functions or tools that serve various general purposes and are commonly reused across different parts of a software project. These utility functions are often not specific to any particular domain or task but rather provide common functionalities that can be helpful in many different situations.

## Key Forecasting Terms

### forecast_step
- **Definition**: The time increment at which predictions are made in a time series, reflecting the data's frequency (e.g., daily, monthly, yearly).
- **Example**: Forecasting 36 months into the future involves steps {0,1,2,…,35}, where step 0 represents the first forecasted period immediately following the last observed data point.

### month_id
- **Definition**: A unique identifier assigned to each month in a time series, starting from the initial observation period and continuing sequentially.
- **Example**: January 1980 is month_id 1, February 1980 is month_id 2, and so on. If the last observed month is December 2020 (month_id 492), January 2021 is month_id 493.

### year
- **Definition**: The actual calendar year in which a data point or forecast occurs.
- **Example**: 1980, 2021, etc.

### forecast_start
- **Definition**: The temporal identifier marking the beginning of the forecast period.
- **Example**: If the last observed month is December 2020 (month_id 492), January 2021 (month_id 493) marks the forecast_start.

### forecast_end
- **Definition**: The temporal identifier marking the end of the forecast period.
- **Example**: If the forecast begins in January 2021 (month_id 493) and spans 36 months, the forecast_end would be December 2023 (month_id 528).

### forecast_horizon
- **Definition**: The total duration into the future for which predictions are made, measured in the same units as the time series data.
- **Example**: A forecast horizon of 36 months indicates predictions are made for the next 36 months following the forecast_start.

### forecast_lead_time
- **Definition**: The duration between when a forecast is made and when the predicted event occurs.
- **Example**: A forecast made in January 2021 for the month of March 2021 has a forecast lead time of 2 months.

## Model Terminology

### 1. Recursive Multi-Step Forecasting
- **Definition**: A single model trained to predict one step ahead, used iteratively to forecast multiple future steps.
- **Example**: Predicting conflict incidents in grid cell months for the next 36 months by using each forecasted value as an input for the next prediction.
- **Algorithms**:
    - Linear Regression
    - Random Forests
    - Gradient Boosting Machines (e.g., XGBoost, LightGBM)
    - Multilayer Perceptrons (MLPs)
- **Notes**:
    - Utilizes conventional Supervised Machine Learning models.
    - Involves adding lagged features to input data to learn temporal dependencies.

### 2. Direct Multi-Step Forecasting (STEPSHIFTER IN VIEWS TERMS)
- **Definition**: Separate (sub) models trained for each forecasting horizon to predict specific future time steps directly.
- **Example**: Training distinct (sub) models to predict conflict incidents 1 month ahead, 2 months ahead, up to 36 months ahead.
- **Algorithms**:
    - Linear Regression
    - Random Forests
    - Gradient Boosting Machines (e.g., XGBoost, LightGBM)
    - Multilayer Perceptrons (MLPs)
- **Notes**:
  - Also utilizes conventional Supervised Machine Learning models but avoids error accumulation seen in recursive forecasting.
  - Requires more computational resources then Recursice Multi-Step Forecasting as multiple (sub) models are trained.

### 3. Autoregressive Model (AR)
- **Definition**: A linear model regressing the current value of a time series on its previous values, using a predefined number of lagged observations.
- **Example**: Using the last five months of conflict data to predict the current month's conflict level.
- **Algorithms**:
    - ARMA (Autoregressive Moving Average)
    - ARIMA (Autoregressive Integrated Moving Average)
    - SARIMA (Seasonal ARIMA)
- **Notes**:
  - Specialized Time Series Models effective for stationary series with linear relationships.

### 4. Multi-Output Models
- **Definition**: Models trained to predict multiple future values at once, producing a sequence of future predictions in a single step.
- **Example**: Using a Seq2Seq transformer or LSTM U-net to forecast conflict incidents for the next 36 months.
- **Algorithms**:
    - Seq2Seq Models (Sequence-to-Sequence)
    - Recurrent Neural Networks (RNNs) - Includes LSTM (Long Short-Term Memory) and GRU (Gated Recurrent Units) networks.
    - Transformer Models
- **Notes**:
    - Suitable for complex, non-linear relationships.
    - Can handle long sequences effectively.

### Summary Table for Model Terminology

| **Method**              | **Definition**      | **Algorithms** |**Notes**  |
|-------------------------|---------------------|----------------|-----------|
| **Recursive Multi-Step**       | Single model predicts one step ahead, used iteratively for multiple steps    | Linear Regression, Random Forests, Gradient Boosting (XGBoost, LightGBM), MLPs      | Uses lagged features to learn temporal dependencies  |
| **Direct Multi-Step (stepshift)**          | Separate models trained for each forecasting horizon  | Separate Linear Regression, Gradient Boosting, MLPs                                   | Avoids error accumulation; requires more computational resources   |
| **Autoregressive (AR)**        | Linear model regressing current value on previous values  | ARMA, ARIMA, SARIMA  | Effective for stationary series with linear relationships                                               |
| **Multi-Output Models**        | Models trained to predict multiple future values at once | Seq2Seq, RNNs (LSTM, GRU), Transformers| Suitable for complex, non-linear relationships; handles long sequences effectively                       |