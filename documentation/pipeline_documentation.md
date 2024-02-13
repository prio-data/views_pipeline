# Documentation of VIEWS Pipeline 001 (i.e., Cabin Hackaton Pipeline)

## Motivation and Rationale
The VIEWS early-warning system pipeline produces predictions on a monthly basis, for a variety of models. However, in the last months, several errors have occured that compromise the quality of our forecasts. Additionally, the pipeline does not yet adhere to best practices standards relating to the structure and implementation. As a result, the VIEWS Pipeline is being rewritten and improved during a 5-day hackathon. We aim to develop a minimal solution first, that can be further developed in the future to accommodate more needs and models.

The most important changes relate to the following elements: standardizing  moving away from Notebooks and towards scripts; implementing alert gates for input and performance drift; using the platform Weights & Biases for logging and visualizing model outputs; using the platform Prefect to carry out the entire monthly run, from fetching the input data through a queryset to allocating predictions in the prediction store on Fimbulthul server.

## Definition of Key Terms

**Model** is understood as:

1) A specific instantiation of a machine learning algorithm, 

2) Trained using a predetermined and unique set of hyperpara.meters,

3) On a well-defined set of input features,

4) And targeting a specific outcome target.

5) In the case of stepshift models, a model is understood as **all** code and **all** artifacts necessary to generate a comprehensive 36 month forecast for the specified target.

6) Note that, two models, identical in all other aspects, will be deemed distinct if varying post-processing techniques are applied to their generated predictions. For instance, if one model's predictions undergo calibration or normalization while the other's do not.

**Run** is defined as:

## Standardization
We have agreed to standardize the pipeline in several ways. 

### Naming Conventions
**Models** will no longer carry descriptive titles (e.g., *transform_log_clf_name_LGBMClassifier_reg_name_LGBMRegressor*). As more and more models are developed over time, this would become too chaotic, long, and ultimately small differences could not be communicated properly through the title. Instead, the code and metadata of the model should be use to substantively differentiate them between each other. 

The new naming convention for models takes the form of *adjective_noun*, adding more models alphabetically. For example, the first model to be added can be named *amazing_apple*, the second model *bad_bunny*, etc. This is a popular practice, and Weights & Biases implements this naming convention automatically. 

*To be clarified: how to "translate" when moving from model development to communicating results.*

### GitHub Repository
The entire pipeline is contained in the repository "views-pipeline", which has a predefined structure stated in the readme. The root (entire pipeline) contains folders for: models; ensembles; prefect; documentation; and meta-tools. 

Within the **models folder**, there is a sub-folder for each model (as defined and named above). 

