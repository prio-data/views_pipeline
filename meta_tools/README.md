# Meta Tools

This folder contains several scripts for creating and assessing new model folders with proper structure.

To create a new model folder, run `make_new_model_dir.py` and follow the instructions.

## ModelDirectoryBuilder

The `ModelDirectoryBuilder` class is designed to create and and enforce the obligatory directory structure of a machine learning model in the VIEWS pipeline. For definitions of a model and information on the structure, see this [ADR](https://github.com/prio-data/views_pipeline/blob/main/documentation/ADRs/005_model_definition_and_structure.md).

### Usage

Create an instance of `ModelDirectoryBuilder` by providing the model name in the format adjective_noun, e.g., 'happy_kitten'.

1. Run `python meta_tools/make_new_model_dir.py`.
2. After the required directores are created, run `meta_tools/make_new_scripts.py` to build the obligatory script files for your model.

## ModelScriptBuilder

The `ModelScriptBuilder` class is designed to build and manage essential Python scripts for machine learning model deployment and evaluation within the ViEWS pipeline.

**`ModelScriptBuilder` uses script templates stored in the `meta_tools/templates` directory. Ensure that the model directories are created first to avoid any errors.**
