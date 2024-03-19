# No change baseline VIEWS Model 🛠️
## A general purpose model for generating VIEWS baseline forecasts

[![Official Website](https://img.shields.io/badge/PRIO_website-www.prio.org-darkgreen
)](https://www.prio.org)
[![VIEWS Forecasting Website](https://img.shields.io/badge/VIEWS_Forecasting-www.viewsforecasting.org-purple
)](https://www.prio.org)
[![Twitter Follow](https://img.shields.io/twitter/follow/PRIOresearch
)](https://twitter.com/PRIOresearch)
[![LinkedIn](https://img.shields.io/badge/PRIO_on_linkedin-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/prio/?originalSubdomain=no)]

VIEWS No Change Baseline model is designed to facilitate generating baseline forecasts. The predictions are the same as the target variable in the training data shifted in time.

The "no change baseline model" is one of the simplest baseline models used in predictive modeling tasks, especially in time-series analysis. This baseline assumes that the target variable will remain unchanged from the previous observation. It's particularly relevant in scenarios where there is no underlying trend or seasonality, and the data is expected to be relatively stable over time.

Here's how the "no change baseline model" works:

Initialization: The model starts by observing the value of the target variable at a certain time point, typically the first observation in the dataset.

Prediction: For each subsequent time point, the model predicts that the value of the target variable will be the same as the value observed at the previous time point.