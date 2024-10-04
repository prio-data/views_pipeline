import pytest
from pathlib import Path
import sys
import importlib
from unittest.mock import patch, MagicMock

# ModelPath class is defined in utils_model_paths
PATH = Path(__file__)
sys.path.insert(
    0,
    str(
        Path(*[i for i in PATH.parts[: PATH.parts.index("views_pipeline") + 1]])
        / "common_utils"
    ),
)

from utils_model_paths import ModelPath


@pytest.fixture
def model_path():
    return ModelPath("purple_alien", validate=False)


def test_initialization(model_path):
    assert model_path.model_name == "purple_alien"
    assert model_path.validate is False
    assert isinstance(model_path.root, Path)
    assert isinstance(model_path.models, Path)


def test_directory_validation(model_path):
    with patch.object(Path, "exists", return_value=True):
        assert model_path._check_if_dir_exists(model_path.root) is True

    with patch.object(Path, "exists", return_value=False):
        assert model_path._check_if_dir_exists(model_path.root) is False


def test_add_paths_to_sys(model_path):
    initial_sys_path_length = len(sys.path)
    model_path.add_paths_to_sys()
    assert len(sys.path) > initial_sys_path_length
    model_path.remove_paths_from_sys()
    assert len(sys.path) == initial_sys_path_length


def test_get_directories(model_path):
    directories = model_path.get_directories()
    assert isinstance(directories, dict)
    assert "root" not in directories
    assert "model_dir" in directories


def test_get_scripts(model_path):
    scripts = model_path.get_scripts()
    assert isinstance(scripts, dict)
    assert "main.py" in scripts


if __name__ == "__main__":
    pytest.main()
