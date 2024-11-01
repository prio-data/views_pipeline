# Input Drift Detection Logging


| ADR Info            | Details                       |
|---------------------|-------------------------------|
| Subject             | Input Drift Detection Logging |
| ADR Number          | 016                           |
| Status              | Accepted                      |
| Author              | Jim Dale                      |
| Date                | 28/10/2014                    |

## Context
An input drift detection system has been implemented as part of the viewser data-fetching package. Its purpose is to check the integrity of input data presented to the models to guard against undetected problems when the data was ingested into the VIEWS database. The drift detector splits a dataset up into a test portion consisting of the latest n months of data, and a standard portion consisting of the m months of data before the first month in the test portion. Usually, n would be 1 and m might be 30. Users may then specify a range of tests which compare the data in the test and standard portions, e.g. does the fraction of missingness or zeros change by more than some threshold, is the probability that the data in the portions is drawn from different distributions greater than some threshold? Thresholds for each test are defined in a configuration dictionary and an alert is issued for features or whole datasets that fail a test. The issue is, how should the pipeline deal with the alerts?

For related ADRs on the generation of different log files and other general logging standards/routines, please see the ADRs below:  [NOTE: new relevant ADRs links should be added]

- [009_log_file_for_generated_data](/documentation/ADRs/009_log_file_for_generated_data.md)

- [017_log_files_for_offline_evaluation](/documentation/ADRs/017_log_files_for_offline_evaluation.md)

- [018_log_files_for_online_evaluation](/documentation/ADRs/018_log_files_for_online_evaluation.md)

- [019_log_files_for_model_training](/documentation/ADRs/019_log_files_for_model_training.md)

- [020_log_files_and_realtime_alerts](/documentation/ADRs/020_log_files_and_realtime_alerts.md)

- [025_log_level_standards](/documentation/ADRs/025_log_level_standards.md)

- [026_log_files_for_input_data](/documentation/ADRs/026_log_files_for_input_data.md)


## Decision
- For every queryset fetched, drift detection will be enabled. 
- Logging is done in the get_data.py routine for each model where the data fetch is executed. 
- Different sets of detectors and thresholds will be defined for the train, test and future partitions. 
- Alerts will be logged to wandb, with each queryset fetch being a separate run, and to a local .txt file. 
- Each alert will be regarded as a warning and will consist of: a timestamp, a WARNING, the model name, the offending feature name (where appropriate), the chosen threshold and the severity.
- For one datafetch per run, the drift-detector's self-test machinery will be enabled, which will log a simple success message to wandb and a local text file, or terminate pipeline execution.

### Overview
Every model in the pipeline (at present) has an input dataset retrieved via viewser. Drift detection will be enabled for every dataset, since such datasets may be very different, and ingestion failures/issues will likely affect some datasets but not others. For at most one data fetch, the drift-detection system's self-test mechanism will be enabled. This fetches a single, simple queryset, perturbs it in ways designed to trigger the drift detectors and checks that they are in fact triggered. If any of them are not, this is regarded as a fatal error indicating that the drift-detection system itself is not working, and execution of the entire pipeline is terminated. Otherwise, a short text is printed confirming that the self-test has been passed. 

## Consequences

**Positive Effects:**
- Enabling drift-logging for every queryset fetch means that every feature used in the pipeline is tested as a matter of course
- Logging to wandb and local text files means that any team-member can access the drift-detection logs at any time
- Allowing different drift detection configurations for each partition enables the drift-detection system to be tuned to issues specific to each partition. The training and test partitions use data which is old and in principle well established, so any issues that occur are likely to be gross database corruption or transformation malfunction issues affecting the whole dataset, so global tests (e.g global missingness) are appropriate. Conversely, the future partition includes the very latest data, so tests which compare the most recent month to a set of previous months are appropriate, to detect issues such as unannounced changes to source data APIs. 

**Negative Effects:**
- Each model run consists of two wandb runs - one for the data fetch, one for the training. Since the runs have no naming conventions, it is not obvious which data-fetch run belongs to which training run.
- Every model's get_data and execute_model_runs script need to be modified, because the logging to wandb needs to be passed the project, which is generated in execute_model_runs

## Rationale
- wandb is the logical location to keep central logs. 
- Fetching of data is a separate task from training a model, with unique potential problems that should be logged separately from output generated while training. This is all the more so during a sweep.
- Every queryset is potentially different, so drift-detection must be done on each one (and therefore for every model) separately. 
- Self-testing, conversely, need only be done once per run of the whole pipeline.

### Considerations
None

## Additional Notes
None

## Feedback and Suggestions
Feedback is welcomed.