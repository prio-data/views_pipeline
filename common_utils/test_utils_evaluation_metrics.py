import pytest
import pandas as pd
import properscoring as ps
from sklearn.metrics import mean_squared_error, mean_absolute_error
from utils_evaluation_metrics import EvaluationMetrics, generate_metric_dict


@pytest.fixture
def mock_df():
    """Fixture to create a mock DataFrame."""
    data = {
        "depvar": [0.1, 0.2, 0.3, 0.4],
        "step_pred_1": [0.15, 0.25, 0.35, 0.45],
        "step_pred_2": [0.16, 0.26, 0.36, 0.46],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_config():
    """Fixture to create a mock configuration."""

    class Config:
        steps = [1, 2]
        depvar = "depvar"

    return Config()


def test_evaluation_metrics_default_values():
    """
    Test the default values and types of the EvaluationMetrics attributes.
    """
    metrics = EvaluationMetrics()
    assert metrics.MSE is None
    assert metrics.MAE is None
    assert metrics.MSLE is None
    assert metrics.KLD is None
    assert metrics.Jeffreys is None
    assert metrics.CRPS is None
    assert metrics.Brier is None
    assert metrics.AP is None
    assert metrics.AUC is None
    assert metrics.ensemble_weight_reg is None
    assert metrics.ensemble_weight_class is None


def test_make_evaluation_dict():
    """
    Test the make_evaluation_dict method.
    Verify the type and shape of the output dictionary.
    """
    evaluation_dict = EvaluationMetrics.make_evaluation_dict(steps=2)
    assert isinstance(evaluation_dict, dict)
    assert len(evaluation_dict) == 2
    assert all(
        isinstance(value, EvaluationMetrics) for value in evaluation_dict.values()
    )


def test_evaluation_dict_to_dataframe():
    """
    Test the evaluation_dict_to_dataframe method.
    Verify the type and shape of the output DataFrame.
    """
    evaluation_dict = EvaluationMetrics.make_evaluation_dict(steps=2)
    df = EvaluationMetrics.evaluation_dict_to_dataframe(evaluation_dict)
    assert isinstance(df, pd.DataFrame)
    assert set(df.columns) == set(EvaluationMetrics.__annotations__.keys())


def test_calculate_aggregate_metrics():
    """
    Test the calculate_aggregate_metrics method.
    Verify the type and shape of the output dictionary.
    Check that the aggregate metrics are correctly calculated.
    """
    evaluation_dict = EvaluationMetrics.make_evaluation_dict(steps=2)
    evaluation_dict["step01"].MSE = 0.1
    evaluation_dict["step02"].MSE = 0.2
    aggregate_metrics = EvaluationMetrics.calculate_aggregate_metrics(evaluation_dict)
    assert isinstance(aggregate_metrics, dict)
    assert set(aggregate_metrics.keys()) == {"mean", "std", "median"}
    assert aggregate_metrics["mean"]["MSE"] == pytest.approx(0.15, rel=1e-2)
    assert aggregate_metrics["std"]["MSE"] == pytest.approx(0.0707, rel=1e-2)
    assert aggregate_metrics["median"]["MSE"] == pytest.approx(0.15, rel=1e-2)


def test_output_metrics():
    """
    Test the output_metrics method.
    Verify the type and shape of the output dictionary.
    Check that the output dictionary contains the correct metrics.
    """
    evaluation_dict = EvaluationMetrics.make_evaluation_dict(steps=2)
    evaluation_dict["step01"].MSE = 0.1
    evaluation_dict["step02"].MSE = 0.2
    output_metrics = EvaluationMetrics.output_metrics(evaluation_dict)
    assert isinstance(output_metrics, dict)
    assert "mean" in output_metrics
    assert "std" in output_metrics
    assert "median" in output_metrics
    assert output_metrics["mean"]["MSE"] == pytest.approx(0.15, rel=1e-2)
    assert output_metrics["std"]["MSE"] == pytest.approx(0.0707, rel=1e-2)
    assert output_metrics["median"]["MSE"] == pytest.approx(0.15, rel=1e-2)


def test_generate_metric_dict(mock_df, mock_config):
    """
    Test the generate_metric_dict function.
    Verify the type and shape of the output dictionary and DataFrame.
    Check that the metrics are correctly calculated.
    """
    evaluation_dict, df_evaluation_dict = generate_metric_dict(mock_df, mock_config)
    print(evaluation_dict)
    # Verify the type of the output dictionary before calling output_metrics
    assert isinstance(evaluation_dict, dict)
    # assert all(
    #     isinstance(value, EvaluationMetrics) for value in evaluation_dict.values()
    # )

    # Check that the metrics are correctly calculated before calling output_metrics
    assert evaluation_dict["step01"]["MSE"] == pytest.approx(
        mean_squared_error(mock_df["depvar"], mock_df["step_pred_1"]), rel=1e-2
    )
    assert evaluation_dict["step01"]["MAE"] == pytest.approx(
        mean_absolute_error(mock_df["depvar"], mock_df["step_pred_1"]), rel=1e-2
    )
    assert evaluation_dict["step01"]["CRPS"] == pytest.approx(
        ps.crps_ensemble(mock_df["depvar"], mock_df["step_pred_1"]).mean(), rel=1e-2
    )

    # Verify the type of the output DataFrame
    assert isinstance(df_evaluation_dict, pd.DataFrame)

    # Verify the shape of the output DataFrame
    assert set(df_evaluation_dict.columns) == set(
        EvaluationMetrics.__annotations__.keys()
    )
    assert (
        len(df_evaluation_dict) == len(mock_config.steps) + 3
    )  # steps + mean, std, median

    # Verify the aggregate metrics
    aggregate_metrics = EvaluationMetrics.calculate_aggregate_metrics(evaluation_dict)
    assert "mean" in aggregate_metrics
    assert "std" in aggregate_metrics
    assert "median" in aggregate_metrics
    assert aggregate_metrics["mean"]["MSE"] == pytest.approx(0.15, rel=1e-2)
    assert aggregate_metrics["std"]["MSE"] == pytest.approx(0.0707, rel=1e-2)
    assert aggregate_metrics["median"]["MSE"] == pytest.approx(0.15, rel=1e-2)
