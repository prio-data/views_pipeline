# Log file for generated data


| ADR Info            | Details                     |
|---------------------|-----------------------------|
| Subject             | Log File for Generated Data |
| ADR Number          | 009                         |
| Status              | Accepted                    |
| Author              | Xiaolong                    |
| Date                | 09.09.2024                  |

## Context
In the context of the VIEWS pipeline, there is a need to create a log file to ensure that models and data are tracked accurately and meet certain criteria before running. 
These log file, used as metadata for deployment and orchestration,  will provide a detailed record of the data generation process, including the model artifact, the generated data, and the input raw data. 
This is critical to ensure the reliability and reproducibility of model outputs and to prevent outdated or incorrect data from being used in production systems.

For related ADRs on the generation of different log files and other general logging standards/routines, please see the ADRs below:  [NOTE: new relevant ADRs links should be added]

- [016_input_drift_detection_logging](/documentation/ADRs/016_input_drift_detection_logging.md)

- [017_log_files_for_offline_evaluation](/documentation/ADRs/017_log_files_for_offline_evaluation.md)

- [018_log_files_for_online_evaluation](/documentation/ADRs/018_log_files_for_online_evaluation.md)

- [019_log_files_for_model_training](/documentation/ADRs/019_log_files_for_model_training.md)

- [020_log_files_and_realtime_alerts](/documentation/ADRs/020_log_files_and_realtime_alerts.md)

- [025_log_level_standards](/documentation/ADRs/025_log_level_standards.md)

- [026_log_files_for_input_data](/documentation/ADRs/026_log_files_for_input_data.md)


## Decision
This decision involves implementing a logging system for all generated data and enforce ensemble model checks. 
This logging will involve creating a **.txt** log file in each model-specific folder. The log file will contain the following details:
- The name and timestamp of the model artifact that produced the data.
- The timestamp of when the data was generated.
- Possibly the data stamp of when the raw data used was fetched from VIEWS.
- The deployment status of the single model.

Additionally, ensemble models will enforce a set of preconditions before running:
- The model artifact used must be trained within the current year (after July).
- The generated data must be from the current month.
- The raw data must also have been fetched in the current month.

In the deployment, when one tries to run an ensemble model, a model check must be passed before executing evaluation or forecatsing. 
If any of these conditions are not met, the pipeline will automatically shut down and output a clear and verbose warning, detailing where the issue occurred.

## Consequences
**Positive Effects:**
- Improved traceability of generated data, which is essential for debugging, auditing, and reproducing results.
- Ensures models and data used in production are up-to-date and relevant, reducing the risk of using outdated or irrelevant information.
- Automatic shutdown of models that don’t meet the criteria prevents orchestration from becoming a waste of time.

**Negative Effects:**
- Additional efforts on maintaining logs and verifying the conditions of models and data may increase the complexity of the system.

## Rationale
The rationale behind this decision stems from the need for traceability and ensuring data integrity. 
Tracking the model artifacts and their corresponding data ensures that each output can be reproduced. 
Furthermore, enforcing time-based checks for models and data helps ensure that outdated information is not used, 
which could negatively impact predictions.

### Considerations
- The conditions for model and data checks need to be clearly defined and communicated to all team members.
- The implementation of these checks may require coordination with the development team to ensure compatibility.