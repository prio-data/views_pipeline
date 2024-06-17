from pathlib import Path

def assess_ensemble_dir(ensemble_dir):
    """
    Assess the structure and presence of obligatory scripts in an ensemble directory.
    
    Args:
    - ensemble_dir (str): Path to the ensemble directory.
    
    Returns:
    - assessment (dict): Dictionary containing assessment results.
    """
    assessment = {
        "ensemble_dir": ensemble_dir,
        "structure_errors": [],
        "missing_scripts": []
    }
    
    # Define the expected structure
    expected_structure = [
        "configs",
        "artifacts",
        "src/dataloaders",
        "src/utils",
        "src/training",
        "src/offline_evaluation",
        "src/management",
        "src/forecasting"
    ] 

    # Convert model_dir to a Path object
    ensemble_path = Path(f'../ensemble/{ensemble_dir}')
    
    # Check structure
    for item in expected_structure:
        item_path = ensemble_path / item
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
        full_script_path = ensemble_path / script_path
        if not full_script_path.exists():
            assessment["missing_scripts"].append(f"Missing script: {script_path}")
    
    return assessment

if __name__ == "__main__":
    ensemble_dir = input("Enter the path to the ensemble directory: ")
    assessment = assess_ensemble_dir(ensemble_dir)
    print("\nAssessment results:")
    print("Ensemble directory:", assessment["ensemble_dir"])
    print("Structure errors:", assessment["structure_errors"])
    print("Missing scripts:", assessment["missing_scripts"])