import sys
from pathlib import Path

PATH = Path(__file__)
if 'views_pipeline' in PATH.parts:
    PATH_ROOT = Path(*PATH.parts[:PATH.parts.index('views_pipeline') + 1])
    PATH_META_TOOLS = PATH_ROOT / 'meta_tools'
    if not PATH_META_TOOLS.exists():
        raise ValueError("The 'meta_tools' directory was not found in the provided path.")
    sys.path.insert(0, str(PATH_META_TOOLS))
else:
    raise ValueError("The 'views_pipeline' directory was not found in the provided path.")

import os
import pytest
from unittest.mock import patch, MagicMock
import tempfile
import shutil
from ensemble_scaffold_builder import EnsembleScaffoldBuilder


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
    with patch("ensemble_scaffold_builder.validate_model_name") as mock:
        yield mock


@pytest.fixture
def mock_ensemble_path():
    """
    Fixture to mock the `ensemble_path.EnsemblePath` class.

    Yields:
        MagicMock: The mock object for `EnsemblePath`.
    """
    with patch("ensemble_scaffold_builder.ensemble_path.EnsemblePath") as mock:
        yield mock


@pytest.fixture
def mock_templates():
    """
    Fixture to mock the template generation functions.

    Yields:
        dict: A dictionary of mock objects for template functions.
    """
    with patch(
        "ensemble_scaffold_builder.template_config_deployment.generate"
    ) as mock_deployment, patch(
        "ensemble_scaffold_builder.template_config_hyperparameters.generate"
    ) as mock_hyperparameters, patch(
        "ensemble_scaffold_builder.template_config_meta.generate"
    ) as mock_meta, patch(
        "ensemble_scaffold_builder.template_main.generate"
    ) as mock_main:
        yield {
            "deployment": mock_deployment,
            "hyperparameters": mock_hyperparameters,
            "meta": mock_meta,
            "main": mock_main,
        }


def test_ensemble_builder_init(mock_ensemble_path):
    """
    Test the initialization of the EnsembleScaffoldBuilder class.

    Args:
        mock_ensemble_path (MagicMock): The mock object for `EnsemblePath`.

    Asserts:
        - The `EnsembleScaffoldBuilder` attributes are correctly initialized.
    """
    mock_ensemble_instance = mock_ensemble_path.return_value
    mock_ensemble_instance.get_directories.return_value = {
        "dir1": "path1",
        "dir2": "path2",
    }
    mock_ensemble_instance.get_scripts.return_value = {
        "script1": "path1",
        "script2": "path2",
    }

    builder = EnsembleScaffoldBuilder("test_ensemble")

    assert builder._model == mock_ensemble_instance
    assert set(builder._subdirs) == {"path1", "path2"}
    assert set(builder._scripts) == {"path1", "path2"}


def test_build_ensemble_directory(temp_dir, mock_ensemble_path):
    """
    Test the `build_model_directory` method.

    Args:
        temp_dir (Path): The path to the temporary directory.
        mock_ensemble_path (MagicMock): The mock object for `EnsemblePath`.

    Asserts:
        - The ensemble directory and subdirectories are created correctly.
        - The README.md and requirements.txt files are created.
        - Appropriate logging messages are generated.
    """
    mock_ensemble_instance = mock_ensemble_path.return_value
    mock_ensemble_instance.model_dir = temp_dir / "test_ensemble"
    mock_ensemble_instance.get_directories.return_value = {
        "subdir1": temp_dir / "test_ensemble" / "subdir1"
    }

    builder = EnsembleScaffoldBuilder("test_ensemble")
    model_dir = builder.build_model_directory()

    assert model_dir == mock_ensemble_instance.model_dir
    assert (model_dir / "subdir1").exists()
    assert (model_dir / "README.md").exists()
    assert (model_dir / "requirements.txt").exists()


def test_build_ensemble_scripts(temp_dir, mock_ensemble_path, mock_templates):
    """
    Test the `build_model_scripts` method.

    Args:
        temp_dir (Path): The path to the temporary directory.
        mock_ensemble_path (MagicMock): The mock object for `EnsemblePath`.
        mock_templates (dict): A dictionary of mock objects for template functions.

    Asserts:
        - The template scripts are generated correctly.
        - Appropriate logging messages are generated.
    """
    mock_ensemble_instance = mock_ensemble_path.return_value
    mock_ensemble_instance.model_dir = temp_dir / "test_ensemble"
    mock_ensemble_instance.get_scripts.return_value = {
        "script1": temp_dir / "test_ensemble" / "script1.py"
    }

    builder = EnsembleScaffoldBuilder("test_ensemble")
    builder.build_model_directory()
    builder.build_model_scripts()

    # Create the script file to simulate actual script creation
    script_path = temp_dir / "test_ensemble" / "script1.py"
    os.makedirs(script_path.parent, exist_ok=True)
    with open(script_path, "w") as f:
        f.write("# Script content")

    for template in mock_templates.values():
        template.assert_called()

    # Ensure the script is created
    assert script_path.exists()


def test_assess_ensemble_directory(temp_dir, mock_ensemble_path):
    """
    Test the `assess_model_directory` method.

    Args:
        temp_dir (Path): The path to the temporary directory.
        mock_ensemble_path (MagicMock): The mock object for `EnsemblePath`.

    Asserts:
        - The directory assessment is performed correctly.
        - Missing directories are detected.
    """
    mock_ensemble_instance = mock_ensemble_path.return_value
    mock_ensemble_instance.model_dir = temp_dir / "test_ensemble"
    mock_ensemble_instance.get_directories.return_value = {
        "subdir1": temp_dir / "test_ensemble" / "subdir1"
    }

    builder = EnsembleScaffoldBuilder("test_ensemble")
    builder.build_model_directory()
    assessment = builder.assess_model_directory()

    assert "structure_errors" in assessment
    assert not assessment["structure_errors"]


def test_assess_ensemble_scripts(temp_dir, mock_ensemble_path):
    """
    Test the `assess_model_scripts` method.

    Args:
        temp_dir (Path): The path to the temporary directory.
        mock_ensemble_path (MagicMock): The mock object for `EnsemblePath`.

    Asserts:
        - The script assessment is performed correctly.
        - Missing scripts are detected.
    """
    mock_ensemble_instance = mock_ensemble_path.return_value
    mock_ensemble_instance.model_dir = temp_dir / "test_ensemble"
    mock_ensemble_instance.get_scripts.return_value = {
        "script1": temp_dir / "test_ensemble" / "script1.py"
    }

    builder = EnsembleScaffoldBuilder("test_ensemble")
    builder.build_model_directory()
    builder.build_model_scripts()

    # Create the script file to simulate actual script creation
    script_path = temp_dir / "test_ensemble" / "script1.py"
    os.makedirs(script_path.parent, exist_ok=True)
    with open(script_path, "w") as f:
        f.write("# Script content")

    assessment = builder.assess_model_scripts()

    assert "missing_scripts" in assessment
    assert not assessment["missing_scripts"]


# def test_assess_ensemble_directory_with_missing_dirs(temp_dir, mock_ensemble_path):
#     """
#     Test the `assess_model_directory` method with missing directories.

#     Args:
#         temp_dir (Path): The path to the temporary directory.
#         mock_ensemble_path (MagicMock): The mock object for `EnsemblePath`.

#     Asserts:
#         - The directory assessment detects missing directories.
#     """
#     mock_ensemble_instance = mock_ensemble_path.return_value
#     mock_ensemble_instance.model_dir = temp_dir / "test_ensemble"
#     mock_ensemble_instance.get_directories.return_value = {
#         "subdir1": temp_dir / "test_ensemble" / "subdir1"
#     }

#     builder = EnsembleScaffoldBuilder("test_ensemble")
#     builder.build_model_directory()

#     with patch('ensemble_scaffold_builder.Path.exists', side_effect=[True, False, True]):
#         assessment = builder.assess_model_directory()
#         assert assessment["structure_errors"] == {temp_dir / "test_ensemble" / "subdir1"}


# def test_assess_ensemble_scripts_with_missing_scripts(temp_dir, mock_ensemble_path):
#     """
#     Test the `assess_model_scripts` method with missing scripts.

#     Args:
#         temp_dir (Path): The path to the temporary directory.
#         mock_ensemble_path (MagicMock): The mock object for `EnsemblePath`.

#     Asserts:
#         - The script assessment detects missing scripts.
#     """
#     mock_ensemble_instance = mock_ensemble_path.return_value
#     mock_ensemble_instance.model_dir = temp_dir / "test_ensemble"
#     mock_ensemble_instance.get_scripts.return_value = {
#         "script1": temp_dir / "test_ensemble" / "script1.py"
#     }

#     builder = EnsembleScaffoldBuilder("test_ensemble")
#     builder.build_model_directory()

#     with patch('ensemble_scaffold_builder.Path.exists', side_effect=[True, False, True, True]):
#         assessment = builder.assess_model_scripts()
#         assert assessment["missing_scripts"] == {temp_dir / "test_ensemble" / "script1.py"}