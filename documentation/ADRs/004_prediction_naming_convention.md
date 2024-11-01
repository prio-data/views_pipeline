# Prediction Naming Convention


| ADR Info            | Details                      |
|---------------------|------------------------------|
| Subject             | Prediction Naming Convention |
| ADR Number          | 004                          |
| Status              | Accepted                     |
| Author              | Xiaolong                     |
| Date                | 11.09.2024                   |

## Context
In the context of the VIEWS pipeline, a standardized naming convention is required to ensure consistency, traceability, and clarity. 
This is particularly important for managing prediction versions, tracking when predictions were generated, and easily identifying which model artifact and dataset were used to create the predictions.


## Decision
The prediction naming convention for using a single model will follow this structure:
```
prediction_<max_forecast_step>_forecasting_<timestamp>.pkl
```
- max_forecast_step: The maximum forecast step for the prediction.
- timestamp: The timestamp when the model was trained **(not when the prediction was generated)**. The format is`YYYYMMDD_HHMMSS`.

The prediction naming convention for using an ensemble model will follow this structure **(needs further discussion)**:
```
prediction_<max_forecast_step>_forecasting_<model_name_1><timestamp_1>_<model_name2><timestamp_2>.pkl
```
- max_forecast_step: The maximum forecast step for the prediction.
- model_name: The name of the model used for the ensemble prediction.
- timestamp: The timestamp when the model was trained. The format is`YYYYMMDD_HHMMSS`.

## Consequences
**Positive Effects:**

- **Easier File Management**: Simplifies handling of prediction files, especially when dealing with multiple models or datasets.
- **Improved Traceability**: Facilitates identification of which model produces the prediction.
- **Enhanced Automation**: Enables smooth automation of tasks like archiving or fetching the latest predictions, as the timestamp provides a clear indicator of file recency.


**Negative Effects:**
- **Longer File Names**: Could be cumbersome in environments where shorter names are preferred.
- **Adjustment Required**: Existing scripts or systems may need updates to accommodate the new naming structure.

## Rationale
The decision to use this naming convention ensures that:

- Each file name is unique and informative, allowing easy identification of time of creation without needing to open the file.
- Including the timestamp makes it easy to log files for generated data (see ADR 009).
- Including the timestamp also helps distinguish between multiple runs of the same model, ensuring that no prediction is accidentally overwritten.
- This structure is easy to parse by both humans and automated systems, improving workflow integration and automation.

### Considerations
- **Timestamp Format**: Using `YYYYMMDD_HHMMSS aligns with standard formats but could introduce issues in systems operating across different time zones.
- **Model timstamp vs. Prediction timestamp**: The decision hasn't been made yet on whether the prediction timestamp should be the time the prediction was generated or the time the model was trained. This will be discussed further.
