# Model Definition

In the context of the VIEWS pipeline, a model should be understood as:

1) A specific instantiation of a machine learning algorithm, 

2) Trained using a predetermined and unique set of hyperpara.meters,

3) On a well-defined set of input features,

4) And targeting a specific outcome target.

5) In the case of "stepshift" models, a model is understood as **all** code and **all** artifacts necessary to generate a comprehensive 36-month forecast for the specified target.

6) Note that, two models, identical in all other aspects, will be deemed distinct if varying post-processing techniques are applied to their generated predictions. For instance, if one model's predictions undergo calibration or normalization while the other's do not.