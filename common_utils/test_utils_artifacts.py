import pytest
from pathlib import Path
from utils_artifacts import get_artifact_files, get_latest_model_artifact


@pytest.fixture
def temp_dir(tmp_path):
    """Fixture to create a temporary directory for testing."""
    return tmp_path


@pytest.fixture
def setup_artifact_files(temp_dir):
    """Fixture to set up artifact files for testing."""
    run_type = "calibration"
    extensions = [
        ".pt",
        ".pth",
        ".h5",
        ".hdf5",
        ".pkl",
        ".json",
        ".bst",
        ".txt",
        ".bin",
        ".cbm",
        ".onnx",
    ]
    filenames = [f"{run_type}_model_20210831_123456{ext}" for ext in extensions] + [
        f"{run_type}_model_20210901_123456{ext}" for ext in extensions
    ]
    for filename in filenames:
        (temp_dir / filename).touch()
    return temp_dir


def test_get_artifact_files(setup_artifact_files):
    """
    Test retrieving artifact files with valid run type and common extensions.

    Args:
        setup_artifact_files: Fixture to set up artifact files for testing.
    """
    run_type = "calibration"
    result = get_artifact_files(setup_artifact_files, run_type)
    assert len(result) == 22  # 11 extensions * 2 timestamps
    for file in result:
        assert file.stem.startswith(f"{run_type}_model_")
        assert file.suffix in [
            ".pt",
            ".pth",
            ".h5",
            ".hdf5",
            ".pkl",
            ".json",
            ".bst",
            ".txt",
            ".bin",
            ".cbm",
            ".onnx",
        ]


def test_get_artifact_files_no_match(temp_dir):
    """
    Test handling when no files match the run type and common extensions.

    Args:
        temp_dir: Temporary directory for testing.
    """
    run_type = "calibration"
    result = get_artifact_files(temp_dir, run_type)
    assert result == []


def test_get_latest_model_artifact(setup_artifact_files):
    """
    Test retrieving the latest model artifact based on modification time.

    Args:
        setup_artifact_files: Fixture to set up artifact files for testing.
    """
    run_type = "calibration"
    result = get_latest_model_artifact(setup_artifact_files, run_type)
    assert result.stem.startswith(f"{run_type}_model_20210901_123456")


def test_get_latest_model_artifact_no_files(temp_dir):
    """
    Test raising FileNotFoundError when no model artifacts are found for the given run type.

    Args:
        temp_dir: Temporary directory for testing.
    """
    run_type = "calibration"
    with pytest.raises(FileNotFoundError):
        get_latest_model_artifact(temp_dir, run_type)
