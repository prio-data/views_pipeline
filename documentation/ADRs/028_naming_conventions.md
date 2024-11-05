## Establishing Standard Naming Conventions for Classes, Functions, Variables, and Files

| ADR Info            | Details           |
|---------------------|-------------------|
| Subject             | Naming Conventions for Classes, Functions, Variables, and Files  |
| ADR Number          | 	028   |
| Status              | Proposed   |
| Author              | Dylan   |
| Date                | 05.11.2024     |

## Context
*The `common_utils` directory contains several scripts with functions that are related but scattered across different files. This lack of organization can lead to difficulties in maintaining the codebase, understanding the functionality, and ensuring consistency. To address these issues, we propose encapsulating related functions into their respective classes and following Python and MLOps best practices for naming conventions.*

## Decision
*TBD*

## Overview

### Class Naming
* Use **PascalCase** for class names.
* Ensure class names are descriptive yet concise, conveying each class’s purpose without verbosity. Ensure public methods can be easily overridden to avoid restricting creativity during model development.

Examples:
*  **Utility Classes (Utils)**: For general-purpose helper functions that don’t fit within a specific module (e.g., `DataUtils`, `FileUtils`).
*  **Handler Classes (Handler)**: For managing specific processes or workflows, especially useful in data handling or API interactions (e.g., `DataHandler`, `RequestHandler`, `CliHandler`).
*  **Manager Classes (Manager)**: For classes that coordinate actions among multiple modules or components, aligning with DevOps' modular design principles (e.g., `SessionManager`, `PipelineManager`, `ModelManager`).
Example: `ModelManager(model_path_obj).train(params).evaluate(params).save()` should trigger the model workflow.
*  **Loader Classes (Loader)**: For classes dedicated to loading data, configurations, or assets, commonly used in data pipelines (e.g., `DataLoader`, `ConfigLoader`).
* **Builder Classes (Builder)**: For constructing or configuring objects, aligning with standard MLOps practices of creating reusable and testable components (e.g., `ModelScaffoldBuilder`, `PipelineBuilder`).

```python
# Good examples
class DataLoader:
    """Class to load and preprocess data."""
    def __init__(self, source: str):
        self.source = source

    def load_data(self) -> pd.DataFrame:
        """Load data from the source."""
        return pd.read_csv(self.source)

class ModelTrainer:
    """Class to train machine learning models."""
    def __init__(self, model: Any):
        self.model = model

    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Train the model with the given data."""
        self.model.fit(X, y)

class PredictionEvaluator:
    """Class to evaluate model predictions."""
    def __init__(self, predictions: pd.Series, actuals: pd.Series):
        self.predictions = predictions
        self.actuals = actuals

    def calculate_accuracy(self) -> float:
        """Calculate the accuracy of the predictions."""
        return (self.predictions == self.actuals).mean()

# Bad examples
class dataloader:  # Not using CamelCase
    def __init__(self, source):
        self.source = source

    def loaddata(self):
        return pd.read_csv(self.source)

class modeltrainer:  # Not using CamelCase
    def __init__(self, model):
        self.model = model

    def train(self, X, y):
        self.model.fit(X, y)

class predictionevaluator:  # Not using CamelCase
    def __init__(self, predictions, actuals):
        self.predictions = predictions
        self.actuals = actuals

    def calcaccuracy(self):
        return (self.predictions == self.actuals).mean()
```

### Function and Variable Naming 
* Use **snake_case** for function and variable names, following Python’s conventions for readability and consistency.
* Function names should be verb-based, clearly indicating the function’s primary action.

Examples:
*  **Public Functions**: Use descriptive, action-based names to clarify their purpose (e.g., `load_data`, `save_results`, `evaluate_model`).
*  **Private Functions**: Prefix with an underscore to signal intended internal use, supporting encapsulation (e.g., `_validate_input`, `_load_config`).
*  **Constants**: Use uppercase with underscores for global constants to clearly differentiate them from mutable variables (e.g., `DEFAULT_BATCH_SIZE`, `MAX_RETRY_COUNT`).

```python
# Good examples
def calculate_mean(values: List[float]) -> float:
    """Calculate the mean of a list of values."""
    return sum(values) / len(values)

def fetch_data_from_api(endpoint: str) -> dict:
    """Fetch data from a given API endpoint."""
    response = requests.get(endpoint)
    return response.json()

def save_model_to_file(model: Any, filename: str) -> None:
    """Save the model to a file."""
    with open(filename, 'wb') as file:
        pickle.dump(model, file)

# Bad examples
def calcMean(vals):  # Not descriptive, not using snake_case
    return sum(vals) / len(vals)

def getData(endpoint):  # Not descriptive, not using snake_case
    response = requests.get(endpoint)
    return response.json()

def saveModel(model, filename):  # Not using snake_case
    with open(filename, 'wb') as file:
        pickle.dump(model, file)
```

### File Naming
* Use lowercase with underscores for file names.
* Ensure file names are descriptive and specific to the content or function of the file, aiding easy identification in larger repositories.

Examples:
`data_loader.py`
`config_handler.py`
`model_evaluator.py`

### Special Cases
* Document any exceptions or domain-specific naming needs.

*  **Single Leading Underscore**: `_variable`
- Meaning: Indicates that the name is meant for internal use only.
Example: `_internal_variable`

*  **Single Trailing Underscore**: `class_`
Meaning: Avoids naming conflicts with Python keywords and built-in names.
Example: `class_`

*  **Double Leading Underscore**: `__attribute`
Meaning: Triggers name mangling in the context of Python classes. Ensures that the case class is not accidentally overridden or accessed by subclasses, especially where multiple inheritance is common. Name mangling also adds a slight overhead to attribute access. In performance-critical code, consider using single leading underscores instead, as they are more efficient.
Example: `__private_attribute`

*  **Double Leading and Trailing Underscore**: `__name__`
Meaning: Indicates special attributes and methods that Python provides.
Example: `__init__`

*  **Single Underscore**: `_`
Meaning: Indicates a temporary or throwaway variable.
Example: `for _ in range(10)`     

* Abbreviations like `cfg` for configuration files or `meta` for metadata can be acceptable if consistently applied.

### Decorators     
* Use decorators to add functionality to functions or methods in a clean and readable manner.

Examples:
*  **@staticmethod**: For methods that do not access or modify the class state.
*  **@classmethod**: For methods that need to access or modify the class state.
*  **@property**: For methods that should be accessed like attributes.
*  **@retry**: For retrying a function if it fails, useful in network operations.
*  **@timeit**: For measuring the execution time of a function, useful in performance monitoring.
*  **Custom decorators**: For adding specific functionality like validation or logging.

### Dunder (Double Underscore) Methods
Use dunder methods to define special behaviors for classes.
Examples:
*  `__init__`: For initializing class instances.
*  `__str__`: For defining the string representation of an object.
*  `__repr__`: For defining the official string representation of an object.
*  `__eq__`: For defining equality comparison between objects.
*  `__lt__`: For defining less-than comparison between objects.

## Consequences

**Positive Effects:**
*  **Improved Readability**: Clear and consistent naming conventions make the code easier to read and understand.
*  **Enhanced Maintainability**: Consistent naming conventions simplify maintenance and reduce the likelihood of errors.
*  **Better Collaboration**: Standardized naming conventions facilitate collaboration among team members.
*  **Alignment with Best Practices**: Adhering to Python and MLOps best practices ensures the codebase is robust and scalable.
*  **CI/CD Integration**: Consistent naming conventions support automated testing and deployment processes, reducing errors and improving the reliability of CI/CD pipelines.
*  **ReadTheDocs Integration**: Clear and consistent naming conventions enhance the generation of documentation using tools like ReadTheDocs, making it easier to maintain and navigate the documentation.

**Negative Effects:**
*  **Initial Refactoring Effort**: Refactoring existing code to fit the new naming conventions will require an initial investment of time and effort.
*  **Learning Curve**: Team members will need to familiarize themselves with the new naming conventions.

## Rationale
*The choice to develop consistent naming standards is motivated by the need to improve code organization, readability, and maintenance. By adhering to Python and MLOps best practices, we ensure that the codebase is stable, scalable, and easy to navigate. Clear and uniform naming conventions strengthen these advantages.*

## Additional Notes
*  **Documentation**: Update the documentation to reflect the new naming conventions.
*  **Testing**: Ensure that all existing tests are updated to work with the new naming conventions and add new tests as needed.
*  **Code Reviews**: Conduct thorough code reviews to ensure adherence to the new naming conventions.
