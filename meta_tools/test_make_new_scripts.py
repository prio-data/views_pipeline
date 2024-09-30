import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from make_new_scripts import ModelScriptBuilder


@pytest.fixture
def mock_validate_model_name():
    """
    Fixture to mock the validate_model_name function.

    This fixture uses the `patch` function from the `unittest.mock` module to replace
    the `validate_model_name` function in the `make_new_scripts` module with a mock object.
    This allows you to test code that depends on `validate_model_name` without actually
    calling the real function.

    Yields:
        unittest.mock.MagicMock: The mock object that replaces `validate_model_name`.
    """
    with patch("make_new_scripts.validate_model_name") as mock:
        yield mock


@pytest.fixture
def mock_find_project_root():
    """
    Fixture to mock the find_project_root function.

    This function uses the `patch` context manager from the `unittest.mock` module
    to replace the `find_project_root` function in the `make_new_scripts` module
    with a mock object. This allows for testing code that depends on
    `find_project_root` without actually invoking the real function.

    Yields:
        unittest.mock.MagicMock: The mock object that replaces `find_project_root`.
    """
    with patch("make_new_scripts.find_project_root") as mock:
        yield mock


@pytest.fixture
def mock_templates():
    """
    Fixture to mock the template generation functions.

    This fixture patches the following functions from the `make_new_scripts` module:
    - `template_config_deployment`
    - `template_config_hyperparameters`
    - `template_config_input_data`
    - `template_config_meta`
    - `template_config_sweep`
    - `template_main`

    Yields:
        dict: A dictionary containing the mocked versions of the template generation functions.
    """
    with patch("make_new_scripts.template_config_deployment") as mock_deployment, patch(
        "make_new_scripts.template_config_hyperparameters"
    ) as mock_hyperparameters, patch(
        "make_new_scripts.template_config_input_data"
    ) as mock_input_data, patch(
        "make_new_scripts.template_config_meta"
    ) as mock_meta, patch(
        "make_new_scripts.template_config_sweep"
    ) as mock_sweep, patch(
        "make_new_scripts.template_main"
    ) as mock_main:
        yield {
            "deployment": mock_deployment,
            "hyperparameters": mock_hyperparameters,
            "input_data": mock_input_data,
            "meta": mock_meta,
            "sweep": mock_sweep,
            "main": mock_main,
        }


@pytest.fixture
def temp_model_dir(tmp_path):
    """
    Creates a temporary model directory for testing purposes.

    This fixture generates a temporary directory path intended for storing
    model-related files during tests. The directory is created within the
    provided temporary path.

    Args:
        tmp_path (pathlib.Path): A temporary directory path provided by pytest.

    Returns:
        pathlib.Path: The path to the temporary model directory.
    """
    return tmp_path / "models" / "test_model"


def test_init_valid_model_name(
    mock_validate_model_name, mock_find_project_root, temp_model_dir
):
    """
    This test ensures that the ModelScriptBuilder is correctly initialized when provided with a valid model name.
    It mocks the `validate_model_name` and `find_project_root` functions to simulate the expected behavior and verifies that the `model_name` and `model_dir` attributes of the builder are set correctly.

        mock_validate_model_name (Mock): Mocked validate_model_name function.
        mock_find_project_root (Mock): Mocked find_project_root function.
        temp_model_dir (Path): Temporary model directory.

    Asserts:
        The model_name attribute of the builder is set to "test_model".
        The model_dir attribute of the builder is set to temp_model_dir.
    """
    mock_validate_model_name.return_value = True
    mock_find_project_root.return_value = temp_model_dir.parent.parent

    builder = ModelScriptBuilder("test_model")
    assert builder.model_name == "test_model"
    assert builder.model_dir == temp_model_dir


def test_check_if_model_dir_exists(
    mock_validate_model_name, mock_find_project_root, temp_model_dir
):
    """
    This test verifies that the _check_if_model_dir_exists method correctly identifies
    whether a model directory exists or not.

        mock_validate_model_name (Mock): Mocked validate_model_name function.
        mock_find_project_root (Mock): Mocked find_project_root function.
        temp_model_dir (Path): Temporary model directory used for testing.
    """
    mock_validate_model_name.return_value = True
    mock_find_project_root.return_value = temp_model_dir.parent.parent

    builder = ModelScriptBuilder("test_model")
    temp_model_dir.mkdir(parents=True)
    assert builder._check_if_model_dir_exists() is True

    temp_model_dir.rmdir()
    assert builder._check_if_model_dir_exists() is False


def test_build_model_scripts_existing_directory(
    mock_validate_model_name, mock_find_project_root, mock_templates, temp_model_dir
):
    """
    This test ensures that the build_model_scripts method correctly generates
    the necessary scripts when the model directory already exists. It mocks
    the validation of the model name, the finding of the project root, and the
    template generation functions to verify that the appropriate templates are
    called.

        mock_validate_model_name (Mock): Mocked validate_model_name function.
        mock_find_project_root (Mock): Mocked find_project_root function.
        mock_templates (dict): Dictionary of mocked template generation functions.
        temp_model_dir (Path): Temporary model directory.
    """
    mock_validate_model_name.return_value = True
    mock_find_project_root.return_value = temp_model_dir.parent.parent

    temp_model_dir.mkdir(parents=True)
    builder = ModelScriptBuilder("test_model")

    with patch("builtins.input", return_value="XGBoost"):
        builder.build_model_scripts()

    assert mock_templates["deployment"].generate.called
    assert mock_templates["hyperparameters"].generate.called
    assert mock_templates["input_data"].generate.called
    assert mock_templates["meta"].generate.called
    assert mock_templates["sweep"].generate.called
    assert mock_templates["main"].generate.called


def test_build_model_scripts_missing_directory(
    mock_validate_model_name, mock_find_project_root, temp_model_dir
):
    """
    mock_validate_model_name (Mock): Mocked validate_model_name function.
        mock_find_project_root (Mock): Mocked find_project_root function.
        temp_model_dir (Path): Temporary model directory.

    Raises:
        FileNotFoundError: If the model directory does not exist.
    mock_validate_model_name, mock_find_project_root, temp_model_dir
    """
    mock_validate_model_name.return_value = True
    mock_find_project_root.return_value = temp_model_dir.parent.parent

    builder = ModelScriptBuilder("test_model")
    with pytest.raises(FileNotFoundError):
        builder.build_model_scripts()


def test_assess_model_scripts(
    mock_validate_model_name, mock_find_project_root, temp_model_dir
):
    """
    This test verifies the functionality of the `assess_model_scripts` method in the `ModelScriptBuilder` class.
    It ensures that the method correctly identifies the presence and absence of obligatory scripts in a model directory.

        mock_validate_model_name (Mock): Mocked `validate_model_name` function.
        mock_find_project_root (Mock): Mocked `find_project_root` function.
        temp_model_dir (Path): Temporary directory for the model scripts.

    Test Steps:
    1. Mock the `validate_model_name` and `find_project_root` functions to return predefined values.
    2. Create an instance of `ModelScriptBuilder` with a test model name.
    3. Create the temporary model directory and all obligatory scripts.
    4. Assess the model scripts and assert that no scripts are missing.
    5. Remove one obligatory script and reassess.
    6. Assert that the assessment correctly identifies the missing script.
    """
    mock_validate_model_name.return_value = True
    mock_find_project_root.return_value = temp_model_dir.parent.parent

    builder = ModelScriptBuilder("test_model")
    temp_model_dir.mkdir(parents=True)
    for script in builder.obligatory_scripts:
        (temp_model_dir / script).parent.mkdir(parents=True, exist_ok=True)
        (temp_model_dir / script).touch()

    assessment = builder.assess_model_scripts()
    assert assessment["model_dir"] == temp_model_dir
    assert not assessment["missing_scripts"]

    # Remove one script and check assessment again
    (temp_model_dir / builder.obligatory_scripts[0]).unlink()
    assessment = builder.assess_model_scripts()
    assert len(assessment["missing_scripts"]) == 1
    assert (
        assessment["missing_scripts"][0]
        == f"Missing script: {builder.obligatory_scripts[0]}"
    )
