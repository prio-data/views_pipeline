from pathlib import Path

def assess_model_dir(model_dir):
    """
    Assess the structure and presence of obligatory scripts in a model directory.
    
    Args:
    - model_dir (str): Path to the model directory.
    
    Returns:
    - assessment (dict): Dictionary containing assessment results.
    """
    assessment = {
        "model_dir": model_dir,
        "structure_errors": [],
        "missing_scripts": []
    }
    
    # Define the expected structure
    expected_structure = [
        "configs",
        "artifacts",
        "notebooks",
        "reports",
        "src/dataloaders",
        "src/architectures",
        "src/utils",
        "src/training",
        "src/offline_evaluation",
        "src/online_evaluation",
        "src/forecasting"
    ] 

    # Convert model_dir to a Path object
    model_path = Path(f'../models/{model_dir}')
    
    # Check structure
    for item in expected_structure:
        item_path = model_path / item
        if not item_path.exists():
            assessment["structure_errors"].append(f"Missing directory or file: {item}")
    
    # Check for obligatory scripts
    obligatory_scripts = [
       "configs/config_deployment.py", 
        "configs/config_hyperparameters.py", 
        "configs/config_input_data.py",
        "configs/config_meta.py",
        "configs/config_sweep.py",
        "src/dataloaders/get_data.py"
        "src/training/train_ensemble.py",
        "src/forecasting/generate_forececast.py",
        "src/offline_evaluation/evaluate_model.py",
        "src/management/execute_model_runs.py",
        "src/management/execute_model_tasks.py",
        "main.py",
        "README.md"
        ]
    
    for script_path in obligatory_scripts:
        full_script_path = model_path / script_path
        if not full_script_path.exists():
            assessment["missing_scripts"].append(f"Missing script: {script_path}")
    
    return assessment

if __name__ == "__main__":
    model_dir = input("Enter the path to the model directory: ")
    assessment = assess_model_dir(model_dir)
    print("\nAssessment results:")
    print("Model directory:", assessment["model_dir"])
    print("Structure errors:", assessment["structure_errors"])
    print("Missing scripts:", assessment["missing_scripts"])
