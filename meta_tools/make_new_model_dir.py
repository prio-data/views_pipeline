from pathlib import Path

def make_new_model_dir(model_name):
    """
    Create a new directory for a standard model.
    
    Args:
    - model_name (str): Name of the model.
    
    Returns:
    - model_dir (str): Path to the newly created model directory.
    """
    # Get the current working directory
    current_dir = Path.cwd()

    # Define the relative path to the "models" directory
    relative_path = "models"

    # If the current directory is not the root directory, go up one level and append "models"
    if current_dir.match('*meta_tools'):
        models_dir = current_dir.parent / relative_path
    else:
        models_dir = current_dir / relative_path
    
    model_dir = models_dir / model_name
    
    try:
        model_dir.mkdir(parents=True, exist_ok=False)        
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
        "src/forecasting"
    ]
    
    for subdir in subdirs:
        subdir_path = model_dir / subdir
        subdir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created subdirectory: {subdir_path}")
    
    # Create README.md and requirements.txt
    readme_path = model_dir / "README.md"
    with open(readme_path, "w") as readme_file:
        readme_file.write("# Model README\n")
    print(f"Created README.md: {readme_path}")
    
    requirements_path = model_dir / "requirements.txt"
    with open(requirements_path, "w") as requirements_file:
        requirements_file.write("# Requirements\n")
    print(f"Created requirements.txt: {requirements_path}")
    
    return model_dir

if __name__ == "__main__":
    model_name = input("Enter the name of the model: ")
    make_new_model_dir(model_name)
