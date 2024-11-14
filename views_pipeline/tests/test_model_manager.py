import pytest
from unittest.mock import MagicMock, patch, mock_open
from views_pipeline.managers.path_manager import ModelPath, EnsemblePath
from views_pipeline.data.dataloaders import ViewsDataLoader
from views_pipeline.managers.model_manager import ModelManager
import wandb
import pandas as pd
from pathlib import Path

@pytest.fixture
def mock_model_path():
    with patch("views_pipeline.managers.path_manager.ModelPath") as mock:
        yield mock

@pytest.fixture
def mock_ensemble_path():
    with patch("views_pipeline.managers.path_manager.EnsemblePath") as mock:
        yield mock

@pytest.fixture
def mock_dataloader():
    with patch("views_pipeline.data.dataloaders.ViewsDataLoader") as mock:
        yield mock

@pytest.fixture
def mock_wandb():
    with patch("wandb.init"), patch("wandb.finish"), patch("wandb.sweep"), patch("wandb.agent"):
        yield

def test_model_manager_init(mock_model_path):
    mock_model_instance = mock_model_path.return_value
    mock_model_instance.get_scripts.return_value = {
        "config_deployment.py": "path/to/config_deployment.py",
        "config_hyperparameters.py": "path/to/config_hyperparameters.py",
        "config_meta.py": "path/to/config_meta.py",
        "config_sweep.py": "path/to/config_sweep.py"
    }
    with patch("importlib.util.spec_from_file_location") as mock_spec, patch("importlib.util.module_from_spec") as mock_module:
        mock_spec.return_value.loader = MagicMock()
        mock_module.return_value.get_deployment_config.return_value = {"key": "value"}
        mock_module.return_value.get_hp_config.return_value = {"key": "value"}
        mock_module.return_value.get_meta_config.return_value = {"key": "value"}
        mock_module.return_value.get_sweep_config.return_value = {"key": "value"}
        manager = ModelManager(mock_model_instance)
        assert manager._entity == "views_pipeline"
        assert manager._model_path == mock_model_instance

def test_load_config(mock_model_path):
    mock_model_instance = mock_model_path.return_value
    mock_model_instance.get_scripts.return_value = {
        "config_deployment.py": "path/to/config_deployment.py"
    }
    with patch("importlib.util.spec_from_file_location") as mock_spec, patch("importlib.util.module_from_spec") as mock_module:
        mock_spec.return_value.loader = MagicMock()
        mock_module.return_value.get_deployment_config.return_value = {"key": "value"}
        manager = ModelManager(mock_model_instance)
        config = manager._ModelManager__load_config("config_deployment.py", "get_deployment_config")
        assert config == {"key": "value"}

def test_update_single_config(mock_model_path):
    mock_model_instance = mock_model_path.return_value
    manager = ModelManager(mock_model_instance)
    manager._config_hyperparameters = {"hp_key": "hp_value"}
    manager._config_meta = {"meta_key": "meta_value"}
    manager._config_deployment = {"deploy_key": "deploy_value"}
    args = MagicMock(run_type="test_run")
    config = manager._update_single_config(args)
    assert config["hp_key"] == "hp_value"
    assert config["meta_key"] == "meta_value"
    assert config["deploy_key"] == "deploy_value"
    assert config["run_type"] == "test_run"
    assert config["sweep"] is False

def test_update_sweep_config(mock_model_path):
    mock_model_instance = mock_model_path.return_value
    manager = ModelManager(mock_model_instance)
    manager._config_sweep = {"parameters": {}}
    manager._config_meta = {"name": "test_name", "depvar": "test_depvar", "algorithm": "test_algorithm"}
    args = MagicMock(run_type="test_run")
    config = manager._update_sweep_config(args)
    assert config["parameters"]["run_type"]["value"] == "test_run"
    assert config["parameters"]["sweep"]["value"] is True
    assert config["parameters"]["name"]["value"] == "test_name"
    assert config["parameters"]["depvar"]["value"] == "test_depvar"
    assert config["parameters"]["algorithm"]["value"] == "test_algorithm"

def test_execute_single_run(mock_model_path, mock_dataloader, mock_wandb):
    mock_model_instance = mock_model_path.return_value
    manager = ModelManager(mock_model_instance)
    manager._update_single_config = MagicMock(return_value={"name": "test_name"})
    manager._execute_model_tasks = MagicMock()
    manager._data_loader = MagicMock()
    manager._data_loader.get_data = MagicMock()
    manager._data_loader._path_raw = "/path/to/raw"
    args = MagicMock(run_type="calibration", saved=False, drift_self_test=False, train=True, evaluate=True, forecast=True, artifact_name="test_artifact")
    manager.execute_single_run(args)
    manager._update_single_config.assert_called_once_with(args)
    manager._execute_model_tasks.assert_called_once_with(config={"name": "test_name"}, train=True, eval=True, forecast=True, artifact_name="test_artifact")

def test_execute_sweep_run(mock_model_path, mock_dataloader, mock_wandb):
    mock_model_instance = mock_model_path.return_value
    manager = ModelManager(mock_model_instance)
    manager._update_sweep_config = MagicMock(return_value={"name": "test_name"})
    manager._execute_model_tasks = MagicMock()
    manager._data_loader = MagicMock()
    manager._data_loader.get_data = MagicMock()
    manager._data_loader._path_raw = "/path/to/raw"
    args = MagicMock(run_type="calibration", saved=False, drift_self_test=False)
    manager.execute_sweep_run(args)
    manager._update_sweep_config.assert_called_once_with(args)
    manager._execute_model_tasks.assert_called_once()

def test_get_artifact_files(mock_model_path):
    mock_model_instance = mock_model_path.return_value
    manager = ModelManager(mock_model_instance)
    path_artifact = Path("/path/to/artifacts")
    run_type = "test_run"
    with patch("pathlib.Path.iterdir") as mock_iterdir:
        mock_iterdir.return_value = [
            Path("/path/to/artifacts/test_run_model_1.pt"),
            Path("/path/to/artifacts/test_run_model_2.h5"),
            Path("/path/to/artifacts/other_model.txt")
        ]
        files = manager._get_artifact_files(path_artifact, run_type)
        assert len(files) == 2
        assert files[0].name == "test_run_model_1.pt"
        assert files[1].name == "test_run_model_2.h5"

def test_save_model_outputs(mock_model_path):
    mock_model_instance = mock_model_path.return_value
    manager = ModelManager(mock_model_instance)
    manager.config = {"steps": [1], "run_type": "test_run", "timestamp": "20220101"}
    df_evaluation = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    df_output = pd.DataFrame({"col1": [5, 6], "col2": [7, 8]})
    path_generated = Path("/path/to/generated")
    with patch("builtins.open", new_callable=mock_open), patch("pathlib.Path.mkdir"), patch("pathlib.Path.exists", return_value=True):
        manager._save_model_outputs(df_evaluation, df_output, path_generated)
        assert Path(f"{path_generated}/output_1_test_run_20220101.pkl").exists()
        assert Path(f"{path_generated}/evaluation_1_test_run_20220101.pkl").exists()

def test_save_predictions(mock_model_path):
    mock_model_instance = mock_model_path.return_value
    manager = ModelManager(mock_model_instance)
    manager.config = {"steps": [1], "run_type": "test_run", "timestamp": "20220101"}
    df_predictions = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    path_generated = Path("/path/to/generated")
    with patch("builtins.open", new_callable=mock_open), patch("pathlib.Path.mkdir"), patch("pathlib.Path.exists", return_value=True):
        manager._save_predictions(df_predictions, path_generated)
        assert Path(f"{path_generated}/predictions_1_test_run_20220101.pkl").exists()
    with patch("importlib.util.spec_from_file_location") as mock_spec, patch("importlib.util.module_from_spec") as mock_module:
        mock_spec.return_value.loader = MagicMock()
        mock_module.return_value.get_deployment_config.return_value = {"key": "value"}
        mock_module.return_value.get_hp_config.return_value = {"key": "value"}
        mock_module.return_value.get_meta_config.return_value = {"key": "value"}
        mock_module.return_value.get_sweep_config.return_value = {"key": "value"}
        manager = ModelManager(mock_model_instance)
        assert manager._entity == "views_pipeline"
        assert manager._model_path == mock_model_instance

def test_load_config(mock_model_path):
    mock_model_instance = mock_model_path.return_value
    mock_model_instance.get_scripts.return_value = {
        "config_deployment.py": "path/to/config_deployment.py"
    }
    with patch("importlib.util.spec_from_file_location") as mock_spec, patch("importlib.util.module_from_spec") as mock_module:
        mock_spec.return_value.loader = MagicMock()
        mock_module.return_value.get_deployment_config.return_value = {"key": "value"}
        manager = ModelManager(mock_model_instance)
        config = manager._ModelManager__load_config("config_deployment.py", "get_deployment_config")
        assert config == {"key": "value"}

def test_update_single_config(mock_model_path):
    mock_model_instance = mock_model_path.return_value
    manager = ModelManager(mock_model_instance)
    manager._config_hyperparameters = {"hp_key": "hp_value"}
    manager._config_meta = {"meta_key": "meta_value"}
    manager._config_deployment = {"deploy_key": "deploy_value"}
    args = MagicMock(run_type="test_run")
    config = manager._update_single_config(args)
    assert config["hp_key"] == "hp_value"
    assert config["meta_key"] == "meta_value"
    assert config["deploy_key"] == "deploy_value"
    assert config["run_type"] == "test_run"
    assert config["sweep"] is False

def test_update_sweep_config(mock_model_path):
    mock_model_instance = mock_model_path.return_value
    manager = ModelManager(mock_model_instance)
    manager._config_sweep = {"parameters": {}}
    manager._config_meta = {"name": "test_name", "depvar": "test_depvar", "algorithm": "test_algorithm"}
    args = MagicMock(run_type="test_run")
    config = manager._update_sweep_config(args)
    assert config["parameters"]["run_type"]["value"] == "test_run"
    assert config["parameters"]["sweep"]["value"] is True
    assert config["parameters"]["name"]["value"] == "test_name"
    assert config["parameters"]["depvar"]["value"] == "test_depvar"
    assert config["parameters"]["algorithm"]["value"] == "test_algorithm"

def test_execute_single_run(mock_model_path, mock_dataloader, mock_wandb):
    mock_model_instance = mock_model_path.return_value
    manager = ModelManager(mock_model_instance)
    manager._update_single_config = MagicMock(return_value={"name": "test_name"})
    manager._execute_model_tasks = MagicMock()
    args = MagicMock(run_type="calibration", saved=False, drift_self_test=False, train=True, evaluate=True, forecast=True, artifact_name="test_artifact")
    manager.execute_single_run(args)
    manager._update_single_config.assert_called_once_with(args)
    manager._execute_model_tasks.assert_called_once_with(config={"name": "test_name"}, train=True, eval=True, forecast=True, artifact_name="test_artifact")

def test_execute_sweep_run(mock_model_path, mock_dataloader, mock_wandb):
    mock_model_instance = mock_model_path.return_value
    manager = ModelManager(mock_model_instance)
    manager._update_sweep_config = MagicMock(return_value={"name": "test_name"})
    manager._execute_model_tasks = MagicMock()
    args = MagicMock(run_type="calibration", saved=False, drift_self_test=False)
    manager.execute_sweep_run(args)
    manager._update_sweep_config.assert_called_once_with(args)
    manager._execute_model_tasks.assert_called_once()

def test_get_artifact_files(mock_model_path):
    mock_model_instance = mock_model_path.return_value
    manager = ModelManager(mock_model_instance)
    path_artifact = Path("/path/to/artifacts")
    run_type = "test_run"
    with patch("pathlib.Path.iterdir") as mock_iterdir:
        mock_iterdir.return_value = [
            Path("/path/to/artifacts/test_run_model_1.pt"),
            Path("/path/to/artifacts/test_run_model_2.h5"),
            Path("/path/to/artifacts/other_model.txt")
        ]
        files = manager._get_artifact_files(path_artifact, run_type)
        assert len(files) == 2
        assert files[0].name == "test_run_model_1.pt"
        assert files[1].name == "test_run_model_2.h5"

def test_save_model_outputs(mock_model_path):
    mock_model_instance = mock_model_path.return_value
    manager = ModelManager(mock_model_instance)
    manager.config = {"steps": [1], "run_type": "test_run", "timestamp": "20220101"}
    df_evaluation = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    df_output = pd.DataFrame({"col1": [5, 6], "col2": [7, 8]})
    path_generated = Path("/path/to/generated")
    with patch("builtins.open", new_callable=mock_open), patch("pathlib.Path.mkdir"):
        manager._save_model_outputs(df_evaluation, df_output, path_generated)
        assert Path(f"{path_generated}/output_1_test_run_20220101.pkl").exists()
        assert Path(f"{path_generated}/evaluation_1_test_run_20220101.pkl").exists()

def test_save_predictions(mock_model_path):
    mock_model_instance = mock_model_path.return_value
    manager = ModelManager(mock_model_instance)
    manager.config = {"steps": [1], "run_type": "test_run", "timestamp": "20220101"}
    df_predictions = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    path_generated = Path("/path/to/generated")
    with patch("builtins.open", new_callable=mock_open), patch("pathlib.Path.mkdir"):
        manager._save_predictions(df_predictions, path_generated)
        assert Path(f"{path_generated}/predictions_1_test_run_20220101.pkl").exists()