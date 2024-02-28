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
        "notebooks",
        "reports",
        "src/dataloaders",
        "src/architectures",
        "src/utils",
        "src/visualization"
        "src/training",
        "src/offline_evaluation",
        "src/online_evaluation",
        "src/drift_detection",
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
        "configs/config_common.py", 
        "src/dataloaders/get_model_outputs.py"
        "src/training/train_ensemble.py",
        "src/online_evaluation/evaluate_forecast.py",
        "src/forecasting/generate_forecast.py",
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
