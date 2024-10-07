from pathlib import Path


def find_project_root(marker="LICENSE.md") -> Path:
    """
    Finds the base directory of the project by searching for a specific marker file or directory.
    Args:
        marker (str): The name of the marker file or directory that indicates the project root.
                    Defaults to 'LICENSE.md'.
    Returns:
        Path: The path of the project root directory.
    Raises:
        FileNotFoundError: If the marker file/directory is not found up to the root directory.
    """
    # Start from the current directory and move up the hierarchy
    current_path = Path(__file__).resolve().parent
    while current_path != current_path.parent:  # Loop until we reach the root directory
        if (current_path / marker).exists():
            return current_path
        current_path = current_path.parent
    raise FileNotFoundError(
        f"{marker} not found in the directory hierarchy. Unable to find project root."
    )
