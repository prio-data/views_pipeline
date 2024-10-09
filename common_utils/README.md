# Common utility functions

This folder contains reusable functions and classes to be used across multiple or all models (i.e., the entire pipeline). Model-specific utils can be found in the respective model source code (src).

Overview of utils package scripts:
- views_stepshift: package performing the VIEWS-developed stepshifting algorithm (testing mode)
- `hurdle_model.py`: Class defining hurdle models, i.e., regression model which handles excessive zeros by fitting a two-part model and combining predictions
- `set_path.py`: Functions for machine-agnostic extracting and returning paths for root, models, data, artifacts.
- `utils_artifacts.py`: Functions to retrieve the path of model artifact
- `utils_cli_parser.py`: Fuctions for command-line-interface parser for model specific main.py scripts
- `utils_dataloaders.py`: Functions to create or load input data & perform input drift detection
- `utils_df_to_vol_conversion.py`: Functions to convert data frames and volumes (used in purple_alien)
- `utils_evaluation_metrics.py`: Class defining evaluation metrics
- `utils_model_outputs.py`: Class for storing and managing model outputs for evaluation and true forcasting

To do list:
- Align the function generate_metric_dict in utils_evaluation_metrics.py with Simon's eval function

# ModelPath (common_utils/model_path.py)

### Initialization

To start using the `ModelPath` class, you need to initialize it with a specific model name. You can optionally validate whether the directories and scripts exist. 

```python
from utils_model_paths import ModelPath

# Initialize ModelPath with a model name
purple_alien = ModelPath("purple_alien", validate=True)
```

* `model_name`: The name of the model you are working with. This will be used to locate the corresponding directories and scripts.
* `validate`: If set to True, the class will check if the specified directories and scripts exist and raise errors if they do not. Defaults to True.

### Viewing Directories and Scripts
Once the ModelPath instance is created, you can view all the directories and scripts that are relevant to your model.

* **View Directories**: This method prints a formatted list of all directories associated with the model.
```python
purple_alien.view_directories()
```

* **View Scripts**: This method lists all expected scripts for the model.
```python
purple_alien.view_scripts()
```

### Working with model and script paths
```python
purple_alien.get_directories()
```
This method returns a dictionary of directory names and their absolute paths for the current model. The method scans through all class attributes and collects directories that are part of the model's structure, excluding internal or unrelated attributes.
#### Key Points:
- **Returns**: A dictionary where keys are directory names (as `str`) and values are the absolute paths (as `str`) of the corresponding directories.
```python
{
    'architectures': '/path/to/models/purple_alien/src/architectures',
    'artifacts': '/path/to/models/purple_alien/artifacts',
    'configs': '/path/to/models/purple_alien/configs',
    'dataloaders': '/path/to/models/purple_alien/src/dataloaders',
    ...
}
```

```python
purple_alien.get_scripts()
```
This method retrieves a dictionary of script file names and their absolute paths. It looks for the specific script files related to the model (such as configuration, training, and evaluation scripts) that are predefined during class initialization.
#### Key Points:
- **Returns**: A dictionary where keys are script names (as str) and values are their absolute paths (as str). If the script is not found, the value will be None.
```python
{
    'config_deployment.py': '/path/to/models/purple_alien/configs/config_deployment.py',
    'train_ensemble.py': '/path/to/models/purple_alien/src/training/train_ensemble.py',
    'get_data.py': '/path/to/models/purple_alien/src/dataloaders/get_data.py',
    ...
}
```

### Usage Scenarios:
`get_directories()` can be used to verify the existence and location of the important directories for a given model, helping to ensure the model structure is in place.
`get_scripts()` can help confirm that all required scripts for the model (training, forecasting, evaluation, etc.) are available and accessible.

#### Example:
```python
directories = purple_alien.get_directories()
```

### Adding and Removing Paths
The `ModelPath` class provides methods to add the relevant directories to Python's sys.path so that scripts can be easily imported, and to remove them when they are no longer needed.
* **Add Paths to sys.path**:
```python
purple_alien.add_paths_to_sys()
```
* **Remove Paths from sys.path**:
```python
model_path.remove_paths_from_sys()
```

### Working with Querysets
The `get_queryset()` method returns the queryset module for the model, which contains functions for data querying. This can be useful for retrieving specific data relevant to your model.
```python
queryset = model_path.get_queryset()
```
The `ModelPath` class checks if the queryset file exists, attempts to import it, and logs the process. If validation is enabled and the queryset file is missing, it raises an error.
