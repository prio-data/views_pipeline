import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_requried_columns_for_vol():

    """
    Returns the list of required columns for constructing the volume array.
    
    These columns are necessary for creating the spatial-temporal volume format used by models
    such as HydraNet and other CNN-based models. The minimum volume array includes data for 
    spatial coordinates, temporal indices, and identifiers for grid cells. 
    Beynd these columns, the volume typically includes "forecast feeatures", 
    for instance "ln_sb_best", "ln_ns_best", and "ln_os_best" for the three event types. 

    Returns:
        list of str: A list of column names required to create the volume array, specifically:
                     - 'pg_id': Priogrid ID, a unique identifier for grid cells.
                     - 'col': Column index in the spatial grid.
                     - 'row': Row index in the spatial grid.
                     - 'month_id': Temporal index for months.
                     - 'c_id': Country ID or relevant identifier.    
    """

    required_columns = ['pg_id', 'col', 'row', 'month_id', 'c_id']

    return required_columns


def calculate_absolute_indices(df): # arguably HydraNet or at lest vol specific
    """
    Computes absolute indices for 'row', 'col', and 'month_id' in the DataFrame.    
    This is needed to turn as pandas df into a numpy array (volume).
    The volme is the data format need be the e.g. HydraNet model(s).

    Args:
        df (pd.DataFrame): The input DataFrame with columns 'row', 'col', and 'month_id'.

    Returns:
        pd.DataFrame: The DataFrame with added 'abs_row', 'abs_col', and 'abs_month' columns.
    """
    
    # get the first month_id
    month_first = df['month_id'].min() 
    
    # calculate the absolute indices
    df['abs_row'] = df['row'] - df['row'].min()         
    df['abs_col'] = df['col'] - df['col'].min()
    df['abs_month'] = df['month_id'] - month_first

    return df


def df_to_vol(df, height = 180, width = 180, forecast_features = ['ln_sb_best', 'ln_ns_best', 'ln_os_best']):


    """
    Converts a DataFrame into a 4D numpy array (volume) for spatial-temporal data representation.
    
    This volume format is used by models like HydraNet and other CNN-based models. The resulting
    volume array has dimensions [n_months, height, width, n_features].

    Args:
        df (pd.DataFrame): The input DataFrame containing spatial-temporal data. Must include columns:
                           - 'pg_id': Priogrid ID.
                           - 'col': Column index in the spatial grid.
                           - 'row': Row index in the spatial grid.
                           - 'month_id': Temporal index for months.
                           - 'c_id': Country ID or relevant identifier.

        height (int, optional): The height of the spatial grid. Defaults to 180 which fits Africa and the Middle East.
        
        width (int, optional): The width of the spatial grid. Defaults to 180 which fits Africa and the Middle East.
        
        forecast_features (list of str, optional): List of forcast feature columns to include in the volume.
                                                   Defaults to ['ln_sb_best', 'ln_ns_best', 'ln_os_best'].

    Returns:
        np.ndarray: A 4D volume array with shape [n_months, height, width, n_features].
                    Where n_features is the total number of required and forecast features combined. Given the default settings the default shape is [n_months, 180, 180, 8].

    Raises:
        ValueError: If any of the required columns ('pg_id', 'col', 'row', 'month_id', 'c_id') are missing from the DataFrame.

    """

    #required_columns = ['pg_id', 'col', 'row', 'month_id', 'c_id']
    required_columns = get_requried_columns_for_vol()
    
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f'Column {col} not found in the DataFrame. Please check your viewser query set in "model"/configs/config_input_data.py')

    vol_features =  required_columns + forecast_features

    n_features = len(vol_features)

    month_first = df['month_id'].min()
    month_last = df['month_id'].max()
    month_range = month_last - month_first + 1

    # DANGER! Right now this changes (adds columns) to the input DataFrame. Bad practice change later... 
    # You could just do df_abs = calculate_absolute_indices(df) and then use df_abs in the rest of the function.
    # But I dont want to break anything now...
    df = calculate_absolute_indices(df) # abs_row, abs_col, abs_month needed for the volume

    vol = np.zeros([height, width, month_range, n_features]) # Create the volume array.

    for i, feature in enumerate(vol_features):
        vol[df['abs_row'], df['abs_col'], df['abs_month'], i] = df[feature] 

    vol = np.flip(vol, axis=0)  # Flip the rows, so north is up.
    vol = np.transpose(vol, (2, 0, 1, 3))  # Move the month dimension to the front.

    print(f'Volume of shape {vol.shape} created. Should be (n_months, 180, 180, 8)')

    return vol


def vol_to_df(vol, forecast_features = ['ln_sb_best', 'ln_ns_best', 'ln_os_best']):

    """
    Converts a 4D numpy array (volumne) back into a DataFrame.
    
    This function is used to transform the 4D volume format used by models like HydraNet back into 
    a DataFrame. Th purpose is to cehck that the conversion between DataFrame and volume does not alter data, 
    thus verifying consistency between df_to_vol and vol_to_df operations.

    Args:
        vol (np.ndarray): The input 4D volume array (created with df_to_vol()) to be converted, with shape 
                          [n_months, height, width, n_features].
                          - n_months: Number of temporal steps (months).
                          - height: Height of the spatial grid.
                          - width: Width of the spatial grid.
                          - n_features: Number of features per grid cell.

        forecast_features (list of str, optional): List of feature names corresponding to 
                                                   the forecast features in the volume. 
                                                   Defaults to ['ln_sb_best', 'ln_ns_best', 'ln_os_best'].

    Returns:
        pd.DataFrame: The DataFrame representation of the volume array containing columns:
                      'pg_id', 'col', 'row', 'month_id', 'c_id', followed by forecast features.
                      Rows where 'pg_id' is 0 are removed. This datafreame should be identical to the original DataFrame used to create the volume via df_to_vol().

    Raises:
        ValueError: If the number of features in the volume does not match the expected number 
                    of features (length of required + forecast features)    
    """

    required_columns = get_requried_columns_for_vol()

    vol_features =  required_columns + forecast_features
    n_features = len(vol_features)

    # check that the n_features is the same as the last dimension of the volume
    if n_features != vol.shape[3]:
        raise ValueError(f'Number of features in the volume array ({vol.shape[3]}) does not match the number of features expected ({n_features}).')

    feature_dict  = {}
    for i, feature in enumerate(vol_features):
        feature_dict[feature] = vol[:, :, :, i].flatten()

    df = pd.DataFrame(feature_dict)

    # Correct the data types for required columns
    for col in required_columns:
        df[col] = df[col].astype(int)

    # Remove rows where 'pg_id' is 0 - these are ocean cells and not PRIO grid cells as such.
    df = df[df['pg_id'] != 0]

    print(f'DataFrame of shape {df.shape} created. Should be (n_months * 180 * 180, 8)')

    return df



def df_vol_conversion_test(df, vol, forecast_features = ['ln_sb_best', 'ln_ns_best', 'ln_os_best']):

    """
    Tests the consistency of DataFrame and volume array conversions.
    
    This unit test verifies that converting a DataFrame to a 4D volume array and back to a DataFrame
    results in the original data. It ensures the `df_to_vol` and `vol_to_df` functions are consistent
    and that data integrity is maintained during the transformations.

    Args:
        df (pd.DataFrame): The original DataFrame containing the spatial-temporal data.
                           Must include columns: 'pg_id', 'col', 'row', 'month_id', 'c_id', and forecast features.

        vol (np.ndarray): The 4D volume array obtained from the DataFrame conversion via df_to_vol().
                          Shape should be [n_months, height, width, n_features].

        forecast_features (list of str, optional): List of feature names included in the volume. Defaults to 
                                                   ['ln_sb_best', 'ln_ns_best', 'ln_os_best'].

    Returns:
        None: This function does not return a value. It prints the result of the equivalence test between
              the original DataFrame and the DataFrame recreated from the volume array.
    """

    # Make a copy of the original DataFrame
    df_copy = df.copy()

    # Proof of concept: Check if the copy is the same as the original
    print("Original DataFrame equals its copy:", df.equals(df_copy))

    # Convert the volume back into a DataFrame
    df_recreated = vol_to_df(vol)

    # Trim the original DataFrame to match the features of the recreated DataFrame
    required_columns = ['pg_id', 'col', 'row', 'month_id', 'c_id']
    vol_features =  required_columns + forecast_features
    df_trimmed = df[vol_features]

    # Sort both DataFrames by 'pg_id' and 'month_id'
    df_trimmed = df_trimmed.sort_values(by=['pg_id', 'month_id'])
    df_recreated = df_recreated.sort_values(by=['pg_id', 'month_id'])

    # Reset the index to ensure alignment
    df_trimmed = df_trimmed.reset_index(drop=True)
    df_recreated = df_recreated.reset_index(drop=True)

    # Check if the two DataFrames are the same
    is_equal = df_trimmed.equals(df_recreated)
    print("Trimmed original DataFrame equals recreated DataFrame from volume:", is_equal)



def plot_vol(vol, month_range, forecast_features = ['ln_sb_best', 'ln_ns_best', 'ln_os_best']):

    """
    Plots feature maps from a 4D volume array over a specified range of months.
    
    This function generates and displays plots for each feature in the volume array for the last `month_range` time steps.
    Each subplot corresponds to a different feature map at each time step, allowing visualization of spatial-temporal data.
    The main purpose of this function is to provide a visual representation of the data in the volume array to check that it is sound and as expected.

    Args:
        vol (np.ndarray): The input 4D volume array with shape [n_months, height, width, n_features].
                          - n_months: Number of time steps (months).
                          - height: Height of the spatial grid.
                          - width: Width of the spatial grid.
                          - n_features: Number of features per grid cell.

        month_range (int): The number of recent time steps (months) to plot. This should be less than or equal to the number of months in `vol`.

        forecast_features (list of str, optional): List of additional feature names to include in the plots.
                                                   Defaults to ['ln_sb_best', 'ln_ns_best', 'ln_os_best'].

    Returns:
        None: The function displays the plots for each time step and feature, but does not return any value.

    Raises:
        ValueError: If `month_range` exceeds the number of time steps in `vol`.

    """

    # check if the month_range is valid:
    if month_range > vol.shape[0]:
        raise ValueError(f"month_range ({month_range}) exceeds the number of time steps in the volume ({vol.shape[0]}).")

    # get the required columns and feature titles
    required_columns = get_requried_columns_for_vol()
    features_titles = required_columns + forecast_features
    n_features = vol.shape[-1]

    # get sub_df of the lasst month_range months
    vol = vol[-month_range:, :, :, :]

    for i in range(month_range):
        fig, ax = plt.subplots(1, n_features, figsize=(15, 4))
        
        for j in range(min(n_features, vol.shape[-1])):  # Handle cases where there are fewer than 7 features
            im = ax[j].imshow(vol[i, :, :, j], cmap='rainbow', vmin= vol[:, :, :, j].min(), vmax= vol[:, :, :, j].max())
            ax[j].set_title(features_titles[j] if j < len(features_titles) else f'Feature {j}')

        # Adding title with specific adjustment
        fig.suptitle(f'Time Step {i + 1}', fontsize=16, y=0.75)  # Adjust `y` for title position

        # remove ticks
        for a in ax:
            a.set_xticks([])
            a.set_yticks([])

        # Adjust layout
        plt.subplots_adjust(left=0.1, right=1, top=0.85, bottom=0.55, wspace=0.2, hspace=-0)
        plt.tight_layout(pad=2.0, rect=[0, 0, 1, 0.9])  # `rect` adjusts the position of subplots
        
        plt.show()