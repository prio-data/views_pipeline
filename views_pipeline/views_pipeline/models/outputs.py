from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd

@dataclass
class ModelOutputs:
    """
    A data class for storing and managing model outputs for evaluation as well as true forcasting.
    
    Attributes:
        y_score (Optional[List[float]]): Model predictions (magnitude, e.g. logged fatalites).
        y_score_prob (Optional[List[float]]): Model prediction (probabilities).
        y_var (Optional[List[float]]): Variance of the model predictions.
        y_var_prob (Optional[List[float]]): Variance of the model prediction probabilities.
        y_true (Optional[List[float]]): True values.
        y_true_binary (Optional[List[int]]): True binary values (0 or 1).
        pg_id (Optional[List[int]]): The priogrid id.
        c_id (Optional[List[int]]): The country id.
        month_id (Optional[List[int]]): The month id.
        out_sample_month (Optional[List[int]]): The step ahead forecast.
    """

    y_score: Optional[List[float]] = field(default_factory=list)
    y_score_prob: Optional[List[float]] = field(default_factory=list)
    y_var: Optional[List[float]] = field(default_factory=list)
    y_var_prob: Optional[List[float]] = field(default_factory=list)
    y_true: Optional[List[float]] = field(default_factory=list)
    y_true_binary: Optional[List[int]] = field(default_factory=list)
    pg_id: Optional[List[int]] = field(default_factory=list)
    c_id: Optional[List[int]] = field(default_factory=list)
    month_id: Optional[List[int]] = field(default_factory=list)
    out_sample_month: Optional[List[int]] = field(default_factory=list)

    @classmethod
    def make_output_dict(cls, steps=36) -> dict:
        """
        Generates a dictionary of ModelOutputs instances for a specified number of forecasting steps.

        This method facilitates the batch creation of output containers for multiple forecasting steps, initializing them with empty lists.

        Args:
            steps (int): The number of forecasting steps for which to generate model outputs. Defaults to 36.

        Returns:
            dict: A dictionary where each key is a step label (e.g., 'step01', 'step02', ...) and each value is an instance of ModelOutputs.

        Example:
            >>> from utils_model_outputs import ModelOutputs
            >>> output_dict = ModelOutputs.make_output_dict(steps=36)
            >>> output_dict['step01'].y_score = [0.1, 0.2, 0.3]
            >>> output_dict['step01'].y_true = [1, 0, 1]
            >>> output_dict['step02'].y_score = [0.2, 0.3, 0.2]
            >>> output_dict['step02'].y_true = [1, 1, 0]
            >>> ...
        """
        return {f"step{str(i).zfill(2)}": cls() for i in range(1, steps + 1)}



# may the doc sting is a bit verbose, but for a thing like this it is probably better to be verbose than not

    @staticmethod
    def output_dict_to_dataframe(dict_of_outputs) -> pd.DataFrame:

        """
        Converts a dictionary of ModelOutputs instances into a pandas DataFrame with expanded lists.

        This method takes a dictionary where the keys are forecasting steps (e.g., 'step01', 'step02') and the values 
        are instances of the ModelOutputs data class. It converts this dictionary into a pandas DataFrame, where each 
        row corresponds to a forecasting step and each column represents one of the output attributes. List-like columns 
        are expanded so that each list element is in a separate row.

        Args:
            dict_of_outputs (Dict[str, ModelOutputs]): A dictionary where each key is a string representing a forecasting 
                                                       step, and each value is an instance of ModelOutputs containing 
                                                       model output data.

        Returns:
            pd.DataFrame: A pandas DataFrame with columns for each attribute of ModelOutputs and rows expanded 
                          from list-like columns to provide a flattened view.

        Example:
            >>> from utils_model_outputs import ModelOutputs
            >>> dict_of_outputs = {
            ...     "step01": ModelOutputs(y_score=[0.1, 0.2], y_true=[1, 0]),
            ...     "step02": ModelOutputs(y_score=[0.3, 0.4], y_true=[0, 1])
            ... }
            >>> df = ModelOutputs.output_dict_to_dataframe(dict_of_outputs)
            >>> print(df)
                   y_score  y_score_prob y_var y_var_prob  y_true y_true_binary
            step01      0.1          None  None       None     1.0          None
            step01      0.2          None  None       None     0.0          None
            step02      0.3          None  None       None     0.0          None
            step02      0.4          None  None       None     1.0          None

        Note:
            - List-like columns are expanded such that each element in the list appears in a new row.
            - Attributes in ModelOutputs that are not lists remain as-is in the DataFrame.
        """ 

        # Convert directly to a DataFrame and then explode list-like columns
        df = pd.DataFrame([{attr: getattr(instance, attr) for attr in instance.__dataclass_fields__.keys()} for instance in dict_of_outputs.values()]).apply(pd.Series.explode)

        return df

# we need to figure out if we are storing logged fatalities or not
# And this is also a good place to decide on the uncertainty quantification. Right now var, but maybe HDI or something else.
# you might also want the a non-step specific list of pgm? So you can recreate the full df from here? Otherwise this could turn into a mess

def generate_output_dict(df, config):
    """
    Generate a dictionary of ModelOutputs instances and a DataFrame from a DataFrame of model predictions.

    This function takes a DataFrame of model predictions and a configuration object, and generates a dictionary of ModelOutputs instances

    Args:
        df (pd.DataFrame): A DataFrame containing model predictions.
        config (dict): A configuration object containing model settings.

    Returns:
        output_dict (dict): A dictionary where each key is a step label and each value is an instance of ModelOutputs.
        df_output_dict (pd.DataFrame): A DataFrame of model outputs.

    Note:
        ! This is temporary for stepshifter model
    """
    output_dict = ModelOutputs.make_output_dict(steps=config["steps"][-1])
    for step in config["steps"]:
        df_step = df[[config["depvar"], f"step_pred_{step}"]]
        output_dict[f"step{str(step).zfill(2)}"].y_true = df_step[config["depvar"]].to_list()
        output_dict[f"step{str(step).zfill(2)}"].y_score = df_step[f"step_pred_{step}"].to_list()
        output_dict[f"step{str(step).zfill(2)}"].month_id = df_step.index.get_level_values("month_id").to_list()
        if df.index.names[1] == "priogrid_gid":
            output_dict[f"step{str(step).zfill(2)}"].pg_id = df_step.index.get_level_values("priogrid_gid").to_list()
        elif df.index.names[1] == "country_id":
            output_dict[f"step{str(step).zfill(2)}"].c_id = df_step.index.get_level_values("country_id").to_list()
        output_dict[f"step{str(step).zfill(2)}"].out_sample_month = step
    df_output_dict = ModelOutputs.output_dict_to_dataframe(output_dict)
    df_output_dict = df_output_dict.reset_index()
    df_output_dict = df_output_dict.drop(columns=df_output_dict.columns[0])
    return output_dict, df_output_dict