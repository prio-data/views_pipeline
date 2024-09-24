# Meta Tools

This folder contains several scripts for creating and assessing new model folders with proper structure.

To create a new model folder, run `make_new_model_dir.py` and enter your desired name into the command line in the format adjective_noun or create an instance of the `ModelDirectoryBuilder` class.

## ModelDirectoryBuilder

The `ModelDirectoryBuilder` class is designed to create and manage the directory structure for a machine learning model.

### Usage

1. **Initialization**: Create an instance of `ModelDirectoryBuilder` by providing the model name.
    ```python
    model_directory_builder = ModelDirectoryBuilder("example_model")
    ```

2. **Building the Directory Structure**: Call the `build` method to create the directory structure and initialize essential files.
    ```python
    model_directory_builder.build()
    ```

3. **Assessing the Directory Structure**: Call the `assess` method to check the directory structure and identify any missing directories.
    ```python
    assessment = model_directory_builder.assess()
    print(f"Model directory: {assessment['model_dir']}")
    print(f"Structure errors: {assessment['structure_errors']}")
    ```

## ModelScriptBuilder

The `ModelScriptBuilder` class is designed to build and manage essential Python scripts for machine learning model deployment and evaluation within the ViEWS pipeline.

**`ModelScriptBuilder` uses script templates stored in the `meta_tools/templates` directory. Ensure that the model directories are created first to avoid any errors.**

1. **Initialization**: Create an instance of `ModelScriptBuilder` by providing the model name.
    ```python
    script_builder = ModelScriptBuilder("example_model")
    ```

2. **Building the Scripts**: Call the `build` method to generate the necessary scripts.
    ```python
    script_builder.build()
    ```

3. **Assessing the Scripts**: Call the `assess` method to check the directory for missing scripts.
    ```python
    assessment = script_builder.assess()
    print(f"Model directory: {assessment['model_dir']}")
    print(f"Missing scripts: {assessment['missing_scripts']}")
    ```
