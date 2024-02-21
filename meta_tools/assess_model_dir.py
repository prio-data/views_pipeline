import os

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
        "data/raw",
        "data/processed",
        "data/generated",
        "artifacts",
        "notebooks",
        "reports/plots",
        "reports/figures",
        "reports/timelapse",
        "reports/papers",
        "reports/slides",
        "src/dataloaders",
        "src/architectures",
        "src/utils",
        "src/visualization",
        "src/training",
        "src/offline_evaluation",
        "src/online_evaluation",
        "src/drift_detection",
        "src/forecasting",
        "README.md",
        "requirements.txt"
    ]
    
    # Check structure
    for item in expected_structure:
        item_path = os.path.join(model_dir, item)
        if not os.path.exists(item_path):
            assessment["structure_errors"].append(f"Missing directory or file: {item}")
    
    # Check for obligatory scripts
    obligatory_scripts = [
        "configs/config_common.py", #or config_partitioner depending on what we decide
        "configs/config_hyperparameters.py",
        "src/dataloaders/get_forecasting_data.py"
        "src/training/train_forecasting_model.py",
        "src/online_evaluation/evaluate_forecast.py",
        "src/forecasting/generate_forecast.py",
        "main.py",
        "README.md"
        ]
    
    for script_path in obligatory_scripts:
        full_script_path = os.path.join(model_dir, script_path)
        if not os.path.exists(full_script_path):
            assessment["missing_scripts"].append(f"Missing script: {script_path}")
    
    return assessment

if __name__ == "__main__":
    model_dir = input("Enter the path to the model directory: ")
    assessment = assess_model_dir(model_dir)
    print("\nAssessment results:")
    print("Model directory:", assessment["model_dir"])
    print("Structure errors:", assessment["structure_errors"])
    print("Missing scripts:", assessment["missing_scripts"])
