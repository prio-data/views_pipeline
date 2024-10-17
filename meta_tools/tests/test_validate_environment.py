import pytest
import subprocess
import yaml
from unittest.mock import patch, mock_open

# Importing necessary modules:
# - pytest: for writing and running tests.
# - subprocess: for running system commands.
# - yaml: for parsing YAML files.
# - patch and mock_open from unittest.mock: for mocking objects in tests.

from pathlib import Path

# Importing Path from pathlib to handle file system paths.

import sys

# Importing the sys module to manipulate the Python runtime environment.

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Adding the grandparent directory of the current file to the system path.
# This allows importing modules from that directory.

from meta_tools.validate_environment import check_environment

# Importing the check_environment function from the validate_environment module in the meta_tools package.

# Mock data
mock_mamba_packages = "numpy=1.19.2\npandas=1.1.3"
mock_pip_packages = ["numpy==1.19.2", "pandas==1.1.3"]
mock_environment_yml = """
name: myenv
dependencies:
  - numpy=1.19.2
  - pandas=1.1.3
  - pip:
      - numpy==1.19.2
      - pandas==1.1.3
"""

# Defining mock data for testing:
# - mock_mamba_packages: a string representing the output of the 'mamba list --export' command.
# - mock_pip_packages: a list of strings representing the output of the 'pip freeze' command.
# - mock_environment_yml: a string representing the contents of an environment.yml file.

@pytest.fixture
def mock_subprocess_run():
    """
    Fixture to mock the subprocess.run function.
    
    This fixture patches subprocess.run to return predefined outputs for 'mamba list --export' 
    and 'pip freeze' commands. It yields the mock object for use in tests.
    
    Yields:
        mock_run (Mock): The mocked subprocess.run function.
    """
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            subprocess.CompletedProcess(args=["mamba", "list", "--export"], returncode=0, stdout=mock_mamba_packages),
            subprocess.CompletedProcess(args=["pip", "freeze"], returncode=0, stdout="\n".join(mock_pip_packages))
        ]
        yield mock_run

@pytest.fixture
def mock_yaml_safe_load():
    """
    Fixture to mock the yaml.safe_load function.
    
    This fixture patches yaml.safe_load to return the parsed mock_environment_yml. 
    It yields the mock object for use in tests.
    
    Yields:
        mock_load (Mock): The mocked yaml.safe_load function.
    """
    with patch("yaml.safe_load", return_value=yaml.safe_load(mock_environment_yml)) as mock_load:
        yield mock_load

@pytest.fixture
def mock_open_file():
    """
    Fixture to mock the open function.
    
    This fixture uses mock_open to simulate opening a file and reading mock_environment_yml. 
    It patches builtins.open to replace it with the mock_open object and yields the mock object for use in tests.
    
    Yields:
        m (Mock): The mocked open function.
    """
    m = mock_open(read_data=mock_environment_yml)
    with patch("builtins.open", m):
        yield m

def test_check_environment_no_environment_yml(mock_subprocess_run):
    """
    Test the check_environment function when environment.yml is missing.
    
    This test patches builtins.open to raise a FileNotFoundError, simulating a missing environment.yml file.
    It asserts that the discrepancies returned by check_environment are None.
    
    Args:
        mock_subprocess_run (Mock): The mocked subprocess.run function.
    """
    with patch("builtins.open", side_effect=FileNotFoundError):
        discrepancies = check_environment()
        assert discrepancies is None

def test_check_environment_malformed_environment_yml(mock_subprocess_run):
    """
    Test the check_environment function when environment.yml is malformed.
    
    This test patches yaml.safe_load to raise a yaml.YAMLError, simulating a malformed environment.yml file.
    It asserts that the discrepancies returned by check_environment are None.
    
    Args:
        mock_subprocess_run (Mock): The mocked subprocess.run function.
    """
    with patch("yaml.safe_load", side_effect=yaml.YAMLError):
        discrepancies = check_environment()
        assert discrepancies is None

def test_check_environment_missing_packages(mock_subprocess_run, mock_yaml_safe_load, mock_open_file):
    """
    Test the check_environment function when there are missing packages.
    
    This test modifies the mock data to simulate missing numpy package. 
    It asserts that the discrepancies list contains the expected missing package messages.
    
    Args:
        mock_subprocess_run (Mock): The mocked subprocess.run function.
        mock_yaml_safe_load (Mock): The mocked yaml.safe_load function.
        mock_open_file (Mock): The mocked open function.
    """
    # Modify mock data to simulate missing packages
    mock_subprocess_run.side_effect = [
        subprocess.CompletedProcess(args=["mamba", "list", "--export"], returncode=0, stdout="pandas=1.1.3"),
        subprocess.CompletedProcess(args=["pip", "freeze"], returncode=0, stdout="pandas==1.1.3")
    ]
    discrepancies = check_environment()
    assert "Missing pip package: numpy==1.19.2" in discrepancies
    assert "Missing mamba package: numpy=1.19.2" in discrepancies
