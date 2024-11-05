# Log Files for Model Training


| ADR Info            | Details           |
|---------------------|-------------------|
| Subject             | Log Files for Model Training  |
| ADR Number          | 019   |
| Status              | Proposed   |
| Author              | Xiaolong |
| Date                | 29.10.2024 |

## Context
To ensure clarity and efficiency in monitoring the model training pipeline, it’s essential to adopt structured logging and alerting practices. The current pipeline generates logs during training execution, but these logs need to be more informative and concise. Therefore, we need to define standards around what to log, where to log, and how to log to enhance the readability and utility of logs.

For related ADRs on the generation of different log files and other general logging standards/routines, please see the ADRs below:  [NOTE: new relevant ADRs links should be added]

- [009_log_file_for_generated_data](/documentation/ADRs/009_log_file_for_generated_data.md)

- [016_input_drift_detection_logging](/documentation/ADRs/016_input_drift_detection_logging.md)

- [017_log_files_for_offline_evaluation](/documentation/ADRs/017_log_files_for_offline_evaluation.md)

- [018_log_files_for_online_evaluation](/documentation/ADRs/018_log_files_for_online_evaluation.md)

- [019_log_files_for_model_training](/documentation/ADRs/019_log_files_for_model_training.md)

- [020_log_files_and_realtime_alerts](/documentation/ADRs/020_log_files_and_realtime_alerts.md)

- [025_log_level_standards](/documentation/ADRs/025_log_level_standards.md)

- [026_log_files_for_input_data](/documentation/ADRs/026_log_files_for_input_data.md)


## Decision
### Logging Content
- Standard training metrics on W&B, including  training loss, accuracy, epochs, batch size, hyperparameters, etc.
- Non-standard events -- use `early_terminated` flag on W&B
  - Early stopping
  - Diverging loss
  - Vanishing and exploding gradients
  - Other anomalies

### Logging Levels
The logging levels we set in this project are `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`. The default level is `INFO`, meaning that only levels above will be logged. Below are specific examples for each level that is logged:

#### 1. INFO
```
logger.info(f"Training model {config['name']}...")
```
At this level logging is used for standard training progress updates.

#### 2. WARNING
```
logger.warning(f"DataFrame contains non-np.float64 numeric columns. Converting the following columns: {', '.join(non_float64_cols)}")
```
At this level logging is used for minor issues like degraded performance in intermediate steps.

#### 3. ERROR
```
logger.error(f"Early stopping at epoch {epoch+1} due to lack of improvement.")

wandb.log({"early_terminated": True})
```
At this level logging is used for training stalls, failed checkpoints, or early stops.

#### 4. CRITICAL
Currently `CRITICAL` hasn't been used, but usually it means major data issues or catastrophic failure requiring immediate attention.


### Storage and Distribution:
The logs are generated at the terminal, in the `.log` file, and on W&B to ensure both internal accessibility and external sharing. Logs on W&B are permanently kept, while the `.log` files are kept until reaching the preset maximum amount .

### Integration with Alerting and Notification
A real-time alert and notification system will be implemented. Please refer to the related ADR [020_log_files_and_realtime_alerts](/documentation/ADRs/020_log_files_and_realtime_alerts.md).

## Consequences

**Positive Effects:**
- Informative logs provide detailed insights into model performance, resource utilization, and pipeline behavior.
- Automated alerts for critical errors or unusual behavior reduce manual monitoring efforts.
- Clear and informative logs create a common understanding of pipeline operations.

**Negative Effects:**
- Designing and setting up standardized logging and alerting practices can be complex, especially when integrating with external logging and alerting tools.
- Logs may contain sensitive information (e.g., model data, configurations) that could pose privacy or security risks if not managed properly.

## Rationale
- Structured logging and alerts improve monitoring and understanding of model training.
- Logs standard metrics and non-standard events (e.g., early stopping, anomalies) on W&B for comprehensive monitoring.
- Logs available in terminal, `.log` files, and on W&B, ensuring easy access and external sharing.
- Real-time alert system enables quick responses to critical issues, minimizing downtime.

### Considerations
- `INFO` as the default level balances detail with readability, and other levels should be used to avoid excessive verbosity.
- W&B retains logs permanently, while `.log` files are rotated and ensures storage is not overloaded.


## Feedback and Suggestions
Feedbacks and suggestions are welcomed.
