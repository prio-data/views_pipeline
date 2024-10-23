import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from model_path import ModelPath

@pytest.fixture
def temp_dir(tmp_path):
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
    project_root, model_dir = temp_dir
    with patch.object(ModelPath, '_root', project_root):
        with patch.object(ModelPath, '_models', project_root / "models"):
            with patch('model_path.ModelPath._get_model_dir', return_value=model_dir):
                model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
                assert model_path_instance.model_name == "test_model"
                assert model_path_instance.root == project_root
                assert model_path_instance.model_dir == model_dir

def test_initialization_with_invalid_name(temp_dir):
    project_root, _ = temp_dir
    with patch.object(ModelPath, '_root', project_root):
        with patch.object(ModelPath, '_models', project_root / "models"):
            with patch('model_path.ModelPath._get_model_dir', return_value=None):
                with pytest.raises(ValueError):
                    ModelPath(model_name_or_path="invalidmodel", validate=True)

def test_is_path(temp_dir):
    project_root, _ = temp_dir
    model_path_instance = ModelPath(model_name_or_path="test_model", validate=False)
    assert model_path_instance._is_path(project_root) == True
    assert model_path_instance._is_path("non_existent_path") == False

def test_get_model_dir(temp_dir):
    project_root, model_dir = temp_dir
    with patch.object(ModelPath, '_root', project_root):
        with patch.object(ModelPath, '_models', project_root / "models"):
            with patch('model_path.ModelPath._get_model_dir', return_value=model_dir):
                model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
                assert model_path_instance._get_model_dir() == model_dir

def test_build_absolute_directory(temp_dir):
    project_root, model_dir = temp_dir
    with patch.object(ModelPath, '_root', project_root):
        with patch.object(ModelPath, '_models', project_root / "models"):
            with patch('model_path.ModelPath._get_model_dir', return_value=model_dir):
                model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
                abs_dir = model_path_instance._build_absolute_directory(Path("src/architectures"))
                assert abs_dir == model_dir / "src/architectures"

def test_add_paths_to_sys(temp_dir):
    project_root, model_dir = temp_dir
    with patch.object(ModelPath, '_root', project_root):
        with patch.object(ModelPath, '_models', project_root / "models"):
            with patch('model_path.ModelPath._get_model_dir', return_value=model_dir):
                model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
                model_path_instance.add_paths_to_sys()
                assert str(model_path_instance.model_dir / "src") in sys.path

def test_remove_paths_from_sys(temp_dir):
    project_root, model_dir = temp_dir
    with patch.object(ModelPath, '_root', project_root):
        with patch.object(ModelPath, '_models', project_root / "models"):
            with patch('model_path.ModelPath._get_model_dir', return_value=model_dir):
                model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
                model_path_instance.add_paths_to_sys()
                model_path_instance.remove_paths_from_sys()
                assert str(model_path_instance.model_dir) not in sys.path

def test_view_directories(temp_dir, capsys):
    project_root, model_dir = temp_dir
    with patch.object(ModelPath, '_root', project_root):
        with patch.object(ModelPath, '_models', project_root / "models"):
            with patch('model_path.ModelPath._get_model_dir', return_value=model_dir):
                model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
                model_path_instance.view_directories()
                captured = capsys.readouterr()
                assert "Name" in captured.out
                assert "Path" in captured.out

def test_view_scripts(temp_dir, capsys):
    project_root, model_dir = temp_dir
    with patch.object(ModelPath, '_root', project_root):
        with patch.object(ModelPath, '_models', project_root / "models"):
            with patch('model_path.ModelPath._get_model_dir', return_value=model_dir):
                model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
                model_path_instance.view_scripts()
                captured = capsys.readouterr()
                assert "Script" in captured.out
                assert "Path" in captured.out

def test_get_directories(temp_dir):
    project_root, model_dir = temp_dir
    with patch.object(ModelPath, '_root', project_root):
        with patch.object(ModelPath, '_models', project_root / "models"):
            with patch('model_path.ModelPath._get_model_dir', return_value=model_dir):
                model_path_instance = ModelPath(model_name_or_path="test_model", validate=True)
                directories = model_path_instance.get_directories()
                assert "architectures" in directories
                assert directories["architectures"] == str(model_dir / "src/architectures")

def test_get_scripts(temp_dir):
    project_root, model_dir = temp_dir
    with patch.object(ModelPath, '_root', project_root):
        with patch.object(ModelPath, '_models', project_root / "models"):
            with patch('model_path.ModelPath._get_model_dir', return_value=model_dir):
                model_path_instance = ModelPath(model_name_or_path="test_model", validate=False)
                scripts = model_path_instance.get_scripts()
                assert "main.py" in scripts
                assert scripts["main.py"] == str(model_dir / "main.py")