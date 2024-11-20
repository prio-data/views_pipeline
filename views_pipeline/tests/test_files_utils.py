import pytest
from unittest.mock import patch, mock_open
from views_pipeline.files.utils import read_log_file, create_data_fetch_log_file, create_specific_log_file, create_log_file
from pathlib import Path

def test_read_log_file():
    """
    Test the read_log_file function.

    This test verifies that the read_log_file function correctly reads and parses
    the log file content into a dictionary.

    Asserts:
        - The log data contains the correct model name.
        - The log data contains the correct data fetch timestamp.
    """
    log_content = "Single Model Name: test_model\nData Fetch Timestamp: 2023-10-01T12:00:00Z\n"
    with patch("builtins.open", mock_open(read_data=log_content)):
        log_data = read_log_file("dummy_path")
        assert log_data["Single Model Name"] == "test_model"
        assert log_data["Data Fetch Timestamp"] == "2023-10-01T12:00:00Z"

def test_create_data_fetch_log_file(tmp_path):
    """
    Test the create_data_fetch_log_file function.

    This test verifies that the create_data_fetch_log_file function correctly creates
    a log file with the specified data fetch details.

    Args:
        tmp_path (Path): The temporary directory provided by pytest.

    Asserts:
        - The log file is created at the expected path.
        - The log file contains the correct model name.
        - The log file contains the correct data fetch timestamp.
    """
    path_raw = tmp_path / "raw"
    path_raw.mkdir()
    run_type = "test_run"
    model_name = "test_model"
    data_fetch_timestamp = "2023-10-01T12:00:00Z"
    
    create_data_fetch_log_file(path_raw, run_type, model_name, data_fetch_timestamp)
    
    log_file_path = path_raw / f"{run_type}_data_fetch_log.txt"
    assert log_file_path.exists()
    
    with open(log_file_path, "r") as file:
        content = file.read()
        assert "Single Model Name: test_model" in content
        assert "Data Fetch Timestamp: 2023-10-01T12:00:00Z" in content

def test_create_specific_log_file(tmp_path):
    """
    Test the create_specific_log_file function.

    This test verifies that the create_specific_log_file function correctly creates
    a log file with the specified model and data generation details.

    Args:
        tmp_path (Path): The temporary directory provided by pytest.

    Asserts:
        - The log file is created at the expected path.
        - The log file contains the correct model name.
        - The log file contains the correct model timestamp.
        - The log file contains the correct data generation timestamp.
        - The log file contains the correct data fetch timestamp.
        - The log file contains the correct deployment status.
    """
    path_generated = tmp_path / "generated"
    path_generated.mkdir()
    run_type = "test_run"
    model_name = "test_model"
    deployment_status = "deployed"
    model_timestamp = "2023-10-01T12:00:00Z"
    data_generation_timestamp = "2023-10-01T12:00:00Z"
    data_fetch_timestamp = "2023-10-01T12:00:00Z"
    
    create_specific_log_file(path_generated, run_type, model_name, deployment_status, model_timestamp, data_generation_timestamp, data_fetch_timestamp)
    
    log_file_path = path_generated / f"{run_type}_log.txt"
    assert log_file_path.exists()
    
    with open(log_file_path, "r") as file:
        content = file.read()
        assert "Single Model Name: test_model" in content
        assert "Single Model Timestamp: 2023-10-01T12:00:00Z" in content
        assert "Data Generation Timestamp: 2023-10-01T12:00:00Z" in content
        assert "Data Fetch Timestamp: 2023-10-01T12:00:00Z" in content
        assert "Deployment Status: deployed" in content

# def test_create_log_file(tmp_path):
#     path_generated = tmp_path / "generated"
#     path_generated.mkdir()
#     model_config = {
#         "run_type": "test_run",
#         "name": "test_model",
#         "deployment_status": "deployed"
#     }
#     model_timestamp = "2023-10-01T12:00:00Z"
#     data_generation_timestamp = "2023-10-01T12:00:00Z"
#     data_fetch_timestamp = "2023-10-01T12:00:00Z"
    
#     with patch("views_pipeline.managers.path_manager.ModelPath") as MockModelPath:
#         mock_model_path_instance = MockModelPath.return_value
#         mock_model_path_instance.data_generated = path_generated
#         MockModelPath.side_effect = lambda name, validate: mock_model_path_instance if name == "test_model" and not validate else None
        
#         create_log_file(path_generated, model_config, model_timestamp, data_generation_timestamp, data_fetch_timestamp, models=["first_model", "second_model"])
        
#         log_file_path = path_generated / f"{model_config['run_type']}_log.txt"
#         assert log_file_path.exists()
        
#         with open(log_file_path, "r") as file:
#             content = file.read()
#             assert "Single Model Name: test_model" in content
#             assert "Single Model Timestamp: 2023-10-01T12:00:00Z" in content
#             assert "Data Generation Timestamp: 2023-10-01T12:00:00Z" in content
#             assert "Data Fetch Timestamp: 2023-10-01T12:00:00Z" in content
#             assert "Deployment Status: deployed" in content

#             # Check for appended model logs
#             assert "Single Model Name: first_model" in content
#             assert "Single Model Name: second_model" in content