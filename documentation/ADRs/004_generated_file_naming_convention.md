# Generated File Naming Convention


| ADR Info            | Details                          |
|---------------------|----------------------------------|
| Subject             | Generated file naming convention |
| ADR Number          | 004                              |
| Status              | Accepted                         |
| Author              | Xiaolong                         |
| Date                | 11.09.2024                       |

## Context
In the context of the VIEWS pipeline, a standardized naming convention is required to ensure consistency, traceability, and clarity. 
This is particularly important for managing prediction versions, tracking when predictions were generated, and easily identifying which model artifact and dataset were used to create the predictions.


## Decision
### 1. Prediction naming convention
The prediction naming convention for using a single model will follow this structure:
```
prediction_<max_forecast_step>_<timestamp>.pkl
```
- max_forecast_step: The maximum forecast step for the prediction.
- run_type: The type of run (e.g., calibration, testing, forecasting).
- timestamp: The timestamp when the model was trained **(not when the prediction was generated)**. The format is`YYYYMMDD_HHMMSS`.

The prediction naming convention for using an ensemble model will follow this structure **(needs further discussion)**:
```
prediction_<max_forecast_step>_<model_name_1><timestamp_1>_<model_name2><timestamp_2>.pkl
```
- max_forecast_step: The maximum forecast step for the prediction.
- model_name: The name of the model used for the ensemble prediction.
- timestamp: The timestamp when the model was trained. The format is`YYYYMMDD_HHMMSS`.

### 2. Artifact naming convention (not model naming convention)
The naming convention for a **single** model artifact will follow this structure:
```
<run_type>_model_<timestamp>.pkl
```
- run_type: The type of run (e.g., calibration, testing, forecasting).
- timestamp: The timestamp when the model was trained. The format is`YYYYMMDD_HHMMSS`.


### 3. Evaluation/Output naming convention
The evaluation/output naming convention for using a single model will follow this structure:
```
<evaluation/output>_<max_forecast_step>_<run_type>_<timestamp>.pkl
```
- max_forecast_step: The maximum forecast step for the prediction.
- run_type: The type of run (e.g., calibration, testing).
- timestamp: The timestamp when the model was trained. The format is`YYYYMMDD_HHMMSS`.

The evaluation naming convention for using an ensemble model will follow this structure:
```
<evaluation/output>_<max_forecast_step>_<run_type>_<model_name_1><timestamp_1>_<model_name2><timestamp_2>.pkl
```
- max_forecast_step: The maximum forecast step for the prediction.
- run_type: The type of run (e.g., calibration, testing).
- model_name: The name of the model used for the ensemble prediction.
- timestamp: The timestamp when the model was trained. The format is`YYYYMMDD_HHMMSS`.

## Consequences
**Positive Effects:**

- **Easier File Management**: Simplifies handling of prediction files, especially when dealing with multiple models or datasets.
- **Improved Traceability**: Facilitates identification of which model produces the prediction/ output/ evaluation.
- **Enhanced Automation**: Enables smooth automation of tasks like archiving or fetching the latest predictions, as the timestamp provides a clear indicator of file recency.


**Negative Effects:**
- **Longer File Names**: Could be cumbersome in environments where shorter names are preferred.
- **Adjustment Required**: Existing scripts or systems may need updates to accommodate the new naming structure.

## Rationale
The decision to use this naming convention ensures that:

- Each file name is unique and informative, allowing easy identification of the model, data version, type of prediction, and time of creation without needing to open the file.
- Including the timestamp makes it easy to log files for generated data (see ADR 009).
- Including the timestamp also helps distinguish between multiple runs of the same model, ensuring that no prediction is accidentally overwritten.
- This structure is easy to parse by both humans and automated systems, improving workflow integration and automation.

### Considerations
- **Timestamp Format**: Using `YYYYMMDD_HHMMSS aligns with standard formats but could introduce issues in systems operating across different time zones.
- **Model timstamp vs. Prediction timestamp**: The decision hasn't been made yet on whether the prediction timestamp should be the time the prediction was generated or the time the model was trained. This will be discussed further.
