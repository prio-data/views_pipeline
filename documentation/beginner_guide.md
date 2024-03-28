# Glossary of Technical Terms

## Config File
Config files specify the settings and hyperparameters used to train machine learning models, allowing for easy experimentation and optimization without modifying the code – i.e., you don't want to hard code (i.e., write directly) hyperparameters into your model code.

## Orchestration
The Prefect Flow coordinates the execution of tasks, ensuring that they are executed in the correct order based on their dependencies.

## Hyperparameters
Hyperparameters are parameters or settings that are not directly learned from data during the training process of a machine learning model, but rather are set prior to training and influence the behavior and performance of the model. For example, hyperparameters could include the learning rate, number of estimators, number of jobs, and transformation of data.

For more information, see the [Weights & Biases article "Intro to MLOps: Hyperparameter Tuning"](https://wandb.ai/site/articles/intro-to-mlops-hyperparameter-tuning).

## Prefect
Prefect is used for workflow orchestration, defining the sequence of tasks (task1, task2, task3) and their dependencies.

See the Quickstart guide [here](https://docs.prefect.io/latest/getting-started/quickstart/).

## Sweep
A sweep configuration is a set of specifications defining how hyperparameters should be explored during a hyperparameter search, the hyperparameters to be tuned, and their respective ranges or values to be tried. 

## Weights & Biases (wandb)
Weights & Biases (W&B) is used to log relevant information (such as data, transformations, and results) produced by each task during the execution of the workflow. W&B logging within each task enables tracking and monitoring of the workflow's progress and outputs, enhancing visibility and reproducibility.

See the Quickstart guide [here](https://docs.wandb.ai/quickstart).

## Utils/Utility Functions
Collection of functions or tools that serve various general purposes and are commonly reused across different parts of a software project. These utility functions are often not specific to any particular domain or task but rather provide common functionalities that can be helpful in many different situations.