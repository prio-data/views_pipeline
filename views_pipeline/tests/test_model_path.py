import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
from views_pipeline.managers.path_manager import ModelPath

@pytest.fixture
def temp_dir(tmp_path):
    """
    Fixture to create a temporary directory structure for testing.

    Args:
        tmp_path (Path): Temporary directory path provided by pytest.

    Returns:
        tuple: A tuple containing the project root directory and the model directory.
    """
    project_root = tmp_path / "views_pipeline"
    project_root.mkdir()
    (project_root / "LICENSE.md").touch()
    models_dir = project_root / "models"
    models_dir.mkdir()
    model_dir = models_dir / "test_model"
    model_dir.mkdir()
    # Create necessary subdirectories
    (model_dir / "src/architectures").mkdir(parents=True)
    (model_dir / "src/dataloaders").mkdir(parents=True)
    (model_dir / "src/forecasting").mkdir(parents=True)
    (model_dir / "src/management").mkdir(parents=True)
    (model_dir / "src/offline_evaluation").mkdir(parents=True)
    (model_dir / "src/online_evaluation").mkdir(parents=True)
    (model_dir / "src/training").mkdir(parents=True)
    (model_dir / "src/utils").mkdir(parents=True)
    (model_dir / "src/visualization").mkdir(parents=True)
    (model_dir / "artifacts").mkdir(parents=True)
    (model_dir / "configs").mkdir(parents=True)
    (model_dir / "data/generated").mkdir(parents=True)
    (model_dir / "data/processed").mkdir(parents=True)
    (model_dir / "data/raw").mkdir(parents=True)
    (model_dir / "notebooks").mkdir(parents=True)
    (model_dir / "reports").mkdir(parents=True)
    (project_root / "common_utils").mkdir(parents=True)
    (project_root / "common_configs").mkdir(parents=True)
    (project_root / "meta_tools/templates").mkdir(parents=True)
    (project_root / "common_querysets").mkdir(parents=True)
    return project_root, model_dir

def test_initialization_with_valid_name(temp_dir):
    """
    Test the initialization of ModelPath with a valid model name.

    Args:
        temp_dir (tuple): A tuple containing the project root directory and the model directory.
    """
    project_root, model_dir = temp_dir
    # Patch the class-level attributes and methods to use the temporary directory structure
    with patch.object(ModelPath, '_root', project_root):
        with patch.object(ModelPath, 'get_models', return_value=project_root / "models"):
            with patch('views_pipeline.managers.path_manager.ModelPath._get_model_dir', return_value=model_dir):
                # Initialize the ModelPath instance with a valid model name
                model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
                # Assert that the model name and directories are correctly set
                assert model_path_instance.model_name == "test_model"
                assert model_path_instance.root == project_root
                assert model_path_instance.model_dir == model_dir

def test_initialization_with_invalid_name(temp_dir):
    """
    Test the initialization of ModelPath with an invalid model name.

    Args:
        temp_dir (tuple): A tuple containing the project root directory and the model directory.
    """
    project_root, _ = temp_dir
    # Patch the class-level attributes and methods to use the temporary directory structure
    with patch.object(ModelPath, '_root', project_root):
        with patch.object(ModelPath, 'get_models', return_value=project_root / "models"):
            with patch('views_pipeline.managers.path_manager.ModelPath._get_model_dir', return_value=None):
                # Assert that initializing with an invalid model name raises a ValueError
                with pytest.raises(ValueError):
                    ModelPath(model_name_or_path="invalidmodel", validate=True)

def test_is_path(temp_dir):
    """
    Test the _is_path method to check if the input is a valid path.

    Args:
        temp_dir (tuple): A tuple containing the project root directory and the model directory.
    """
    project_root, _ = temp_dir
    # Initialize the ModelPath instance without validation
    model_path_instance = ModelPath(model_name_or_path="test_model", validate=False)
    # Assert that the project root is a valid path
    assert model_path_instance._is_path(project_root) == True
    # Assert that a non-existent path is not valid
    assert model_path_instance._is_path("non_existent_path") == False

def test_get_model_dir(temp_dir):
    """
    Test the _get_model_dir method to get the model directory.

    Args:
        temp_dir (tuple): A tuple containing the project root directory and the model directory.
    """
    project_root, model_dir = temp_dir
    # Patch the class-level attributes and methods to use the temporary directory structure
    with patch.object(ModelPath, '_root', project_root):
        with patch.object(ModelPath, 'get_models', return_value=project_root / "models"):
            with patch('views_pipeline.managers.path_manager.ModelPath._get_model_dir', return_value=model_dir):
                # Initialize the ModelPath instance with a valid model name
                model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
                # Assert that the _get_model_dir method returns the correct model directory
                assert model_path_instance._get_model_dir() == model_dir

def test_build_absolute_directory(temp_dir):
    """
    Test the _build_absolute_directory method to build an absolute directory path.

    Args:
        temp_dir (tuple): A tuple containing the project root directory and the model directory.
    """
    project_root, model_dir = temp_dir
    # Patch the class-level attributes and methods to use the temporary directory structure
    with patch.object(ModelPath, '_root', project_root):
        with patch.object(ModelPath, 'get_models', return_value=project_root / "models"):
            with patch('views_pipeline.managers.path_manager.ModelPath._get_model_dir', return_value=model_dir):
                # Initialize the ModelPath instance with a valid model name
                model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
                # Build an absolute directory path for "src/architectures"
                abs_dir = model_path_instance._build_absolute_directory(Path("src/architectures"))
                # Assert that the absolute directory path is correct
                assert abs_dir == model_dir / "src/architectures"

# def test_add_paths_to_sys(temp_dir):
#     """
#     Test the add_paths_to_sys method to add model paths to the system path.

#     Args:
#         temp_dir (tuple): A tuple containing the project root directory and the model directory.
#     """
#     project_root, model_dir = temp_dir
#     # Patch the class-level attributes and methods to use the temporary directory structure
#     with patch.object(ModelPath, '_root', project_root):
#         with patch.object(ModelPath, 'get_models', return_value=project_root / "models"):
#             with patch('views_pipeline.managers.path_manager.ModelPath._get_model_dir', return_value=model_dir):
#                 # Initialize the ModelPath instance with a valid model name
#                 model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
#                 # Add model paths to the system path
#                 model_path_instance.add_paths_to_sys()
#                 # Assert that the "src" directory is added to the system path
#                 assert str(model_path_instance.model_dir / "src") in sys.path

# def test_remove_paths_from_sys(temp_dir):
#     """
#     Test the remove_paths_from_sys method to remove model paths from the system path.

#     Args:
#         temp_dir (tuple): A tuple containing the project root directory and the model directory.
#     """
#     project_root, model_dir = temp_dir
#     # Patch the class-level attributes and methods to use the temporary directory structure
#     with patch.object(ModelPath, '_root', project_root):
#         with patch.object(ModelPath, 'get_models', return_value=project_root / "models"):
#             with patch('views_pipeline.managers.path_manager.ModelPath._get_model_dir', return_value=model_dir):
#                 # Initialize the ModelPath instance with a valid model name
#                 model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
#                 # Add model paths to the system path
#                 model_path_instance.add_paths_to_sys()
#                 # Remove model paths from the system path
#                 model_path_instance.remove_paths_from_sys()
#                 # Assert that the model directory is removed from the system path
#                 assert str(model_path_instance.model_dir) not in sys.path