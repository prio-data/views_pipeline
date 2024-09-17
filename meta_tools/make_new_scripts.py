from pathlib import Path
import py_compile
from typing import Dict
from utils import model_naming

# TOOD: Implement a mechanism to generate the scripts from template files at views_pipeline/meta_tools/templates


class ModelScriptBuilder:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model_dir = Path(self.model_name)
        self.architecture = None
        self.obligatory_scripts = [
            "configs/config_deployment.py",
            "configs/config_hyperparameters.py",
            "configs/config_input_data.py",
            "configs/config_meta.py",
            "configs/config_sweep.py",
            "src/dataloaders/get_data.py",
            "src/training/train_ensemble.py",
            "src/forecasting/generate_forececast.py",
            "src/offline_evaluation/evaluate_model.py",
            "src/management/execute_model_runs.py",
            "src/management/execute_model_tasks.py",
            "main.py",
            "README.md"
        ]

        self.current_dir = Path.cwd()
        self.relative_path = "models"

        # If the current directory is not the root directory, go up one level and append "models"
        if self.current_dir.match('*meta_tools'):
            self.models_dir = self.current_dir.parent / self.relative_path
        else:
            self.models_dir = self.current_dir / self.relative_path

        self.model_dir = self.models_dir / model_name

    def _save_script(self, output_file: Path, code: str) -> bool:
        """
    Compiles a Python script to a specified file and saves it.

    Parameters:
    output_file : Path
        The path to the file where the Python script will be saved. This should
        be a `Path` object pointing to the desired file location, including
        the filename and extension (e.g., 'script.py').

    code : str
        The Python code to be written to the file. This should be a string containing
        valid Python code that will be saved and compiled.

    Returns:
    bool:
        Returns `True` if the script was successfully written and compiled.
        Returns `False` if an error occurred during the file writing or compilation.

    Raises:
    IOError: If there is an error writing the code to the file (e.g., permission denied, invalid path).

    py_compile.PyCompileError: If there is an error compiling the Python script (e.g., syntax error in the code).

    Example:
    >>> code = "print('Hello, World!')"
    >>> output_file = Path('hello_world.py')
    >>> _save_script(output_file, code)
    True
    """
        try:
            # Write the sample code to the Python file
            with open(output_file, "w") as file:
                file.write(code)

            # Compile the newly created Python script
            py_compile.compile(
                output_file)  # cfile=output_file.with_suffix('.pyc')

            return True
        except (IOError, py_compile.PyCompileError) as e:
            print(
                f"Failed to write or compile the deployment configuration script: {e}")
            return False

    def _gen_config_deployment(self, deployment_type: str = "shadow", additional_settings: Dict[str, any] = None) -> bool:
        """
        Generates a deployment configuration script and writes it to a specified file. The script is then compiled.

        This function creates a Python script that defines the deployment configuration settings for the application.
        The script includes the deployment status and any additional settings specified. The generated script is 
        saved to the `configs` directory within `self.model_dir` and is compiled into bytecode.

        Parameters:
        deployment_type : str, optional
            The type of deployment. Must be one of "shadow", "deployed", "baseline", or "deprecated". Default is "shadow".
        additional_settings : dict, optional
            A dictionary of additional settings to include in the deployment configuration. Defaults to None.

        Raises:
        ValueError: If `deployment_type` is not one of the valid types.

        Returns:
        bool: True if the script was written and compiled successfully, False otherwise.
        """
        valid_types = {"shadow", "deployed", "baseline", "deprecated"}
        if deployment_type.lower() not in valid_types:
            raise ValueError(
                f"Invalid deployment_type: {deployment_type}. Must be one of {valid_types}.")

        deployment_config = {
            "deployment_status": deployment_type.lower()
        }

        # Merge additional settings if provided
        if additional_settings and isinstance(additional_settings, dict):
            deployment_config.update(additional_settings)

        # Generate the script code
        code = f"""\"\"\"
Deployment Configuration Script

This script defines the deployment configuration settings for the application. 
It includes the deployment status and any additional settings specified.

Deployment Status:
- shadow: The deployment is shadowed and not yet active.
- deployed: The deployment is active and in use.
- baseline: The deployment is in a baseline state, for reference or comparison.
- deprecated: The deployment is deprecated and no longer supported.

Additional settings can be included in the configuration dictionary as needed.

\"\"\"

def get_deployment_config():
    # Deployment settings
    deployment_config = {deployment_config}
    return deployment_config
"""
        return self._save_script(
            self.model_dir / "configs/config_deployment.py", code)

    def _gen_config_hyperparameters(self, model_architecture: str) -> bool:
        """
    Writes the `get_hp_config` function to a Python script file and compiles it to bytecode.

    Parameters:
        output_dir : Path
            The directory where the Python script will be saved and compiled.

    Returns:
        bool: True if the script was written and compiled successfully, False otherwise.
    """
        code = f"""def get_hp_config():
    \"""
    Contains the hyperparameter configurations for model training.
    This configuration is "operational" so modifying these settings will impact the model's behavior during the training.

    Returns:
    - hyperparameters (dict): A dictionary containing hyperparameters for training the model, which determine the model's behavior during the training phase.
    \"""
    
    hyperparameters = {{
        'model': '{model_architecture}',  # The model architecture used
        # Add more hyperparameters as needed
    }}
    return hyperparameters
"""
        return self._save_script(
            self.model_dir / "configs/config_hyperparameters.py", code)

    def _gen_config_input_data(self):
        code = f"""from viewser import Queryset, Column

def get_input_data_config():
    \"""
    Contains the configuration for the input data in the form of a viewser queryset. That is the data from viewser that is used to train the model.
    This configuration is "behavioral" so modifying it will affect the model's runtime behavior and integration into the deployment system.
    There is no guarantee that the model will work if the input data configuration is changed here without changing the model settings and architecture accordingly.

    Returns:
    - queryset_base (Queryset): A queryset containing the base data for the model training.
    \"""
    
    # VIEWSER 6, Example configuration

    queryset_base = (Queryset("{self.model_name}", "priogrid_month")
        # Create a new column 'ln_sb_best' using data from 'priogrid_month' and 'ged_sb_best_count_nokgi' column
        # Apply logarithmic transformation, handle missing values by replacing them with NA
        .with_column(Column("ln_sb_best", from_loa="priogrid_month", from_column="ged_sb_best_count_nokgi")
            .transform.ops.ln().transform.missing.replace_na())
        
        # Create a new column 'ln_ns_best' using data from 'priogrid_month' and 'ged_ns_best_count_nokgi' column
        # Apply logarithmic transformation, handle missing values by replacing them with NA
        .with_column(Column("ln_ns_best", from_loa="priogrid_month", from_column="ged_ns_best_count_nokgi")
            .transform.ops.ln().transform.missing.replace_na())
        
        # Create a new column 'ln_os_best' using data from 'priogrid_month' and 'ged_os_best_count_nokgi' column
        # Apply logarithmic transformation, handle missing values by replacing them with NA
        .with_column(Column("ln_os_best", from_loa="priogrid_month", from_column="ged_os_best_count_nokgi")
            .transform.ops.ln().transform.missing.replace_na())
        
        # Create columns for month and year_id
        .with_column(Column("month", from_loa="month", from_column="month"))
        .with_column(Column("year_id", from_loa="country_year", from_column="year_id"))
        
        # Create columns for country_id, col, and row
        .with_column(Column("c_id", from_loa="country_year", from_column="country_id"))
        .with_column(Column("col", from_loa="priogrid", from_column="col"))
        .with_column(Column("row", from_loa="priogrid", from_column="row"))
    )

    return queryset_base
"""
        return self._save_script(
            self.model_dir / "configs/config_input_data.py", code)

    def _gen_config_meta(self) -> bool:
        code = f"""def get_meta_config():
    \"""
    Contains the meta data for the model (model architecture, name, target variable, and level of analysis).
    This config is for documentation purposes only, and modifying it will not affect the model, the training, or the evaluation.

    Returns:
    - meta_config (dict): A dictionary containing model meta configuration.
    \"""
    
    meta_config = {{
        "name": "{self.model_name}",
        "architecture": "{self.model_architecture}", 
        # Uncomment and modify the following lines as needed for additional metadata:
        # "target(S)": ["ln_sb_best", "ln_ns_best", "ln_os_best", "ln_sb_best_binarized", "ln_ns_best_binarized", "ln_os_best_binarized"],
        # "queryset": "escwa001_cflong",
        # "level": "pgm",
        # "creator": "Your name here"
    }}
    return meta_config
"""
        return self._save_script(
            self.model_dir / "configs/config_meta.py", code)

    def _gen_config_sweep(self) -> bool:
        code = f"""def get_sweep_config():
    \"""
    Contains the configuration for hyperparameter sweeps using WandB.
    This configuration is "operational" so modifying it will change the search strategy, parameter ranges, and other settings for hyperparameter tuning aimed at optimizing model performance.
    
    Returns:
    - sweep_config (dict): A dictionary containing the configuration for hyperparameter sweeps, defining the methods and parameter ranges used to search for optimal hyperparameters.
    \"""
    
    sweep_config = {{
        'method': 'grid',
    }}
    
    # Example metric setup:
    metric = {{
        'name': 'MSE',
        'goal': 'minimize'   
    }}
    sweep_config['metric'] = metric
    
    # Example parameters setup:
    parameters_dict = {{
        'model': {{
            'value': '{self.model_architecture}'
        }},
    }}
    sweep_config['parameters'] = parameters_dict
    
    return sweep_config
"""
        return self._save_script(
            self.model_dir / "configs/config_sweep.py", code)

    def _gen_dataloaders_get_data(self) -> bool:
        """
    Generates a Python script for data loading functionality and saves it to a specified location.

    Returns:
    bool: Returns `True` if the script was successfully written and saved; `False` otherwise.

    This function relies on the `_save_script` method of the class, which handles the actual file writing and compilation.
    The generated script will be saved in the `model_dir/src/dataloaders/` directory with the name `get_data.py`.

    Notes:
    Ensure that `setup_project_paths` and `setup_data_paths` are correctly
    implemented and available in the expected modules for the generated script to work as intended.
    """
        code = """import sys
from pathlib import Path
import pandas as pd

# Set the path for common_utils module
PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS

# Import necessary functions
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)

from config_input_data import get_input_data
from utils import ensure_float64

def get_data(args):
    \"""
    Fetches data from a parquet file or generates it if the file does not exist.

    Parameters:
    ----------
    args : Namespace
        Contains command-line arguments including 'run_type' to determine the parquet file path.

    Returns:
    -------
    pd.DataFrame
        A pandas DataFrame containing the data.
    \"""
    print("Getting data...")
    
    # Setup data paths
    PATH_RAW, _, _ = setup_data_paths(PATH)
    
    # Define the path to the parquet file
    parquet_path = PATH_RAW / f'raw_{args.run_type}.parquet'
    
    # Check if the parquet file exists
    if not parquet_path.exists():
        # Fetch data using the get_input_data function
        qs = get_input_data()
        data = qs.publish().fetch()
        
        # Ensure all numeric columns are of type float64
        data = ensure_float64(data)
        
        # Save the data to a parquet file
        data.to_parquet(parquet_path)
    else:
        # Load the data from the existing parquet file
        data = pd.read_parquet(parquet_path)

    return data
"""
        return self._save_script(
            self.model_dir / "src/dataloaders/get_data.py", code)

    def _gen_main(self):
        """
    Generates a Python script for the main execution flow of the model training or evaluation process.

    This function creates a Python script that serves as the entry point for executing model runs, either as a sweep or a single run.
    The generated script handles command-line arguments, sets up the project environment, logs into Weights & Biases (wandb), and
    manages the execution of the model runs. It also tracks and reports the runtime of the process.

    Returns:
    bool: Returns `True` if the script was successfully written and saved; `False` otherwise.
    """
        code = """import time
import wandb
import sys
from pathlib import Path

# Set up the path to include common_utils module
PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS

# Import necessary functions for project setup and model execution
from set_path import setup_project_paths
setup_project_paths(PATH)

from utils_cli_parser import parse_args, validate_arguments
from execute_model_runs import execute_sweep_run, execute_single_run

if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()
    
    # Validate the arguments to ensure they are correct
    validate_arguments(args)

    # Log in to Weights & Biases (wandb)
    wandb.login()

    # Record the start time
    start_t = time.time()

    # Execute the model run based on the sweep flag
    if args.sweep:
        execute_sweep_run(args)  # Execute sweep run
    else:
        execute_single_run(args)  # Execute single run

    # Record the end time
    end_t = time.time()
    
    # Calculate and print the runtime in minutes
    minutes = (end_t - start_t) / 60
    print(f'Done. Runtime: {minutes:.3f} minutes')
"""
        return self._save_script(
            self.model_dir / "main.py", code)

    def build(self):
        self._gen_config_deployment()
        self.model_architecture = input(
            "Enter the architecture of the model: ")
        self._gen_config_hyperparameters(
            model_architecture=self.model_architecture)
        self._gen_config_input_data()
        self._gen_config_meta()
        self._gen_config_sweep()
        # self._gen_dataloaders_get_data()
        # self._gen_main()

    def assess(self) -> dict:
        """
        Assess the model directory by checking for the presence of expected obligatory scripts.

        Returns:
            dict: A dictionary containing assessment results with two keys:
                - 'model_dir': The path to the model directory.
                - 'missing_scripts': A list of errors related to missing script files.
        """
        assessment = {
            "model_dir": self.model_dir,
            "missing_scripts": []
        }
        # Check scripts
        for script_path in self.obligatory_scripts:
            full_script_path = self.model_dir / script_path
            if not full_script_path.exists():
                assessment["missing_scripts"].append(
                    f"Missing script: {script_path}")
        return assessment


if __name__ == "__main__":
    model_name = input("Enter the name of the model: ")
    while not model_naming.validate_model_name(model_name):
        print("Invalid model name. Please use the format 'adjective_noun' in lowercase.")
        model_name = input("Enter the name of the model: ")
    script_builder = ModelScriptBuilder(model_name)
    script_builder.build()
    assessment = script_builder.assess()
    print("\nScript assessment results:")
    print(f"Model directory: {assessment['model_dir']}")
    print(f"Missing scripts: {assessment['missing_scripts']}")
