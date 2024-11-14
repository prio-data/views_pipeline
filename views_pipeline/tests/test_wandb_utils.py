import pytest
import wandb
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

from views_pipeline.wandb.utils import (
    add_wandb_monthly_metrics,
    generate_wandb_log_dict,
    log_wandb_log_dict,
)


@pytest.fixture
def mock_wandb():
    """
    Fixture to mock wandb methods.

    This fixture patches the `wandb.define_metric` and `wandb.log` methods to prevent
    actual calls to the Weights and Biases API during testing. It yields the mocked
    methods for use in tests.

    Yields:
        tuple: A tuple containing the mocked `wandb.define_metric` and `wandb.log` methods.
    """
    with patch("wandb.define_metric") as mock_define_metric, patch(
        "wandb.log"
    ) as mock_log:
        yield mock_define_metric, mock_log


def test_add_wandb_monthly_metrics(mock_wandb):
    """
    Test defining WandB metrics for monthly evaluation.

    This test verifies that the `add_wandb_monthly_metrics` function correctly defines
    the necessary metrics for monthly evaluation using the `wandb.define_metric` method.
    It checks that the metrics "monthly/out_sample_month" and "monthly/*" with the step
    metric "monthly/out_sample_month" are defined.

    Args:
        mock_wandb (tuple): A tuple containing the mocked `wandb.define_metric` and `wandb.log` methods.
    """
    mock_define_metric, _ = mock_wandb
    add_wandb_monthly_metrics()
    mock_define_metric.assert_any_call("monthly/out_sample_month")
    mock_define_metric.assert_any_call(
        "monthly/*", step_metric="monthly/out_sample_month"
    )


def test_generate_wandb_log_dict():
    """
    Test updating the log dictionary with evaluation metrics for a specific time step.

    This test verifies that the `generate_wandb_log_dict` function correctly updates the
    log dictionary with evaluation metrics for a given time step. It checks that the
    output is a dictionary with keys prefixed by "monthly/" and values that are either
    integers or floats.

    Raises:
        AssertionError: If the output is not a dictionary or if the keys and values do not
                        meet the expected criteria.
    """
    log_dict = {}
    dict_of_eval_dicts = {
        "step01": {"MSE": 0.1, "AP": 0.2, "AUC": 0.3, "Brier": 0.4},
        "step02": {"MSE": 0.2, "AP": 0.3, "AUC": 0.4, "Brier": 0.5},
    }
    updated_log_dict = generate_wandb_log_dict(log_dict, dict_of_eval_dicts, "step01")

    # Verify the type of the output
    assert isinstance(updated_log_dict, dict)

    # Verify the shape of the output
    assert all(key.startswith("monthly/") for key in updated_log_dict.keys())
    assert all(isinstance(value, (int, float)) for value in updated_log_dict.values())


def test_generate_wandb_log_dict_with_none_values():
    """
    Test updating the log dictionary with evaluation metrics, ignoring None values.

    This test verifies that the `generate_wandb_log_dict` function correctly updates the
    log dictionary with evaluation metrics for a given time step, ignoring any None values.
    It checks that the output is a dictionary with keys prefixed by "monthly/" and values
    that are either integers or floats.

    Raises:
        AssertionError: If the output is not a dictionary or if the keys and values do not
                        meet the expected criteria.
    """
    log_dict = {}
    dict_of_eval_dicts = {"step01": {"MSE": 0.1, "AP": None, "AUC": 0.3, "Brier": None}}
    updated_log_dict = generate_wandb_log_dict(log_dict, dict_of_eval_dicts, "step01")

    # Verify the type of the output
    assert isinstance(updated_log_dict, dict)

    # Verify the shape of the output
    assert all(key.startswith("monthly/") for key in updated_log_dict.keys())
    assert all(isinstance(value, (int, float)) for value in updated_log_dict.values())


def test_log_wandb_log_dict(mock_wandb):
    """
    Test logging the WandB log dictionary for each step in the configuration.

    This test verifies that the `log_wandb_log_dict` function correctly logs the WandB
    log dictionary for each step specified in the configuration. It checks that the
    output for each step is a dictionary with keys prefixed by "monthly/" and values
    that are either integers or floats, and that the `wandb.log` method is called with
    the expected log dictionary.

    Args:
        mock_wandb (tuple): A tuple containing the mocked `wandb.define_metric` and `wandb.log` methods.

    Raises:
        AssertionError: If the output is not a dictionary or if the keys and values do not
                        meet the expected criteria, or if `wandb.log` is not called with
                        the expected log dictionary.
    """
    _, mock_log = mock_wandb
    config = {"steps": [1, 2]}
    evaluation = {
        "step01": {"MSE": 0.1, "AP": 0.2, "AUC": 0.3, "Brier": 0.4},
        "step02": {"MSE": 0.2, "AP": 0.3, "AUC": 0.4, "Brier": 0.5},
    }
    log_wandb_log_dict(config, evaluation)

    # Verify the type and shape of the output for each step
    for t in config["steps"]:
        step = f"step{str(t).zfill(2)}"
        expected_log_dict = generate_wandb_log_dict(
            {"monthly/out_sample_month": t}, evaluation, step
        )

        # Verify the type of the output
        assert isinstance(expected_log_dict, dict)

        # Verify the shape of the output
        assert all(key.startswith("monthly/") for key in expected_log_dict.keys())
        assert all(
            isinstance(value, (int, float)) for value in expected_log_dict.values()
        )

        mock_log.assert_any_call(expected_log_dict)
