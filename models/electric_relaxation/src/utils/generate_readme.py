from pathlib import Path
from utils.set_paths import set_paths

def generate_readme():
    """
    Generate a README file for the specified folder.
    The folder name is inferred from the parent folder of the script's parent folder (two levels up).
    """
    folder_name = Path(__file__).resolve().parent.parent.name
    readme_content = f"This is the README for {folder_name}."
    model_path = next(set_paths())  # Get the model directory path using set_paths function
    readme_path = model_path / folder_name / "README.md"
    with open(readme_path, "w") as readme_file:
        readme_file.write(readme_content)

if __name__ == "__main__":
    generate_readme()


