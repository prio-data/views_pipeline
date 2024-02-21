import os

def make_new_ensemble_dir(ensemble_name):
    """
    Create a new directory for a standard ensemble.
    
    Args:
    - ensemble_name (str): Name of the ensemble.
    
    Returns:
    - ensemble_dir (str): Path to the newly created ensemble directory.
    """
    ensembles_dir = "ensembles"
    ensemble_dir = os.path.join(ensembles_dir, ensemble_name)
    
    try:
        os.makedirs(ensemble_dir)
        print(f"Created new ensemble directory: {ensemble_dir}")
    except FileExistsError:
        print(f"Ensemble directory already exists: {ensemble_dir}")
    
    # Create subdirectories
    subdirs = [
        "configs",
        "artifacts",
        "notebooks",
        "reports/plots",
        "reports/figures",
        "reports/timelapse",
        "reports/papers",
        "reports/slides",
        "src/dataloaders",
        "src/architecture",
        "src/utils",
        "src/visualization",
        "src/training",
        "src/offline_evaluation",
        "src/online_evaluation",
        "src/drift_detection",
        "src/forecasting"
    ]
    
    for subdir in subdirs:
        subdir_path = os.path.join(ensemble_dir, subdir)
        os.makedirs(subdir_path, exist_ok=True)
        print(f"Created subdirectory: {subdir_path}")
    
    # Create README.md and requirements.txt
    readme_path = os.path.join(ensemble_dir, "README.md")
    with open(readme_path, "w") as readme_file:
        readme_file.write("# Model README\n")
    print(f"Created README.md: {readme_path}")
    
    requirements_path = os.path.join(ensemble_dir, "requirements.txt")
    with open(requirements_path, "w") as requirements_file:
        requirements_file.write("# Requirements\n")
    print(f"Created requirements.txt: {requirements_path}")
    
    return ensemble_dir

if __name__ == "__main__":
    ensemble_name = input("Enter the name of the ensemble: ")
    make_new_ensemble_dir(ensemble_name)
