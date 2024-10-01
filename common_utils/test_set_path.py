import pytest
import sys
from pathlib import Path
from set_path import (
    setup_root_paths,
    setup_model_paths,
    setup_ensemble_paths,
    setup_project_paths,
    setup_data_paths,
    setup_artifacts_paths,
)


@pytest.fixture
def temp_path(tmp_path):
    """Fixture to create a temporary path for testing."""
    return tmp_path / "views_pipeline" / "models" / "test_model"


def test_setup_root_paths(temp_path):
    """
    Test extracting the root path up to and including the "views_pipeline" directory.

    Args:
        temp_path: Temporary path for testing.
    """
    temp_path.mkdir(parents=True)
    result = setup_root_paths(temp_path)
    assert result == temp_path.parent.parent


def test_setup_model_paths(temp_path):
    """
    Test extracting the model-specific path including the "models" directory and its immediate subdirectory.

    Args:
        temp_path: Temporary path for testing.
    """
    temp_path.mkdir(parents=True)
    result = setup_model_paths(temp_path)
    assert result == temp_path


def test_setup_model_paths_no_models(temp_path):
    """
    Test handling when the "models" directory is not present.

    Args:
        temp_path: Temporary path for testing.
    """
    temp_path = temp_path.parent.parent / "no_models"
    temp_path.mkdir(parents=True)
    result = setup_model_paths(temp_path)
    assert result is None


def test_setup_ensemble_paths(temp_path):
    """
    Test extracting the model-specific path including the "ensembles" directory and its immediate subdirectory.

    Args:
        temp_path: Temporary path for testing.
    """
    temp_path = temp_path.parent.parent / "ensembles" / "test_ensemble"
    temp_path.mkdir(parents=True)
    result = setup_ensemble_paths(temp_path)
    assert result == temp_path


def test_setup_ensemble_paths_no_ensembles(temp_path):
    """
    Test handling when the "ensembles" directory is not present.

    Args:
        temp_path: Temporary path for testing.
    """
    temp_path = temp_path.parent.parent / "no_ensembles"
    temp_path.mkdir(parents=True)
    result = setup_ensemble_paths(temp_path)
    assert result is None


def test_setup_project_paths(temp_path):
    """
    Test configuring project-wide access to common utilities, configurations, and model-specific paths by adjusting `sys.path`.

    Args:
        temp_path: Temporary path for testing.
    """
    temp_path.mkdir(parents=True)
    setup_project_paths(temp_path)
    expected_paths = [
        str(temp_path.parent.parent),
        str(temp_path.parent.parent / "common_utils"),
        str(temp_path.parent.parent / "common_configs"),
        str(temp_path.parent.parent / "common_querysets"),
        str(temp_path / "configs"),
        str(temp_path / "src" / "utils"),
        str(temp_path / "src" / "management"),
        str(temp_path / "src" / "architectures"),
        str(temp_path / "src" / "training"),
        str(temp_path / "src" / "forecasting"),
        str(temp_path / "src" / "offline_evaluation"),
        str(temp_path / "src" / "dataloaders"),
    ]
    print(sys.path)
    for path in expected_paths:
        print(path)
        assert path in sys.path


def test_setup_data_paths(temp_path):
    """
    Test returning the raw, processed, and generated data paths for the specified model.

    Args:
        temp_path: Temporary path for testing.
    """
    temp_path.mkdir(parents=True)
    raw, processed, generated = setup_data_paths(temp_path)
    assert raw == temp_path / "data" / "raw"
    assert processed == temp_path / "data" / "processed"
    assert generated == temp_path / "data" / "generated"


def test_setup_artifacts_paths(temp_path):
    """
    Test returning the paths for the artifacts for the specified model.

    Args:
        temp_path: Temporary path for testing.
    """
    temp_path.mkdir(parents=True)
    result = setup_artifacts_paths(temp_path)
    assert result == temp_path / "artifacts"
