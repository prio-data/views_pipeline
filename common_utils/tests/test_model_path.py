import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from model_path import ModelPath

@pytest.fixture
def temp_dir(tmp_path):
    """
    Fixture to create a temporary directory structure for testing.

    Args:
        tmp_path (pathlib.Path): Temporary directory provided by pytest.

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
        temp_dir (tuple): Fixture providing the project root and model directory.

    Asserts:
        The model name, root directory, and model directory are correctly set.
    """
    project_root, model_dir = temp_dir
    with patch('model_path.utils_model_paths.find_project_root', return_value=project_root):
        with patch('model_path.utils_model_naming.validate_model_name', return_value=True):
            model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
            assert model_path_instance.model_name == "test_model"
            assert model_path_instance.root == project_root
            assert model_path_instance.model_dir == model_dir

def test_initialization_with_invalid_name(temp_dir):
    """
    Test the initialization of ModelPath with an invalid model name.

    Args:
        temp_dir (tuple): Fixture providing the project root and model directory.

    Asserts:
        A ValueError is raised when an invalid model name is provided.
    """
    project_root, _ = temp_dir
    with patch('model_path.utils_model_paths.find_project_root', return_value=project_root):
        with patch('model_path.utils_model_naming.validate_model_name', return_value=False):
            with pytest.raises(ValueError):
                ModelPath(model_name_or_path="invalid_model", validate=True)

def test_is_path(temp_dir):
    """
    Test the _is_path method of ModelPath.

    Args:
        temp_dir (tuple): Fixture providing the project root and model directory.

    Asserts:
        The _is_path method correctly identifies existing and non-existing paths.
    """
    project_root, _ = temp_dir
    model_path_instance = ModelPath(model_name_or_path="test_model", validate=False)
    assert model_path_instance._is_path(project_root) == True
    assert model_path_instance._is_path("non_existent_path") == False

def test_get_model_dir(temp_dir):
    """
    Test the _get_model_dir method of ModelPath.

    Args:
        temp_dir (tuple): Fixture providing the project root and model directory.

    Asserts:
        The _get_model_dir method returns the correct model directory.
    """
    project_root, model_dir = temp_dir
    with patch('model_path.utils_model_paths.find_project_root', return_value=project_root):
        model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
        assert model_path_instance._get_model_dir() == model_dir

def test_build_absolute_directory(temp_dir):
    """
    Test the _build_absolute_directory method of ModelPath.

    Args:
        temp_dir (tuple): Fixture providing the project root and model directory.

    Asserts:
        The _build_absolute_directory method returns the correct absolute directory path.
    """
    project_root, model_dir = temp_dir
    with patch('model_path.utils_model_paths.find_project_root', return_value=project_root):
        model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
        abs_dir = model_path_instance._build_absolute_directory(Path("src/architectures"))
        assert abs_dir == model_dir / "src/architectures"

def test_add_paths_to_sys(temp_dir):
    """
    Test the add_paths_to_sys method of ModelPath.

    Args:
        temp_dir (tuple): Fixture providing the project root and model directory.

    Asserts:
        The add_paths_to_sys method correctly adds the model's src directory to sys.path.
    """
    project_root, model_dir = temp_dir
    with patch('model_path.utils_model_paths.find_project_root', return_value=project_root):
        model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
        model_path_instance.add_paths_to_sys()
        assert str(model_path_instance.model_dir / "src") in sys.path

def test_remove_paths_from_sys(temp_dir):
    """
    Test the remove_paths_from_sys method of ModelPath.

    Args:
        temp_dir (tuple): Fixture providing the project root and model directory.

    Asserts:
        The remove_paths_from_sys method correctly removes the model's directory from sys.path.
    """
    project_root, model_dir = temp_dir
    with patch('model_path.utils_model_paths.find_project_root', return_value=project_root):
        model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
        model_path_instance.add_paths_to_sys()
        model_path_instance.remove_paths_from_sys()
        assert str(model_path_instance.model_dir) not in sys.path

def test_view_directories(temp_dir, capsys):
    """
    Test the view_directories method of ModelPath.

    Args:
        temp_dir (tuple): Fixture providing the project root and model directory.
        capsys (pytest.CaptureFixture): Pytest fixture to capture stdout and stderr.

    Asserts:
        The view_directories method correctly prints the directory names and paths.
    """
    project_root, model_dir = temp_dir
    with patch('model_path.utils_model_paths.find_project_root', return_value=project_root):
        model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
        model_path_instance.view_directories()
        captured = capsys.readouterr()
        assert "Name" in captured.out
        assert "Path" in captured.out

def test_view_scripts(temp_dir, capsys):
    """
    Test the view_scripts method of ModelPath.

    Args:
        temp_dir (tuple): Fixture providing the project root and model directory.
        capsys (pytest.CaptureFixture): Pytest fixture to capture stdout and stderr.

    Asserts:
        The view_scripts method correctly prints the script names and paths.
    """
    project_root, model_dir = temp_dir
    with patch('model_path.utils_model_paths.find_project_root', return_value=project_root):
        model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
        model_path_instance.view_scripts()
        captured = capsys.readouterr()
        assert "Script" in captured.out
        assert "Path" in captured.out

def test_get_directories(temp_dir):
    """
    Test the get_directories method of ModelPath.

    Args:
        temp_dir (tuple): Fixture providing the project root and model directory.

    Asserts:
        The get_directories method returns a dictionary with the correct directory paths.
    """
    project_root, model_dir = temp_dir
    with patch('model_path.utils_model_paths.find_project_root', return_value=project_root):
        model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
        directories = model_path_instance.get_directories()
        assert "architectures" in directories
        assert directories["architectures"] == str(model_dir / "src/architectures")

def test_get_scripts(temp_dir):
    """
    Test the get_scripts method of ModelPath.

    Args:
        temp_dir (tuple): Fixture providing the project root and model directory.

    Asserts:
        The get_scripts method returns a dictionary with the correct script paths.
    """
    project_root, model_dir = temp_dir
    with patch('model_path.utils_model_paths.find_project_root', return_value=project_root):
        model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
        scripts = model_path_instance.get_scripts()
        assert "main.py" in scripts
        assert scripts["main.py"] == str(model_dir / "main.py")