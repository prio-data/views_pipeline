# Log Files General Strategy 

| ADR Info            | Details                      |
|---------------------|------------------------------|
| Subject             | Log Files General Strategy   |
| ADR Number          | 015                          |
| Status              | Accepted                     |
| Author              | Simon                        |
| Date                | 28.10.2024                   |


## Context

Effective logging is essential for maintaining data integrity, monitoring model behavior, and troubleshooting issues within the model pipeline. A cohesive, centralized logging strategy ensures that logs are structured and accessible, enhancing transparency, auditability, and reliability across the model deployment lifecycle. The main goals of this logging strategy are to:

1. **Enable Reproducibility and Traceability**: Log details such as timestamps, script paths, and process IDs are standardized to help trace model behavior and system states effectively across different environments.
2. **Support Monitoring and Real-Time Alerts**: Logs will provide data for monitoring tools, enabling real-time alerting on critical errors and pipeline health checks.
3. **Align with MLOps Best Practices**: This strategy follows MLOps standards for consistent error handling, observability, scalability, and storage management, preparing the pipeline for scalable deployment and future monitoring enhancements.

For additional information, see also: 
- [009_log_file_for_generated_data.md](009_log_file_for_generated_data.md) 
- [016_log_files_for_input_data.md](016_log_files_for_input_data.md) 
- [017_log_files_for_offline_evaluation.md](017_log_files_for_offline_evaluation.md) 
- [018_log_files_for_online_evaluation.md](018_log_files_for_online_evaluation.md) 
- [019_log_files_for_model_training.md](019_log_files_for_model_training.md) 
- [020_log_files_realtime_alerts.md](020_log_files_realtime_alerts.md) 

## Decision

To implement a robust and unified logging strategy, we have decided on the following practices:

### Overview

1. **Standardized Log Configuration**: All logs will follow a centralized structure defined in the configurable `common_config/config_log.yaml` file. This configuration file controls logging levels, file rotation schedules, log output formats, and target log destinations. By centralizing log settings, all models within the pipeline will have a consistent logging structure, making the setup easier to maintain and adapt across environments.

2. **Daily Rotation and Retention Policy**: Logs will rotate daily, keeping the last 30 days of logs by default. This policy provides sufficient historical data for troubleshooting and auditing without excessive storage usage. Rotation is achieved using a `TimedRotatingFileHandler`, with daily timestamped log filenames for easy access.

3. **Log Separation by Level**: Logs are separated into `INFO`, `DEBUG`, and `ERROR` files and stored under `views_pipeline/common_logs`. This separation improves monitoring and helps maintain focus on the desired logging level when troubleshooting (e.g., reviewing only errors or detailed debugging information). Each log file will capture messages specific to its level, ensuring modularity and readability in logs.

4. **Inclusion of Path and Process Details**: Log messages include additional context such as script path (`%(pathname)s`), filename (`%(filename)s`), line number (`%(lineno)d`), process ID (`%(process)d`), and thread name (`%(threadName)s`). This information aids in tracing logs back to their source, supporting traceability and aiding debugging.

5. **Error Handling and Alerts**: Real-time alerting will be implemented for critical errors and unmet conditions. Integration with alerting tools (such as Slack or email) will provide immediate notifications of key pipeline issues. Alerts will include relevant metadata like timestamps, log level, and error specifics to support rapid troubleshooting.

6. **Dual Logging to Local Storage and Weights & Biases (W&B)**:
   - **Local Storage**: Logs will be stored locally on a rotating basis for easy access and immediate troubleshooting.
   - **Weights & Biases (W&B) Integration**: Model training and evaluation logs will also be sent to W&B, which allows for centralized logging of metrics, model performance tracking, and experiment comparison. The W&B integration supports MLOps best practices by making logs easily searchable, taggable (e.g., by model or pipeline stage), and accessible for experiment analysis and auditing.

7. **Access Control and Data Sensitivity**: Logs will avoid capturing sensitive data (such as configuration secrets or personally identifiable information) to align with data governance standards. While access controls for log files are not implemented at this stage, we may restrict log access in the future as the project scales, ensuring that sensitive log data is adequately protected.

8. **Testing and Validation**: Automated tests will validate that logs are created accurately and that rotation and level-specific separation operate as expected. These tests will cover:
   - Log creation and rotation validation.
   - Level-specific log file checks to confirm appropriate separation (e.g., that `INFO` logs do not include `DEBUG` messages).
   - Functional testing of real-time alerts to verify that notifications trigger as configured.

## Consequences

**Positive Effects:**
- Provides a consistent and structured logging framework, improving troubleshooting, auditability, and compliance.
- Supports MLOps best practices by establishing robust monitoring, traceability, and data governance standards.
- Facilitates scalability and onboarding by providing a standardized, centralized approach to logging across all pipeline models.

**Negative Effects:**
- Additional storage resources are required for log retention and rotation, and periodic monitoring of storage usage is needed.
- Initial setup and adjustment period may add complexity as team members adapt to the standardized logging and alerting practices.
- Some refactoring of the current codebase will be needed as this ADR is accepted.

## Rationale

The unified logging strategy aligns with MLOps best practices by combining flexibility, scalability, and robustness. This approach ensures that logging configurations are adaptable, reproducible, and traceable across the model pipeline. By establishing standardized configuration files and integrating alerting, this logging strategy proactively supports system monitoring and provides a foundation for future observability and security enhancements.

## Considerations

1. **Future Alerting Integrations**: Additional alerting tools, such as W&B alerts, Slack, and email notifications, will be incorporated as the project matures to ensure real-time visibility into pipeline states and failures.

2. **Centralized Logging Platform**: In future updates, the logging system may transition to a centralized platform (e.g., ELK Stack, Grafana) to improve scalability, visualization, and monitoring. This would require adjusting the current setup to work seamlessly with a logging infrastructure, which could involve additional configurations or external services.

3. **Access Control Expansion**: As the project scales, access control measures will be considered to ensure data protection. Log files should avoid sensitive information to comply with best practices in data governance and avoid potential data exposure risks.

4. **Testing Resource Allocation**: Implementing automated tests for logging mechanisms may require resources such as mock environments or testing frameworks to ensure the system functions as expected under different scenarios and that alert conditions trigger correctly.

## Additional Notes

Future updates may involve enhancing logging with a centralized platform, providing a more scalable and observable solution for monitoring and auditability. Access control measures and security protocols will also be revisited as the project scales to protect data integrity and confidentiality. Team members are encouraged to provide feedback on specific logging configuration details or suggest improvements to the alerting and monitoring system.

