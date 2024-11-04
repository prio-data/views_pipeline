
# Create Model Catalogs


| ADR Info            | Details           |
|---------------------|-------------------|
| Subject             | Create Model Catalog  |
| ADR Number          | 022  |
| Status              | Accepted   |
| Author              | Borbála   |
| Date                | 29.10.2024.     |

## Context
We wanted to have a catalog about all of the models in the pipeline. We needed to do that both for the old and the new pipeline because the structure of the two pipelines and the way how the querysets are organised are different. We also had to be sure that the catalogs update whenever a model is modified or added.

## Decision
### New pipeline
*In the new pipeline there are two spearate catalogs for 'country level' and 'priogrid level' models with the following structure:*
| Model Name | Algorithm | Target | Input Features | Non-default Hyperparameters | Forecasting Type | Implementation Status | Implementation Date | Author |
| ---------- | --------- | ------ | -------------- | --------------------------- | ---------------- | --------------------- | ------------------- | ------ |
| electric_relaxation | RandomForestClassifier | ged_sb_dep | - [escwa001_cflong](https://github.com/prio-data/views_pipeline/blob/main/common_querysets/queryset_electric_relaxation.py) | - [hyperparameters electric_relaxation](https://github.com/prio-data/views_pipeline/blob/main/models/electric_relaxation/configs/config_hyperparameters.py) | None | shadow | NA | Sara |

Configs used to create the catalog:
- `views_pipeline/models/*/configs/config_meta.py`
- `views_pipeline/models/*/configs/config_deployment.py`
- `views_pipeline/models/*/configs/config_hyperparameters.py`
- `views_pipeline/common_querysets/*`

Columns:
- **Model Name**: name of the model, always in a form of `adjective_noun`
- **Algorithm**: "algorithm" from `config_meta.py`
- **Target**: "depvar" from `config_meta.py`
- **Input Features**: "queryset" from `config_meta.py` that points to the queryset in `common_querysets`folder
- **Non-default Hyperparameters**: "hyperparameters model_name" that points to `config_hyperparameters.py`
- **Forecasting Type**: TBD
- **Implementation Status**: "deployment_status" from `config_deployment.py` (e.g. shadow, deployed, baseline, or deprecated)
- **Implementation Date**: TBD
- **Author**: "creator" from `config_meta.py`

### Old Pipeline
*In the old pipeline there is only one catalog that contains both  'country level' and 'priogrid level' models with the following structure:*
| Model Name | Algorithm | Target | Input Features | Non-default Hyperparameters | Forecasting Type | Implementation Status | Implementation Date | Author |
| ---------- | --------- | ------ | -------------- | --------------------------- | ---------------- | --------------------- | ------------------- | ------ |
| fatalities002_baseline_rf | XGBRFRegressor | ln_ged_sb_dep | - [fatalities002_baseline](https://github.com/prio-data/viewsforecasting/blob/main/Tools/cm_querysets.py#L16) | n_estimators=300, n_jobs=nj | Direct multi-step | no | NA | NA |

Configs used to create the catalog:
- [ModelDefinitions.py](https://github.com/prio-data/viewsforecasting/blob/main/SystemUpdates/ModelDefinitions.py)
- [cm_querysets.py](https://github.com/prio-data/viewsforecasting/blob/main/Tools/cm_querysets.py)
- [pgm_querysets.py](https://github.com/prio-data/viewsforecasting/blob/main/Tools/pgm_querysets.py)

Columns:
- **Model Name**: "modelname" from `ModelDefinitions.py`
- **Algorithm**: "algorithm" from `ModelDefinitions.py`
- **Target**: "depvar" from `ModelDefinitions.py`
- **Input Features**: "queryset" from `ModelDefinitions.py` pointing to the corresponding line in `cm_querysets.py` or `pgm_querysets.py`
- **Non-default Hyperparameters**: the argument of "algorithm" from `ModelDefinitions.py`
- **Forecasting Type**: Direct multi-step
- **Implementation Status**: no (none of these models are in production)
- **Implementation Date**: TBD
- **Author**: TBD

### GitHub actions
The catalogs are updated via GitHub actions. Action for the new pipeline: [update_views_pipeline_cm_catalog.yml](https://github.com/prio-data/viewsforecasting/blob/github_workflows/.github/workflows/update_views_pipeline_cm_catalog.yml), action for the old pipeline: [check_if_new_model_added.yml](https://github.com/prio-data/views_pipeline/blob/production/.github/workflows/check_if_new_model_added.yml). They trigger when the config files are modified on the `production` and `development` branch. These GitHub actions can also be triggered manually for testing reason. The GitHub actions can only push to non-protected branches.


### Overview
Creating catalogs for 'country level' and 'priogrid level' that update automatically when a model is modified. Separate implementation for the old and the new pipeline.


## Consequences
Clear overview about our existing models in the `views_pipeline/documentation/catalogs/` directory.

**Positive Effects:**
- Our models become trackable and presentable.
- Model features are easily accessible via links. 

**Negative Effects:**
- The github actions and generator scripts require maintenance.
- If the catalogs fail to update, it might remain unnoticed for a while.

## Rationale
Every information about the models are found at one place. Models can be tracked and presented, even for people not involved in the development. It is easier to involve new people to the model development. GitHub actions provide a convenient way to keep the catalogs up-to-date.


### Considerations
- We decided to separate 'country level' and 'priogrid level' models into different catalogs. 
- We needed a separate catalog for the old pipeline as well, which will be depreciated. 
- GitHub actions push to `development` branch, but they cannot push to `production` branch, since it is protected.



## Additional Notes
- Involving GitHub actions led to the separation of `production` and `development`branch, since they cannot push to a protected branch (`production`). More detailed information is found in **ADR #023**.

- Implementation of an alerting system, if GitHub actions fail.

## Feedback and Suggestions
*Feedbacks are awaited.*

---
