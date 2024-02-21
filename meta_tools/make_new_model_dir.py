import os

def make_new_model_dir(model_name):
    """
    Create a new directory for a standard model.
    
    Args:
    - model_name (str): Name of the model.
    
    Returns:
    - model_dir (str): Path to the newly created model directory.
    """
    models_dir = "models"
    model_dir = os.path.join(models_dir, model_name)
    
    try:
        os.makedirs(model_dir)
        print(f"Created new model directory: {model_dir}")
    except FileExistsError:
        print(f"Model directory already exists: {model_dir}")
    
    # Create subdirectories
    subdirs = [
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
        "src/forecasting"
    ]
    
    for subdir in subdirs:
        subdir_path = os.path.join(model_dir, subdir)
        os.makedirs(subdir_path, exist_ok=True)
        print(f"Created subdirectory: {subdir_path}")
    
    # Create README.md and requirements.txt
    readme_path = os.path.join(model_dir, "README.md")
    with open(readme_path, "w") as readme_file:
        readme_file.write("# Model README\n")
    print(f"Created README.md: {readme_path}")
    
    requirements_path = os.path.join(model_dir, "requirements.txt")
    with open(requirements_path, "w") as requirements_file:
        requirements_file.write("# Requirements\n")
    print(f"Created requirements.txt: {requirements_path}")
    
    return model_dir

if __name__ == "__main__":
    model_name = input("Enter the name of the model: ")
    make_new_model_dir(model_name)
