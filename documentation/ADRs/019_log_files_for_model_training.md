# Log Files for Model Training


| ADR Info            | Details           |
|---------------------|-------------------|
| Subject             | Log Files for Model Training  |
| ADR Number          | 019   |
| Status              | Accepted   |
| Author              | Xiaolong |
| Date                | 29.10.2024 |

## Context
To ensure clarity and efficiency in monitoring the model training pipeline, it’s essential to adopt structured logging and alerting practices. The current pipeline generates logs during training execution, but these logs need to be more informative and concise. Therefore, we need to define standards around what to log, where to log, and how to log to enhance the readability and utility of logs.

For related ADRs on the generation of different log files and other general logging standards/routines, please see the ADRs below:  [NOTE: new relevant ADRs links should be added]

- [009_log_file_for_generated_data](/documentation/ADRs/009_log_file_for_generated_data.md)

- [015_log_files_general_strategy](/documentation/ADRs/015_log_files_general_strategy.md)

- [016_input_drift_detection_logging](/documentation/ADRs/016_input_drift_detection_logging.md)

- [017_log_files_for_offline_evaluation](/documentation/ADRs/017_log_files_for_offline_evaluation.md)

- [018_log_files_for_online_evaluation](/documentation/ADRs/018_log_files_for_online_evaluation.md)

- [019_log_files_for_model_training](/documentation/ADRs/019_log_files_for_model_training.md)

- [020_log_files_and_realtime_alerts](/documentation/ADRs/020_log_files_and_realtime_alerts.md)

- [025_log_level_standards](/documentation/ADRs/025_log_level_standards.md)

- [026_log_files_for_input_data](/documentation/ADRs/026_log_files_for_input_data.md)


## Decision
### Storage and Retention of Training Logs
All logs related to model training and validation will be stored both locally and centrally to ensure accessibility, durability, and ease of sharing.

**Local Storage**: Logs are generated at the terminal and stored in `.log` files locally for internal debugging and backup purposes. Local `.log` files are subject to a retention policy: they are kept until they reach a preset maximum size or number, as defined in the configuration. For more details on the general logging strategy, refer to [015_log_files_general_strategy](/documentation/ADRs/015_log_files_general_strategy.md).

**Centralized Storage**: All logs are also centralized using Weights & Biases (W&B) for real-time visualization, consistent tracking, and long-term sharing with collaborators. Logs stored on W&B are retained permanently for future reference and analysis.

Centralized logs enable sharing and visualization, while local storage ensures reliable debugging during network or platform issues, balancing observability, retention, and redundancy per MLOps best practices.

### Logging Content
To ensure comprehensive, transparent, and actionable logging during model training, we distinguish between two categories of information to be captured: **standard metrics** and **non-standard events**. Standard metrics provide continuous insight into training progress and model performance, while non-standard events record critical interruptions or anomalies. 

**Standard Metrics**: Standard metrics are essential for evaluating the effectiveness of the training process and ensuring reproducibility. These metrics will be logged to Weights & Biases (W&B) at configurable intervals (e.g., every N iterations or epochs) to balance real-time monitoring with performance overhead. Examples of metrics that will be logged:

- Training loss: Tracks optimization progress over time.
- Accuracy and validation metrics: Monitors model performance on unseen data.
- Epoch and batch information: Provides context for logged metrics and helps diagnose training issues.
- Hyperparameters: Captures key settings such as learning rate, optimizer type, and regularization parameters for reproducibility.

**Non-Standard Events**: To capture interruptions and anomalies, a dedicated `early_terminated` flag will be used in W&B. This flag will highlight deviations from expected training behavior and support real-time diagnostics. Flagged events will be documented with relevant context and, where applicable, trigger alerts or automated responses. These events include:

- Early Stopping: Triggered when validation performance does not improve for a predefined number of epochs.
- Diverging Loss: Flagged if the loss increases beyond a configurable threshold over consecutive iterations.
- Vanishing/Exploding Gradients: Detected through monitoring gradient magnitudes; anomalies are flagged if gradients fall below or exceed predefined thresholds.
- Other Anomalies: Includes runtime errors, hardware failures, or interruptions caused by resource constraints.

### Logging Levels
We will use the following logging levels in this project: `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`. Each level corresponds to a degree of severity, with `DEBUG` providing the most detailed information for developers and `CRITICAL` indicating the most severe issues. 

**Default**: The default logging level is set to `INFO`, meaning only messages at `INFO` or higher severity (`WARNING`, `ERROR`, `CRITICAL`) will be displayed in the terminal during execution. If at any point this needs changing the setting is handled here [config_log](/common_configs/config_log.yaml)

**Local storage**: All logging messages, regardless of level, are stored locally. This ensures comprehensive records are available for debugging and post-analysis, even if not displayed in real time.

**`DEBUG` level**: Although DEBUG messages are not shown in the terminal by default, they provide detailed internal state information and can be enabled for development and troubleshooting purposes.

Below are specific examples for each level that is logged:

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
Currently `CRITICAL` hasn't been used, but usually it means major data issues or catastrophic failure during training which requires immediate attention.

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
