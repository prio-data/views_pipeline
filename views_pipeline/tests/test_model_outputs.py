import pytest
import pandas as pd
from views_pipeline.models.outputs import ModelOutputs, generate_output_dict # todo
import wandb

@pytest.fixture
def mock_df():
    """
    Fixture to create a mock DataFrame.

    This fixture creates a mock DataFrame with predefined data for testing purposes.
    The DataFrame contains columns for month_id, priogrid_gid, country_id, depvar,
    step_pred_1, and step_pred_2. The DataFrame is indexed by month_id and priogrid_gid.

    Returns:
        pd.DataFrame: A mock DataFrame with predefined data.
    """
    data = {
        "month_id": [1, 1, 2, 2],
        "priogrid_gid": [101, 102, 101, 102],
        "country_id": [1, 1, 1, 1],
        "depvar": [0.1, 0.2, 0.3, 0.4],
        "step_pred_1": [0.15, 0.25, 0.35, 0.45],
        "step_pred_2": [0.16, 0.26, 0.36, 0.46],
    }
    df = pd.DataFrame(data)
    df.set_index(["month_id", "priogrid_gid"], inplace=True)
    return df


@pytest.fixture
def mock_config():
    """
    Fixture to create a mock configuration.

    This fixture creates a mock configuration object with predefined attributes for
    testing purposes. The configuration includes the steps for prediction and the
    dependent variable name.

    Returns:
        Config: A mock configuration object with predefined attributes.
    """

    config = wandb.Config()
    config.steps = [1, 2]
    config.depvar = "depvar"

    return config


def test_model_outputs_default_values():
    """
    Test the default values and types of the ModelOutputs attributes.

    This test verifies that the default values of the ModelOutputs attributes are
    correctly initialized as empty lists. It checks the types of the attributes to
    ensure they are lists.

    Raises:
        AssertionError: If any of the attributes are not lists.
    """
    model_outputs = ModelOutputs()
    assert isinstance(model_outputs.y_score, list)
    assert isinstance(model_outputs.y_score_prob, list)
    assert isinstance(model_outputs.y_var, list)
    assert isinstance(model_outputs.y_var_prob, list)
    assert isinstance(model_outputs.y_true, list)
    assert isinstance(model_outputs.y_true_binary, list)
    assert isinstance(model_outputs.pg_id, list)
    assert isinstance(model_outputs.c_id, list)
    assert isinstance(model_outputs.month_id, list)
    assert isinstance(model_outputs.out_sample_month, list)


def test_make_output_dict():
    """
    Test the make_output_dict method.

    This test verifies that the make_output_dict method correctly creates a dictionary
    of ModelOutputs objects for the specified number of steps. It checks the type and
    length of the output dictionary and ensures that each value is an instance of
    ModelOutputs.

    Raises:
        AssertionError: If the output is not a dictionary, if the length of the dictionary
                        is incorrect, or if any value in the dictionary is not an instance
                        of ModelOutputs.
    """
    output_dict = ModelOutputs.make_output_dict(steps=2)
    assert isinstance(output_dict, dict)
    assert len(output_dict) == 2
    assert all(isinstance(value, ModelOutputs) for value in output_dict.values())


def test_output_dict_to_dataframe():
    """
    Test the output_dict_to_dataframe method.

    This test verifies that the output_dict_to_dataframe method correctly converts a
    dictionary of ModelOutputs objects into a pandas DataFrame. It checks the type of
    the output and ensures that the DataFrame columns match the attributes of the
    ModelOutputs class.

    Raises:
        AssertionError: If the output is not a DataFrame or if the columns of the DataFrame
                        do not match the attributes of the ModelOutputs class.
    """
    output_dict = ModelOutputs.make_output_dict(steps=2)
    df = ModelOutputs.output_dict_to_dataframe(output_dict)
    assert isinstance(df, pd.DataFrame)
    assert set(df.columns) == set(ModelOutputs.__dataclass_fields__.keys())


def test_generate_output_dict(mock_df, mock_config):
    """
    Test the generate_output_dict function.

    This test verifies that the generate_output_dict function correctly generates a
    dictionary of ModelOutputs objects and a corresponding DataFrame from the input
    DataFrame and configuration. It checks the types and shapes of the output dictionary
    and DataFrame.

    Args:
        mock_df (pd.DataFrame): A mock DataFrame with predefined data.
        mock_config (Config): A mock configuration object with predefined attributes.

    Raises:
        AssertionError: If the output dictionary is not a dictionary, if any value in the
                        dictionary is not an instance of ModelOutputs, if the output
                        DataFrame is not a DataFrame, or if the columns of the DataFrame
                        do not match the attributes of the ModelOutputs class.
    """
    output_dict, df_output_dict = generate_output_dict(mock_df, mock_config)

    # Verify the type of the output dictionary
    assert isinstance(output_dict, dict)
    assert all(isinstance(value, ModelOutputs) for value in output_dict.values())

    # Verify the type of the output DataFrame
    assert isinstance(df_output_dict, pd.DataFrame)

    # Verify the shape of the output DataFrame
    assert set(df_output_dict.columns) == set(ModelOutputs.__dataclass_fields__.keys())
    assert len(df_output_dict) == len(mock_df) * len(mock_config.steps)
