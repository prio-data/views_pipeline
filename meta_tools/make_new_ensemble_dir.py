from pathlib import Path

def make_new_ensemble_dir(ensemble_name):
    """
    Create a new directory for a standard ensemble.
    
    Args:
    - ensemble_name (str): Name of the ensemble.
    
    Returns:
    - ensemble_dir (str): Path to the newly created ensemble directory.
    """
    current_dir = Path.cwd()

    # Define the relative path to the "ensembles" directory
    relative_path = "ensembles"

    # If the current directory is not the root directory, go up one level and append "ensembles"
    if current_dir.match('*meta_tools'):
        ensembles_dir = current_dir.parent / relative_path
    else:
        ensembles_dir = current_dir  /relative_path

    ensemble_dir = ensembles_dir / ensemble_name
    
    try:
        ensemble_dir.mkdir(parents=True, exist_ok=False)
        print(f"Created new ensemble directory: {ensemble_dir}")
    except FileExistsError:
        print(f"Ensemble directory already exists: {ensemble_dir}")
    
    # Create subdirectories
    subdirs = [
        "configs",
        "artifacts",
        "notebooks",
        "reports",
        "data/generated",
        "data/processed",
        "src/dataloaders",
        "src/architectures",
        "src/utils",
        "src/visualization",
        "src/offline_evaluation",
        "src/forecasting",
        "src/management"
    ]
    
    for subdir in subdirs:
        subdir_path = ensemble_dir / subdir
        subdir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created subdirectory: {subdir_path}")
    
    # Create README.md and requirements.txt
    readme_path = ensemble_dir / "README.md"
    with open(readme_path, "w") as readme_file:
        readme_file.write("# Model README\n")
    print(f"Created README.md: {readme_path}")
    
    requirements_path = ensemble_dir / "requirements.txt"
    with open(requirements_path, "w") as requirements_file:
        requirements_file.write("# Requirements\n")
    print(f"Created requirements.txt: {requirements_path}")
    
    return ensemble_dir

if __name__ == "__main__":
    ensemble_name = input("Enter the name of the ensemble: ")
    make_new_ensemble_dir(ensemble_name)