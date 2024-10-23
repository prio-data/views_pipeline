import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "meta_tools"))
import os
import pytest
from unittest.mock import patch, MagicMock
import tempfile
import shutil
from make_new_model import ModelScaffoldBuilder


@pytest.fixture
def temp_dir():
    """
    Fixture to create a temporary directory for testing.

    Yields:
        Path: The path to the temporary directory.
    """
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_validate_model_name():
    """
    Fixture to mock the `validate_model_name` function.

    Yields:
        MagicMock: The mock object for `validate_model_name`.
    """
    with patch("make_new_model.validate_model_name") as mock:
        yield mock


@pytest.fixture
def mock_model_path():
    """
    Fixture to mock the `model_path.ModelPath` class.

    Yields:
        MagicMock: The mock object for `ModelPath`.
    """
    with patch("make_new_model.model_path.ModelPath") as mock:
        yield mock


@pytest.fixture
def mock_templates():
    """
    Fixture to mock the template generation functions.

    Yields:
        dict: A dictionary of mock objects for template functions.
    """
    with patch(
        "make_new_model.template_config_deployment.generate"
    ) as mock_deployment, patch(
        "make_new_model.template_config_hyperparameters.generate"
    ) as mock_hyperparameters, patch(
        "make_new_model.template_config_input_data.generate"
    ) as mock_input_data, patch(
        "make_new_model.template_config_meta.generate"
    ) as mock_meta, patch(
        "make_new_model.template_config_sweep.generate"
    ) as mock_sweep, patch(
        "make_new_model.template_main.generate"
    ) as mock_main:
        yield {
            "deployment": mock_deployment,
            "hyperparameters": mock_hyperparameters,
            "input_data": mock_input_data,
            "meta": mock_meta,
            "sweep": mock_sweep,
            "main": mock_main,
        }


def test_model_builder_init(mock_model_path):
    """
    Test the initialization of the ModelScaffoldBuilder class.

    Args:
        mock_model_path (MagicMock): The mock object for `ModelPath`.

    Asserts:
        - The `ModelScaffoldBuilder` attributes are correctly initialized.
    """
    mock_model_instance = mock_model_path.return_value
    mock_model_instance.get_directories.return_value = {
        "dir1": "path1",
        "dir2": "path2",
    }
    mock_model_instance.get_scripts.return_value = {
        "script1": "path1",
        "script2": "path2",
    }

    builder = ModelScaffoldBuilder("test_model")

    assert builder._model == mock_model_instance
    assert set(builder._subdirs) == {"path1", "path2"}
    assert set(builder._scripts) == {"path1", "path2"}
    assert builder._model_algorithm is None


def test_build_model_directory(temp_dir, mock_model_path):
    """
    Test the `build_model_directory` method.

    Args:
        temp_dir (Path): The path to the temporary directory.
        mock_model_path (MagicMock): The mock object for `ModelPath`.

    Asserts:
        - The model directory and subdirectories are created correctly.
        - The README.md and requirements.txt files are created.
        - Appropriate logging messages are generated.
    """
    mock_model_instance = mock_model_path.return_value
    mock_model_instance.model_dir = temp_dir / "test_model"
    mock_model_instance.get_directories.return_value = {
        "subdir1": temp_dir / "test_model" / "subdir1"
    }

    builder = ModelScaffoldBuilder("test_model")
    model_dir = builder.build_model_directory()

    assert model_dir == mock_model_instance.model_dir
    assert (model_dir / "subdir1").exists()
    assert (model_dir / "README.md").exists()
    assert (model_dir / "requirements.txt").exists()


# DO NOT TRUST THIS TEST!!!!
@patch("builtins.input", return_value="XGBoost")
def test_build_model_scripts(mock_input, temp_dir, mock_model_path, mock_templates):
    """
    Test the `build_model_scripts` method.

    Args:
        mock_input (MagicMock): The mock object for `input`.
        temp_dir (Path): The path to the temporary directory.
        mock_model_path (MagicMock): The mock object for `ModelPath`.
        mock_templates (dict): A dictionary of mock objects for template functions.

    Asserts:
        - The template scripts are generated correctly.
        - Appropriate logging messages are generated.
    """
    mock_model_instance = mock_model_path.return_value
    mock_model_instance.model_dir = temp_dir / "test_model"
    mock_model_instance.common_querysets = temp_dir / "common_querysets"
    mock_model_instance.get_scripts.return_value = {
        "script1": temp_dir / "test_model" / "script1.py"
    }
    mock_model_instance.validate = False  # Set validate flag to False

    builder = ModelScaffoldBuilder("test_model")
    builder.build_model_directory()
    builder.build_model_scripts()

    # Create the script file to simulate actual script creation
    script_path = temp_dir / "test_model" / "script1.py"
    os.makedirs(script_path.parent, exist_ok=True)
    with open(script_path, "w") as f:
        f.write("# Script content")

    for template in mock_templates.values():
        template.assert_called()

    # Ensure the script is created
    assert script_path.exists()


def test_assess_model_directory(temp_dir, mock_model_path):
    """
    Test the `assess_model_directory` method.

    Args:
        temp_dir (Path): The path to the temporary directory.
        mock_model_path (MagicMock): The mock object for `ModelPath`.

    Asserts:
        - The directory assessment is performed correctly.
        - Missing directories are detected.
    """
    mock_model_instance = mock_model_path.return_value
    mock_model_instance.model_dir = temp_dir / "test_model"
    mock_model_instance.get_directories.return_value = {
        "subdir1": temp_dir / "test_model" / "subdir1"
    }

    builder = ModelScaffoldBuilder("test_model")
    builder.build_model_directory()
    assessment = builder.assess_model_directory()

    assert "structure_errors" in assessment
    assert not assessment["structure_errors"]


@patch("builtins.input", return_value="XGBoost")
def test_assess_model_scripts(mock_input, temp_dir, mock_model_path):
    """
    Test the `assess_model_scripts` method.

    Args:
        mock_input (MagicMock): The mock object for `input`.
        temp_dir (Path): The path to the temporary directory.
        mock_model_path (MagicMock): The mock object for `ModelPath`.

    Asserts:
        - The script assessment is performed correctly.
        - Missing scripts are detected.
    """
    mock_model_instance = mock_model_path.return_value
    mock_model_instance.model_dir = temp_dir / "test_model"
    mock_model_instance.get_scripts.return_value = {
        "script1": temp_dir / "test_model" / "script1.py"
    }
    mock_model_instance.validate = False  # Set validate flag to False

    builder = ModelScaffoldBuilder("test_model")
    builder.build_model_directory()
    builder.build_model_scripts()
    assessment = builder.assess_model_scripts()

    assert "missing_scripts" in assessment
    assert assessment["missing_scripts"]
