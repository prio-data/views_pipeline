# Artifact Naming Convention


| ADR Info            | Details                    |
|---------------------|----------------------------|
| Subject             | Artifact Naming Convention |
| ADR Number          | 012                        |
| Status              | Accepted                   |
| Author              | Xiaolong                   |
| Date                | 11.09.2024                 |

## Context
In the context of the VIEWS pipeline, a standardized naming convention is required to ensure consistency, traceability, and clarity. 
This is particularly important for managing prediction versions, tracking when predictions were generated, and easily identifying which model artifact and dataset were used to create the predictions.

## Decision
The naming convention for a single model artifact will follow this structure:
```
<run_type>_model_<timestamp>.pkl
```
- run_type: The type of run (e.g., calibration, testing, forecasting).
- timestamp: The timestamp when the model was trained. The format is`YYYYMMDD_HHMMSS`.

Training is not an option for ensemble models right now as they are made by aggregating single models. So no decision has been made on the naming convention for ensemble models yet.

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

- Each file name is unique and informative, allowing easy identification of the model, data version, and time of creation without needing to open the file.
- Including the timestamp makes it easy to log files for generated data (see ADR 009).
- This structure is easy to parse by both humans and automated systems, improving workflow integration and automation.

### Considerations
- **Timestamp Format**: Using `YYYYMMDD_HHMMSS aligns with standard formats but could introduce issues in systems operating across different time zones.
- **Model timstamp vs. Prediction timestamp**: The decision hasn't been made yet on whether the prediction timestamp should be the time the prediction was generated or the time the model was trained. This will be discussed further.
