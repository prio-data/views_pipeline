import warnings
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

class PersistenceModel:
    def __init__(self, df, features, is_true_forecast=True, lower_date_bound="01.1990", overwrite_lastmonth_warning=False):
        """
        Initializes the PersistenceModel with the necessary parameters.

        Parameters:
        - df (pandas.DataFrame): The input dataframe containing 'pg_id', 'month_id', and feature columns.
        - features (list): A list of strings containing the names of the feature values that should be forecasted.
        - is_true_forecast (bool): If True, use the actual max month for forecasting. If False, subtract 36 months from max month.
        - lower_date_bound (str): The lower bound date in the format "MM.YYYY". Default is "01.1990".
        - overwrite_lastmonth_warning (bool): If True, suppresses errors and prints warnings instead.
        """
        self.df = df
        self.features = features
        self.is_true_forecast = is_true_forecast
        self.lower_date_bound = lower_date_bound
        self.overwrite_lastmonth_warning = overwrite_lastmonth_warning

        self.validate_input_dataframe()

    def validate_input_dataframe(self):
        """ Validates the input dataframe for necessary columns and non-emptiness. """
        if self.df.empty:
            raise ValueError("The input dataframe is empty.")
        
        if 'pg_id' not in self.df.columns:
            raise ValueError("The input dataframe does not contain the 'pg_id' column.")
        
        if 'month_id' not in self.df.columns:
            raise ValueError("The input dataframe does not contain the 'month_id' column.")
        
        for feature in self.features:
            if feature not in self.df.columns:
                raise ValueError(f"The input dataframe does not contain the '{feature}' column.")

    def calculate_date_from_index(self, target_index, start_index=121, start_date='01.1990'):
        """
        Calculates the month-year date for a given target index based on the start index and start date.

        Parameters:
        start_index (int): The index corresponding to the start date.
        start_date (str): The start date in 'MM.YYYY' format.
        target_index (int): The index for which the month-year date is required.

        Returns:
        str: The calculated month-year date corresponding to the target_index in 'MM.YYYY' format.
        """
        base_date = datetime.strptime(start_date, '%m.%Y')
        month_difference = target_index - start_index
        target_date = base_date + relativedelta(months=month_difference)
        return target_date.strftime('%m.%Y')

    def check_max_month(self, max_month):
        """
        Checks if the max_month is within the valid range (inclusive) from a given lower bound to the current month.

        Parameters:
        - max_month (str): The month to check in the format "MM.YYYY".
        
        Returns:
        - bool: True if the date is within the range, otherwise raises an error or prints a warning.
        """
        date_format = "%m.%Y"
        
        max_month_date = datetime.strptime(max_month, date_format)
        min_date = datetime.strptime(self.lower_date_bound, date_format)
        current_date = datetime.now().replace(day=1)  # Use the first day of the current month

        if max_month_date < min_date or max_month_date > current_date:
            message = (f"The max_month {max_month} is out of the valid range "
                       f"({self.lower_date_bound} to {current_date.strftime(date_format)}).")
            if self.overwrite_lastmonth_warning:
                warnings.warn(message)
            else:
                raise ValueError(message)
        
        return True

    def get_persistence_model_predictions(self):
        """
        Generate persistence model predictions for time series forecasting.

        Returns:
        - pandas.DataFrame: A dataframe with 'pg_id', the specified features suffixed 
                            with '_persistence', and 'step' columns, extended from 
                            step 1 to 36 with constant values.
        """
        # Get the max month_id and date    
        max_month_id = self.df["month_id"].max()

        if not self.is_true_forecast:
            # Subtract 36 months for validation or evaluation
            max_month_id -= 36

        max_month_date = self.calculate_date_from_index(max_month_id)

        # Get the current date formatted as MM.YYYY
        current_month_date = datetime.now().strftime("%m.%Y")

        # Print statement reflecting whether it's a true forecast or validation/evaluation
        mode = "True Forecast" if self.is_true_forecast else "Validation/Evaluation (Adjusted 36 months earlier)"
        print(f"[{mode}] The max month is {max_month_date} with month_id {max_month_id}. Ensure this corresponds to your expectations! Current date is {current_month_date}.")

        # Check if the max_month is within the valid range    
        self.check_max_month(max_month_date)

        sub_df = self.df[self.df['month_id'] == max_month_id][['pg_id'] + self.features].copy()
        sub_df['step'] = 0

        dfs = [sub_df]

        for step in range(1, 37):
            new_sub_df = sub_df.copy()
            new_sub_df['step'] = step
            dfs.append(new_sub_df)

        extended_sub_df = pd.concat(dfs, ignore_index=True)
        extended_sub_df = extended_sub_df[extended_sub_df['step'] != 0]

        # Dynamically rename feature columns
        rename_mapping = {feature: f"{feature}_persistence" for feature in self.features}
        extended_sub_df.rename(columns=rename_mapping, inplace=True)

        if extended_sub_df.empty:
            raise ValueError("The output dataframe is empty - something went wrong!")

        return extended_sub_df


# Example usage
# model = PersistenceModel(df_test, ['ln_sb_best', 'ln_os_best', 'ln_ns_best'], is_true_forecast=False)
# df_persistence = model.get_persistence_model_predictions()
# print(df_persistence)
