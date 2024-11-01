# Log Level Standards

| ADR Info            | Details           |
|---------------------|-------------------|
| Subject             | Logging Levels Configuration  |
| ADR Number          | 025   |
| Status              | Accepted  |
| Author              | Simon   |
| Date                | 30.10.2024.     |

## Context
We aim to establish a new benchmark in MLOps for early warning systems (EWS), emphasizing robust and transparent logging practices. The conflict forecasting pipeline must have a comprehensive logging strategy to support the continuous quality assurance, real-time monitoring, and rapid model updates critical for high-stakes decision-making and early action. This ADR specifically addresses the standardized use of log levels within the pipeline, which helps the team capture relevant system states and provides clear visibility into operations, potential issues, and crucial decision points across the pipeline.

The following log levels—DEBUG, INFO, WARNING, ERROR, and CRITICAL—are configured to ensure appropriate information is logged for various scenarios, supporting both ongoing development and long-term system monitoring and troubleshooting.


For related ADRs on the generation of different log files and other general logging standards/routines, please see the ADRs below:  [NOTE: new relevant ADRs links should be added]

- [009_log_file_for_generated_data](/documentation/ADRs/009_log_file_for_generated_data.md)

- [016_input_drift_detection_logging](/documentation/ADRs/016_input_drift_detection_logging.md)

- [017_log_files_for_offline_evaluation](/documentation/ADRs/017_log_files_for_offline_evaluation.md)

- [018_log_files_for_online_evaluation](/documentation/ADRs/018_log_files_for_online_evaluation.md)

- [019_log_files_for_model_training](/documentation/ADRs/019_log_files_for_model_training.md)

- [020_log_files_and_realtime_alerts](/documentation/ADRs/020_log_files_and_realtime_alerts.md)

- [026_log_files_for_input_data](/documentation/ADRs/026_log_files_for_input_data.md)


## Decision
The following log levels are implemented as standard for the conflict forecasting pipeline:

### Overview
The system’s log levels are structured as follows:

1. **DEBUG**: Provides detailed diagnostic information, primarily used during development and debugging.
2. **INFO**: Captures general system information about normal operations to give an overview without verbosity.
3. **WARNING**: Logs potentially problematic situations that require attention but do not yet impact execution.
4. **ERROR**: Indicates issues where specific processes fail but the overall system remains operational.
5. **CRITICAL**: Records severe errors that require immediate attention as they could lead to system failures or data loss.

### Examples and Use Cases

- **DEBUG**:
  - Example: Logging input data shapes, intermediate transformations, or model hyperparameters during experimentation phases.
  - Example: get_data.py provides the shape of data if exists when loading the data.
    - ` logger.debug(f"DataFrame shape: {data.shape if data is not None else 'None'}") `
  - Use: Essential for development and debugging stages, enabling the team to trace and diagnose precise pipeline states.

- **INFO**:
  - Example: Model training and evaluation start/completion times or successful data fetching messages.
  - Example: Information about which model is trained when training an ensemble model.
    - ` logger.info(f"Training single model {model_name}...") `
  - Use: Provides a clear history of system operations without overwhelming detail, facilitating audits and general status tracking.

- **WARNING**:
  - Example: Detection of minor schema mismatches in input data or slower-than-expected execution times.
  - Example: Warning arises when a queryset does not exist using the ModelPath class.
    - ` f"Queryset {self.queryset_path} does not exist. Continuing..." `
  - Use: Highlights potentially impactful issues that may worsen if not addressed, useful for preventive monitoring.

- **ERROR**:
  - Example: Failure in data loading or model saving or model artifact.
  - Example: Error arises when a model is run without specifying the run type.
    - ` f"Error: Run type is {args.run_type} but neither --train, --evaluate, nor --sweep flag is set. Nothing to do... Exiting." ` 
  - Use: Captures failures within components, supporting root cause analysis without interrupting the entire pipeline’s execution.

- **CRITICAL**:
  - Example: Data corruption detected during ingestion or a complete failure in the model orchestration module.
  - Use: Alerts the team to major issues demanding immediate intervention, ensuring prompt actions to mitigate risks.

## Consequences
Implementing this structured logging approach provides several benefits and potential drawbacks:

**Positive Effects:**
- **Improved Observability**: Each log level offers a distinct lens on system operations, enhancing real-time monitoring and troubleshooting capabilities.
- **Data-Driven Issue Resolution**: The logging structure supports continuous quality assurance by capturing detailed information, aiding root cause analysis and enabling proactive interventions.
- **MLOps Standardization**: This approach aligns with best practices in MLOps, facilitating future integrations, scaling, and consistent team understanding.

**Negative Effects:**
- **Increased Storage Use**: Higher log granularity, especially at DEBUG and INFO levels, may increase storage requirements.
- **Operational Overhead**: Maintenance of log file management, such as purging or archiving, may require periodic oversight, particularly with large volume logs like DEBUG.

## Rationale
The chosen logging levels reflect best practices in MLOps, which call for clearly defined, purposeful logging to maintain high observability and diagnostic precision within production environments. By setting granular logging levels, we are able to balance immediate operational needs with long-term maintenance, ensuring that the system remains adaptable to shifting conditions and that degraded performance can be preemptively managed.

### Considerations
Key considerations include:
- **Dependency Management**: Log retention and storage solutions must scale with the forecast pipeline, ensuring longevity without excessive operational costs.
- **Data Security**: Sensitive information should not be logged, especially at DEBUG or INFO levels, to maintain data protection standards.
- **Resource Constraints**: Frequent updates to logging configurations may impose operational overheads; thus, the current structure should be periodically reviewed but not frequently changed.

## Additional Notes
- **Log Rotation**: Log files are set up with TimedRotatingFileHandler to rotate daily, retaining a set number of logs per level (e.g., INFO logs for 30 days), which balances traceability and storage efficiency.
- **Future Enhancements**: Potential additions may include automated alerts for CRITICAL logs or integration with monitoring dashboards for centralized logging analysis.

## Feedback and Suggestions
Team members and stakeholders are encouraged to provide feedback on the logging configuration’s effectiveness, particularly regarding its impact on troubleshooting and operational transparency. Suggestions for improvement are welcome as we continue refining MLOps practices to support reliable, high-stakes forecasting.
