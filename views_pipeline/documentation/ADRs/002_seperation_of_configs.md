# Model Configuration Structure Reference Document

|ADR Info| Details|
|--------------|-----------|
| Subject      | Config File Structure|
| ADR Number   | 002       |
| Status       | Accepted  |
| Author       | Simon     |
| Date         | 29.07.2024|

## Context

The project's previous configuration management approach, utilizing a single config_model file, was found to be cumbersome and unclear, hindering operational efficiency and maintainability. There was a need to clarify and optimize the configuration structure to improve system architecture and ease future modifications.

## Decision

The decision was made to restructure the model configuration into distinct files, each tailored to specific functionalities aligned with the model's lifecycle stages—training, deployment, and documentation. This involves splitting the previous config_model into several targeted configuration files (see below).

### Configuration Files Overview

Here is a detailed table describing the new configuration files and their respective purposes:

| Configuration File                        | Type            | Description                                                                                             |
|-------------------------------------------|-----------------|---------------------------------------------------------------------------------------------------------|
| **config_hyperparameters.py**           | Operational     | Defines hyperparameters that influence the training process of the model.                              |
| **config_sweep.py**                     | Operational     | Specifies methods for conducting hyperparameter sweeps to optimize model performance.                   |
| **config_deployment.py**                | Behavioral      | Manages settings for model deployment across various environments, affecting runtime behavior.          |
| **config_inputdata.py**                 | Behavioral      | Configures the input data specifications using a viewer queryset format.                               |
| **config_meta.py**                      | Documentation   | Contains metadata about the model, such as the algorithm used and the identity of the creator.          |


## Consequences
**Positive Effects:**
- Improved clarity and maintainability of the configuration files.
- Enhanced ability for new developers to understand the system's architecture.
- Streamlined updates and modifications to model behavior without extensive system-wide impacts.

**Negative Effects:**
- Initial overhead of transitioning to a new configuration structure.
- Potential for initial confusion or errors as developers adjust to the new file distribution.

## Rationale

The division of the configuration into specific files is designed to:

- **Operational Configurations:** Operational configurations consist of parameters that directly affect model training and evaluation. Changes to these settings, such as learning rate, number of training epochs, and model-specific hyperparameters, will alter the model's behavior, impacting how it processes and learns from training data.

- **Behavioral Configurations:** Behavioral configurations include parameters that influence the model's deployment and runtime behavior. Modifying these settings affects how the model processes input data, integrates with other systems, and manages operations in real time. This category is critical for the model's adaptation to its operational environment and includes settings for data preprocessing, deployment strategies, and runtime management. It's important to note that changes here may require additional modifications to the model's source code; simply adjusting these configurations does not guarantee correct behavior without considering the specific model type and implementation.

- **Documentation Configurations:** Documentation configurations contain purely informational metadata about the model. Modifying these parameters does not impact the model’s training, behavior, or deployment. They are crucial for documentation purposes, aiding in compliance and maintenance, and include details such as the model’s architecture, purpose, and version.



### Considerations

- **Centralization vs. Duplication:** To avoid redundancy, certain information from the documentation configurations, such as levels in config_meta.py, could be used for orchestration. Changes in these settings should not impact model behavior but are crucial for ensuring that documentation influences operational decisions appropriately.

- **Error Handling:** Any modifications in documentation settings that do not align with the model’s operational parameters should generate informative error messages.

## Additional Notes

- **Partition Configurations:** While some current models use a local partition_config, we want to use set_partition from common_utils as a standard approach. This method can be adapted to accommodate unique needs in exceptional cases.
- **Integration of Querysets:** As part of the restructuring, the queryset integration has been moved to config_inputdata.py to streamline data handling processes.

## Feedback and Suggestions

Please share your insights and suggestions to further refine our model configuration strategy. Feedback on the integration of documentation configurations in operational contexts and other areas of concern is particularly valuable.
