# Meta Tools

This folder contains several scripts for creating and assessing new model folders with proper structure.

## Building a new model

1. Run `python meta_tools/make_new_model_dir.py` and follow the instructions.
2. After the required directores are created, run `meta_tools/make_new_scripts.py` to build the obligatory script files for your model.


### ModelDirectoryBuilder

The `ModelDirectoryBuilder` class is designed to create and and enforce the obligatory directory structure of a machine learning model in the VIEWS pipeline. For definitions of a model and information on the structure, see this [ADR](https://github.com/prio-data/views_pipeline/blob/main/documentation/ADRs/005_model_definition_and_structure.md).

### ModelScriptBuilder

The `ModelScriptBuilder` class is designed to build and manage essential Python scripts for machine learning model deployment and evaluation within the ViEWS pipeline.

**`ModelScriptBuilder` uses script templates stored in the `meta_tools/templates` directory. Ensure that the model directories are created first to avoid any errors.**

## Checking your conda/mamba environment

`validate_environment.py`contains a set of utilities for managing Python package environments using mamba and pip. The provided script helps in listing, comparing, and synchronizing package versions between the current environment and a saved environment.yml file.

`--check`: Check if the environment matches the environment.yml file.     
`--write`: Write the current environment to environment.yml.

To test the scripts in meta_tools, run `pytest -v meta_tools`