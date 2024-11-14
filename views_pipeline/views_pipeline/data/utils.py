import logging
import numpy as np
logger = logging.getLogger(__name__)

def ensure_float64(df):
        """
        Check if the DataFrame only contains np.float64 types. If not, raise a warning
        and convert the DataFrame to use np.float64 for all its numeric columns.
        """
        non_float64_cols = df.select_dtypes(include=['number']).columns[
            df.select_dtypes(include=['number']).dtypes != np.float64]

        if len(non_float64_cols) > 0:
            logger.warning(
                f"DataFrame contains non-np.float64 numeric columns. Converting the following columns: {', '.join(non_float64_cols)}")

            for col in non_float64_cols:
                df[col] = df[col].astype(np.float64)
        return df