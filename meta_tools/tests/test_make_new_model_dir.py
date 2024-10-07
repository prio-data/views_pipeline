import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "meta_tools"))
from make_new_model_dir import ModelDirectoryBuilder


@pytest.fixture
def mock_validate_model_name():
    """
    Fixture to mock the `validate_model_name` function in the `make_new_model_dir` module.

    This fixture uses the `patch` function from the `unittest.mock` module to replace
    the `validate_model_name` function with a mock object for the duration of the test.

    Yields:
        mock (Mock): The mock object that replaces `validate_model_name`.
    """
    with patch("make_new_model_dir.validate_model_name") as mock:
        yield mock


@pytest.fixture
def mock_find_project_root():
    """
    Fixture to mock the `find_project_root` function from the `make_new_model_dir` module.

    This fixture uses the `patch` function from the `unittest.mock` module to replace
    the `find_project_root` function with a mock object for the duration of the test.

    Yields:
        mock (Mock): The mock object that replaces `find_project_root`.
    """
    with patch("make_new_model_dir.find_project_root") as mock:
        yield mock


@pytest.fixture
def temp_model_dir(tmp_path):
    """
    Fixture that provides a temporary directory for model testing.

    This fixture creates a temporary directory under the "models" directory
    with the name "test_model". The directory is created using the `tmp_path`
    fixture provided by pytest, which ensures that the directory is unique
    and automatically cleaned up after the test session.

    Returns:
        pathlib.Path: Path to the temporary model directory.
    """
    return tmp_path / "models" / "test_model"


def test_init_valid_model_name(
    mock_validate_model_name, mock_find_project_root, temp_model_dir
):
    """
    Test the initialization of ModelDirectoryBuilder with a valid model name.

    This test verifies that the ModelDirectoryBuilder correctly initializes
    with a given model name and sets the appropriate model directory.

    Args:
        mock_validate_model_name (Mock): Mock object for the validate_model_name function.
        mock_find_project_root (Mock): Mock object for the find_project_root function.
        temp_model_dir (Path): Temporary directory path for the model directory.

    Assertions:
        - The model_name attribute of the builder should be set to "test_model".
        - The model_dir attribute of the builder should be set to temp_model_dir.
    """
    mock_validate_model_name.return_value = True
    mock_find_project_root.return_value = temp_model_dir.parent.parent

    builder = ModelDirectoryBuilder("test_model")
    assert builder.model_name == "test_model"
    assert builder.model_dir == temp_model_dir


def test_init_invalid_model_name(mock_validate_model_name):
    """
    Test the initialization of ModelDirectoryBuilder with an invalid model name.

    This test ensures that when an invalid model name is provided, the
    ModelDirectoryBuilder raises a ValueError. The validation of the model
    name is mocked to return False, simulating an invalid model name scenario.

    Args:
        mock_validate_model_name (Mock): A mock object for the model name
        validation function, set to return False.

    Raises:
        ValueError: If the model name is invalid.
    """
    mock_validate_model_name.return_value = False

    with pytest.raises(ValueError):
        ModelDirectoryBuilder("invalidmodel")


def test_build_model_directory_creates_directories(
    mock_validate_model_name, mock_find_project_root, temp_model_dir
):
    """
    Test that the build_model_directory method of ModelDirectoryBuilder creates the expected directories.

    Args:
        mock_validate_model_name (Mock): Mock object for the validate_model_name method.
        mock_find_project_root (Mock): Mock object for the find_project_root method.
        temp_model_dir (Path): Temporary directory path for the model.

    Asserts:
        The created model directory matches the temporary model directory.
        Each expected subdirectory exists within the created model directory.
    """
    mock_validate_model_name.return_value = True
    mock_find_project_root.return_value = temp_model_dir.parent.parent

    builder = ModelDirectoryBuilder("test_model")
    created_model_dir = builder.build_model_directory()

    assert created_model_dir == temp_model_dir
    for subdir in builder.subdirs:
        assert (temp_model_dir / subdir).exists()


def test_build_model_directory_existing_directory(
    mock_validate_model_name, mock_find_project_root, temp_model_dir
):
    """
    Test the `build_model_directory` method of `ModelDirectoryBuilder` when the directory already exists.

    This test ensures that the `build_model_directory` method correctly identifies and uses an existing model directory.

    Args:
        mock_validate_model_name (Mock): Mock object for the `validate_model_name` method.
        mock_find_project_root (Mock): Mock object for the `find_project_root` method.
        temp_model_dir (Path): Temporary directory path for the model directory.

    Assertions:
        Asserts that the created model directory is the same as the temporary model directory.
    """
    mock_validate_model_name.return_value = True
    mock_find_project_root.return_value = temp_model_dir.parent.parent

    temp_model_dir.mkdir(parents=True)
    builder = ModelDirectoryBuilder("test_model")
    created_model_dir = builder.build_model_directory()

    assert created_model_dir == temp_model_dir


def test_assess_model_directory(
    mock_validate_model_name, mock_find_project_root, temp_model_dir
):
    """
    Test the assessment of a model directory.

    This test verifies that the ModelDirectoryBuilder correctly assesses the
    structure of a newly created model directory.

    Args:
        mock_validate_model_name (Mock): Mock object for the model name validation function.
        mock_find_project_root (Mock): Mock object for the function that finds the project root.
        temp_model_dir (Path): Temporary directory path for the model directory.

    Asserts:
        The model directory path is correctly set.
        There are no structure errors in the assessed model directory.
    """
    mock_validate_model_name.return_value = True
    mock_find_project_root.return_value = temp_model_dir.parent.parent

    builder = ModelDirectoryBuilder("test_model")
    builder.build_model_directory()
    assessment = builder.assess_model_directory()

    assert assessment["model_dir"] == temp_model_dir
    assert not assessment["structure_errors"]
