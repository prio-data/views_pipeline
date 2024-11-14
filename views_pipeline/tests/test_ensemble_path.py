import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
from views_pipeline.managers.path_manager import EnsemblePath

@pytest.fixture
def temp_dir(tmp_path):
    """
    Fixture to create a temporary directory structure for testing.

    Args:
        tmp_path (Path): Temporary directory path provided by pytest.

    Returns:
        tuple: A tuple containing the project root directory and the ensemble directory.
    """
    project_root = tmp_path / "views_pipeline"
    project_root.mkdir()
    (project_root / "LICENSE.md").touch()
    ensembles_dir = project_root / "ensembles"
    ensembles_dir.mkdir()
    ensemble_dir = ensembles_dir / "test_ensemble"
    ensemble_dir.mkdir()
    return project_root, ensemble_dir

def test_initialization_with_valid_name(temp_dir):
    """
    Test the initialization of EnsemblePath with a valid ensemble name.

    Args:
        temp_dir (tuple): A tuple containing the project root directory and the ensemble directory.
    """
    project_root, ensemble_dir = temp_dir
    # Patch the class-level attributes and methods to use the temporary directory structure
    with patch.object(EnsemblePath, '_root', project_root):
        with patch.object(EnsemblePath, 'get_models', return_value=project_root / "ensembles"):
            with patch('views_pipeline.managers.path_manager.EnsemblePath._get_model_dir', return_value=ensemble_dir):
                # Initialize the EnsemblePath instance with a valid ensemble name
                ensemble_path_instance = EnsemblePath(ensemble_name_or_path="test_ensemble", validate=True)
                # Assert that the ensemble name and directories are correctly set
                assert ensemble_path_instance.model_name == "test_ensemble"
                assert ensemble_path_instance.root == project_root
                assert ensemble_path_instance.model_dir == ensemble_dir

def test_initialization_with_invalid_name(temp_dir):
    """
    Test the initialization of EnsemblePath with an invalid ensemble name.

    Args:
        temp_dir (tuple): A tuple containing the project root directory and the ensemble directory.
    """
    project_root, _ = temp_dir
    # Patch the class-level attributes and methods to use the temporary directory structure
    with patch.object(EnsemblePath, '_root', project_root):
        with patch.object(EnsemblePath, 'get_models', return_value=project_root / "ensembles"):
            with patch('views_pipeline.managers.path_manager.EnsemblePath._get_model_dir', return_value=None):
                # Assert that initializing with an invalid ensemble name raises a ValueError
                with pytest.raises(ValueError):
                    EnsemblePath(ensemble_name_or_path="invalidensemble", validate=True)