
# Documentation of Models in VIEWS Pipeline

| ADR Info            | Details                                      |
|---------------------|----------------------------------------------|
| Subject             | Documentation of Models in VIEWS Pipeline    |
| ADR Number          | 005                                          |
| Status              | Accepted                                     |
| Author              | Sara and Simon                               |
| Date                | 29.07.2024                                   |

## Context
In the context of the VIEWS pipeline, there is a need to standardize the definition and structure of models to ensure consistency and clarity. This involves defining what constitutes a model and outlining the specific obligations for model directories, including the required scripts and artifacts for both forecasting and experimentation.

## Decision
This decision establishes a standardized definition and structure for models in the VIEWS pipeline, including the necessary scripts and artifacts for forecasting and experimentation.

### Overview
1. A specific instantiation of a machine learning algorithm.
2. Trained using a predetermined and unique set of hyperparameters.
3. On a well-defined set of input features.
4. Targeting a specific outcome target.
5. For stepshift models, it includes all code and artifacts necessary to generate a comprehensive 36-month forecast for the specified target.
6. Models that are identical in all other aspects will be considered distinct if different post-processing techniques are applied to their generated predictions.

Additionally, model directories must adhere to a specific structure and contain a number of essential scripts to generate monthly forecasts and support model experimentation.

## Consequences
**Positive Effects:**
- Ensures a clear and consistent definition of models within the VIEWS pipeline.
- Standardizes the structure of model directories, making it easier to manage and understand.
- Facilitates the generation of monthly forecasts and supports systematic model experimentation.

**Negative Effects:**
- Imposes a strict structure that might limit flexibility in some cases.
- Requires existing models to be restructured to comply with the new standards.

## Rationale
The rationale behind this decision is to maintain architectural integrity and promote consistency across the VIEWS pipeline. By clearly defining what constitutes a model and standardizing the structure and required scripts, the project can ensure that all models are comprehensible, reproducible, and maintainable.

### Considerations
- Potential risks include the initial effort required to restructure existing models.
- Ensuring all team members are aware of and adhere to the new standards.

## Additional Notes
Model directories must conform to the structure defined in the root README.md, which can be quickly replicated by running `meta_tools/make_new_model_dir`. The specific scripts required for forecasting and experimentation are outlined below.

### Required Scripts for Monthly Forecasts
- `configs/config_hyperparameters.py`
- `src/artifacts/metadata_dict.py`
- `src/dataloaders/get_latest_data.py`
- `src/training/train_pipeline_model.py`
- `src/online_evaluation/evaluate_forecast.py`
- `src/drift_detection/drift_detection_input.py`
- `src/drift_detection/drift_detection_output.py`
- `src/drift_detection/drift_detection_performance.py`
- `src/forecasting/generate_forecast.py`

### Required Scripts for Model Experimentation
- `src/dataloaders/get_partitioned_data.py`
- `src/training/train_experimental_model.py`
- `src/offline_evaluation/evaluate_model.py`
- `src/offline_evaluation/evaluate_sweep.py`

### Required Artifacts
- `artifacts/model_train_partition.pth` (or `.pkl`)
- `artifacts/model_test_partition.pth` (or `.pkl`)
- `artifacts/model_forecasting.pth` (or `.pkl`)

### Outputs
The final output from `src/forecasting/generate_forecast.py` should be an array or pandas DataFrame to quantify uncertainty.

## Feedback and Suggestions
Team members and stakeholders are encouraged to provide feedback or suggest improvements on the decision or its implementation through repository issues or during regular team meetings.
