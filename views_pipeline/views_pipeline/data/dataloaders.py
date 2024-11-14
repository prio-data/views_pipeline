import os
import numpy as np
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
from views_pipeline.configs import drift_detection
from views_pipeline.files.utils import create_data_fetch_log_file
from views_pipeline.managers.path_manager import ModelPath
from typing import Dict
from ingester3.ViewsMonth import ViewsMonth
from views_pipeline.data.utils import ensure_float64

logger = logging.getLogger(__name__)


class ViewsDataLoader:
    """
    A class to handle data loading, fetching, and processing for different partitions.

    This class provides methods to fetch data from viewser, validate data partitions,
    create or load volumes, and handle drift detection configurations.
    """

    def __init__(self, model_path: ModelPath, **kwargs):
        """
        Initializes the DataLoaders class with a ModelPath object and optional keyword arguments.

        Args:
            model_path (ModelPath): An instance of the ModelPath class.
            **kwargs: Additional keyword arguments to set instance attributes.

        Attributes:
            partition (str, optional): The partition type. Defaults to None.
            partition_dict (dict, optional): The dictionary containing partition information. Defaults to None.
            drift_config_dict (dict, optional): The dictionary containing drift detection configuration. Defaults to None.
            override_month (str, optional): The override month. Defaults to None.
            month_first (str, optional): The first month in the range. Defaults to None.
            month_last (str, optional): The last month in the range. Defaults to None.
        """
        self._model_path = model_path
        self._model_name = model_path.model_name
        if self._model_path.target == "model":
            self._path_raw = model_path.data_raw
        self._path_processed = model_path.data_processed
        self.partition = None
        self.partition_dict = None
        self.drift_config_dict = None
        self.override_month = None
        self.month_first, self.month_last = None, None

        for key, value in kwargs.items():
            setattr(self, key, value)

    def _get_partition_dict(self, step=36) -> Dict:
        """
        Returns the partitioner dictionary for the given partition.

        Args:
            step (int, optional): The step size for the forecasting partition. Defaults to 36.

        Returns:
            dict: A dictionary containing the train and predict ranges for the specified partition.

        Raises:
            ValueError: If the partition attribute is not one of "calibration", "testing", or "forecasting".

        Notes:
            - For the "calibration" partition, the train range is (121, 396) and the predict range is (397, 444).
            - For the "testing" partition, the train range is (121, 444) and the predict range is (445, 492).
            - For the "forecasting" partition, the train range starts at 121 and ends at the current month minus 2.
              The predict range starts at the current month minus 1 and extends by the step size.
        """
        match self.partition:
            case "calibration":
                return {
                    "train": (121, 396),
                    "predict": (397, 444),
                }  # calib_partitioner_dict - (01/01/1990 - 12/31/2012) : (01/01/2013 - 31/12/2015)
            case "testing":
                return {"train": (121, 444), "predict": (445, 492)}
            case "forecasting":
                month_last = (
                    ViewsMonth.now().id - 2
                )  # minus 2 because the current month is not yet available. Verified but can be tested by changing this and running the check_data notebook.
                return {
                    "train": (121, month_last),
                    "predict": (month_last + 1, month_last + 1 + step),
                }  # is it even meaningful to have a predict partition for forecasting? if not you can remove steps
            case _:
                raise ValueError(
                    'partition should be either "calibration", "testing" or "forecasting"'
                )

    def _fetch_data_from_viewser(self, self_test: bool) -> tuple[pd.DataFrame, list]:
        """
        Fetches and prepares the initial DataFrame from viewser.

        Args:
            month_first (int): The first month ID to fetch.
            month_last (int): The last month ID to fetch.
            self_test (bool): Flag indicating whether to perform self-testing.

        Returns:
            pd.DataFrame: The prepared DataFrame with initial processing done.
            list: List of alerts generated during data fetching.

        Raises:
            RuntimeError: If the queryset for the model is not found.
        """
        logger.info(
            f"Beginning file download through viewser with month range {self.month_first},{self.month_last}"
        )

        queryset_base = self._model_path.get_queryset()  # just used here..
        if queryset_base is None:
            raise RuntimeError(
                f"Could not find queryset for {self._model_name} in common_querysets"
            )
        else:
            logger.info(f"Found queryset for {self._model_name} in common_querysets")

        df, alerts = queryset_base.publish().fetch_with_drift_detection(
            start_date=self.month_first,
            end_date=self.month_last - 1,
            drift_config_dict=self.drift_config_dict,
            self_test=self_test,
        )

        df = ensure_float64(df)  # The dataframe must contain only np.float64 floats
        #    with wandb.init(project=f'{model_path.model_name}', entity="views_pipeline"):
        for ialert, alert in enumerate(
            str(alerts).strip("[").strip("]").split("Input")
        ):
            if "offender" in alert:
                logger.warning(
                    {f"{self._model_path.model_name} data alert {ialert}": str(alert)}
                )

        # Not required for stepshift model
        # df.reset_index(inplace=True)
        # df.rename(columns={'priogrid_gid': 'pg_id'}, inplace=True) # arguably HydraNet or at lest vol specific
        # df['in_viewser'] = True  # arguably HydraNet or at lest vol specific

        return df, alerts

    def _get_month_range(self) -> tuple[int, int]:
        """
        Determines the month range based on the partition type.

        Returns:
            tuple: The start and end month IDs for the partition.

        Raises:
            ValueError: If partition is not 'calibration', 'testing', or 'forecasting'.
        """
        month_first = self.partition_dict["train"][0]

        if self.partition == "forecasting":
            month_last = self.partition_dict["train"][1] + 1
        elif self.partition in ["calibration", "testing"]:
            month_last = self.partition_dict["predict"][1] + 1
        else:
            raise ValueError(
                'partition should be either "calibration", "testing" or "forecasting"'
            )
        if self.partition == "forecasting" and self.override_month is not None:
            month_last = self.override_month
            logger.warning(
                f"Overriding end month in forecasting partition to {month_last} ***\n"
            )

        return month_first, month_last

    def _validate_df_partition(
        self, df: pd.DataFrame
    ) -> bool:
        """
        Checks to see if the min and max months in the input dataframe are the same as the min
        month in the train and max month in the predict portions (or min and max months in the train portion for
        the forecasting partition).

        Args:
            df (pd.DataFrame): The dataframe to be checked.
            partition_dict (Dict): The partition dictionary.
            override_month (int, optional): If user has overridden the end month of the forecasting partition, this value
                                            is substituted for the last month in the forecasting train portion.

        Returns:
            bool: True if the dataframe is valid for the partition, False otherwise.
        """
        if "month_id" in df.columns:
            df_time_units = df["month_id"].values
        else:
            df_time_units = df.index.get_level_values("month_id").values
        # partitioner_dict = get_partitioner_dict(partition)
        if self.partition in ["calibration", "testing"]:
            first_month = self.partition_dict["train"][0]
            last_month = self.partition_dict["predict"][1]
        else:
            first_month = self.partition_dict["train"][0]
            last_month = self.partition_dict["train"][1]
            if self.override_month is not None:
                last_month = self.override_month - 1
        if [np.min(df_time_units), np.max(df_time_units)] != [first_month, last_month]:
            return False
        else:
            return True

    @staticmethod
    def filter_dataframe_by_month_range(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filters the DataFrame to include only the specified month range.

        Args:
            df (pd.DataFrame): The input DataFrame to be filtered.
            month_first (int): The first month ID to include.
            month_last (int): The last month ID to include.

        Returns:
            pd.DataFrame: The filtered DataFrame.
        """
        month_range = np.arange(self.month_first, self.month_last)
        return df[df["month_id"].isin(month_range)].copy()

    def get_data(
        self,
        self_test: bool,
        partition: str,
        use_saved: bool,
        validate: bool = True,
        override_month: int = None,
    ) -> tuple[pd.DataFrame, list]:
        """
        Fetches or loads a DataFrame for a given partition from viewser.

        This function handles the retrieval or loading of raw data for the specified partition.

        The default behaviour is to fetch fresh data via viewser. This can be overridden by setting the
        used_saved flag to True, in which case saved data is returned, if it can be found.

        Args:
            self_test (bool): Flag indicating whether to perform self-testing.
            use_saved (bool, optional): Flag indicating whether to use saved data if available.
            override_month (int, optional): If provided, overrides the end month for the forecasting partition.

        Returns:
            pd.DataFrame: The DataFrame fetched or loaded from viewser, with minimum preprocessing applied.
            list: List of alerts generated during data fetching.

        Raises:
            RuntimeError: If the saved data file is not found or if the data is incompatible with the partition.
        """
        self.partition = partition #if self.partition is None else self.partition
        self.partition_dict = self._get_partition_dict() #if self.partition_dict is None else self.partition_dict
        self.drift_config_dict = drift_detection.drift_detection_partition_dict[
            partition
        ] if self.drift_config_dict is None else self.drift_config_dict
        self.override_month = override_month if self.override_month is None else override_month
        if self.month_first is None or self.month_last is None:
            self.month_first, self.month_last = self._get_month_range()

        path_viewser_df = Path(
            os.path.join(str(self._path_raw), f"{self.partition}_viewser_df.pkl")
        )  # maby change to df...
        alerts = None

        if use_saved:
            # Check if the VIEWSER data file exists
            try:
                if path_viewser_df.exists():
                    df = pd.read_pickle(path_viewser_df)
                    logger.info(f"Reading saved data from {path_viewser_df}")
            except Exception as e:
                raise RuntimeError(
                    f"Use of saved data was specified but getting {path_viewser_df} failed with: {e}"
                )
        else:
            logger.info(f"Fetching data from viewser...")
            df, alerts = self._fetch_data_from_viewser(
                self_test
            )  # which is then used here
            data_fetch_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            create_data_fetch_log_file(
                self._path_raw, self.partition, self._model_name, data_fetch_timestamp
            )
            logger.info(f"Saving data to {path_viewser_df}")
            df.to_pickle(path_viewser_df)
        if validate:
            if self._validate_df_partition(df=df):
                return df, alerts
            else:
                raise RuntimeError(
                    f"file at {path_viewser_df} incompatible with partition {self.partition}"
                )
        logger.debug(f"DataFrame shape: {df.shape if df is not None else 'None'}")
        for ialert, alert in enumerate(
            str(alerts).strip("[").strip("]").split("Input")
        ):
            if "offender" in alert:
                logger.warning({f"{partition} data alert {ialert}": str(alert)})

        return df, alerts
    