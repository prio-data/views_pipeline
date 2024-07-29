# Glossary

| Info         | Details  |
|--------------|----------|
| Last updated | 29.07.2024 |
| By author    | Simon    |

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
  - **Linear Models**: Linear Regression
  - **Tree-Based Models**: Decision Trees, Random Forests
  - **Ensemble Methods**: Gradient Boosting Machines (e.g., XGBoost, LightGBM)
  - **Neural Networks**: Multilayer Perceptrons (MLPs)
- **Notes**:
  - Utilizes conventional Supervised Machine Learning models.
  - Involves adding lagged features to input data to learn temporal dependencies.

### 2. Direct Multi-Step Forecasting (ALSO KNOWN AS STEPSHIFT IN VIEWS TERMS)
- **Definition**: Separate models trained for each forecasting horizon to predict specific future time steps directly.
- **Example**: Training distinct models to predict conflict incidents 1 month ahead, 2 months ahead, up to 36 months ahead.
- **Algorithms**:
  - **Linear Models**: Separate Linear Regression models for each step
  - **Tree-Based Models**: Separate Decision Trees for each step
  - **Ensemble Methods**: Separate Gradient Boosting models for each step
  - **Neural Networks**: Separate MLPs for each step
- **Notes**:
  - Avoids error accumulation seen in recursive forecasting.
  - Requires more computational resources as multiple models are trained.

### 3. Autoregressive Model (AR)
- **Definition**: A linear model regressing the current value of a time series on its previous values, using a predefined number of lagged observations.
- **Example**: Using the last five months of conflict data to predict the current month's conflict level.
- **Algorithms**:
  - **AR (Autoregressive)**: Uses past values to predict current values.
  - **ARMA (Autoregressive Moving Average)**: Combines AR with a Moving Average model.
  - **ARIMA (Autoregressive Integrated Moving Average)**: Includes differencing to make the series stationary.
  - **SARIMA (Seasonal ARIMA)**: Adds seasonal components to ARIMA for handling seasonality.
- **Notes**:
  - Specialized Time Series Models effective for stationary series with linear relationships.

### 4. Multi-Output Models
- **Definition**: Models trained to predict multiple future values at once, producing a sequence of future predictions in a single step.
- **Example**: Using a Seq2Seq transformer or LSTM U-net to forecast conflict incidents for the next 36 months.
- **Algorithms**:
  - **Seq2Seq Models (Sequence-to-Sequence)**: Effective for multi-step forecasting.
  - **Recurrent Neural Networks (RNNs)**: Includes LSTM (Long Short-Term Memory) and GRU (Gated Recurrent Units) networks.
  - **Transformer Models**: Use self-attention mechanisms for long-range dependencies.
  - **LSTM U-net**: Combines LSTM networks with U-net architectures for spatial-temporal data.
- **Notes**:
  - Suitable for complex, non-linear relationships.
  - Can handle long sequences effectively.

### Summary Table for Model Terminology

| **Method**                     | **Definition**                                                               | **Example**                                      | **Algorithms**                                                                                      | **Notes**                                                                                               |
|--------------------------------|-------------------------------------------------------------------------------|--------------------------------------------------|------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| **Recursive Multi-Step**       | Single model predicts one step ahead, used iteratively for multiple steps     | Predicting conflict incidents for 36 months      | Linear Regression, Decision Trees, Random Forests, Gradient Boosting (XGBoost, LightGBM), MLPs      | Uses lagged features to learn temporal dependencies                                                     |
| **Direct Multi-Step (stepshift)**          | Separate models trained for each forecasting horizon                          | Training models for 1 to 36 months ahead         | Separate Linear Regression, Decision Trees, Gradient Boosting, MLPs                                   | Avoids error accumulation; requires more computational resources                                        |
| **Autoregressive (AR)**        | Linear model regressing current value on previous values                      | Predicting current month's conflict level        | AR, ARMA, ARIMA, SARIMA                                                                               | Effective for stationary series with linear relationships                                               |
| **Multi-Output Models**        | Models trained to predict multiple future values at once                      | Seq2Seq transformer or LSTM U-net for 36 months  | Seq2Seq, RNNs (LSTM, GRU), Transformer, LSTM U-net                                                   | Suitable for complex, non-linear relationships; handles long sequences effectively                       |