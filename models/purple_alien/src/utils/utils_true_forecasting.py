import wandb
import numpy as np
import torch
import matplotlib.pyplot as plt

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_artifacts_paths
setup_project_paths(PATH)

from utils_df_to_vol_conversion import get_requried_columns_for_vol


def generate_fake_vol(vol, month_range=36):
    """
    Generates a fake prediction volume for testing purposes by extracting the last three features from the input volume.
    Assumes the last three features represent `sb`, `ns`, and `os`.

    Args:
        vol (np.ndarray): The input 4D volume array with shape [n_months, height, width, n_features].
        n_months (int): The number of months to include in the fake volume. Default is 36.

    Returns:
        np.ndarray: A volume array with the last three features, shape [32, height, width, 3].
                    Represents a subset of the original volume for testing.
    """
    # Extract the last three features from the volume
    fake_vol = vol[-month_range:, :, :, 5:]  

    return fake_vol


def make_forecast_storage_vol(df, heigth = 180, width = 180, month_range = 36, to_tensor = True):
    """
    Creates a forecast storage volume based on the last month of data in the DataFrame.
    The volume is repeated for the specified `month_range` with incrementally adjusted month IDs.

    Args:
        df (pd.DataFrame): The input DataFrame containing spatial-temporal data.
                           Expected columns include 'abs_row', 'abs_col', 'abs_month', 'pg_id', 'col', 
                           'row', 'month_id', 'c_id'.

        month_range (int): The number of months to forecast into the future. Default is 36.

    Returns:
        np.ndarray: The forecast storage volume with shape [month_range, 180, 180, 5].
                    Each time slice in the volume represents a future month based on the last month of data.
    """

    # Infer the last month_id from the DataFrame
    last_month_id = df['month_id'].max()

    # Create a sub DataFrame of only the last month
    sub_df = df[df['month_id'] == last_month_id].copy()

    # required features
    required_columns = get_requried_columns_for_vol()

    # check if the required columns are in the df
    for col in required_columns:
        if col not in sub_df.columns:
            raise ValueError(f"Column '{col}' not found in the DataFrame. Check the input DataFrame (located in 'data/raw') and try again.")

    # Initialize the volume array
    features_num = len(required_columns)  # Adjust this based on the number of features you have - MUST BE INFERED FROM THE DATA

    # Create the zero array with only the last month
    vol = np.zeros([heigth, width, 1, features_num])

    # Adjust abs_month to 0 for the initial volume
    sub_df['adjusted_abs_month'] = 0

    for i, j in enumerate(required_columns):
        vol[sub_df['abs_row'], sub_df['abs_col'], sub_df['adjusted_abs_month'], i] = sub_df[j]

    # Stack the volume to the desired month range
    vol = np.repeat(vol, month_range, axis=2)

    # THIS IS A WIERD THING AND THERE COULD BE A BUG HERE.... :
    # Adjust the month_id with an increment of 1
    for i in range(month_range):
        vol[:, :, i, 3] = last_month_id + i + 1 # to get one month after the last observed month

    # Reorient and transpose
    vol = np.flip(vol, axis=0)
    vol = np.transpose(vol, (2, 0, 1, 3))

    print(f'Volume of shape {vol.shape} created. Should be ({month_range}, 180, 180, {features_num})')

    #  Convert to tensor and permute the dimensions. This make the vol similar to the out_of_sample_meta_vol and thus aligns the forcasting rutine with the eval rutine-
    if to_tensor:
        vol = torch.tensor(vol.copy()).float().unsqueeze(dim=0).permute(0,1,4,2,3) # the copy thing is weird but it works

    return vol



def merge_vol(forecast_storage_vol, vol_fake):
    """
    Merges a forecast volume with an existing forecast storage volume.
    Combines the features from `vol_fake` with `vol` along the feature axis.

    Args:
        vol (np.ndarray): The forecast storage volume with shape [n_months, height, width, n_features].
        vol_fake (np.ndarray): The forecast volume to be merged with shape [n_months, height, width, n_features_fake].

    Returns:
        np.ndarray: The merged volume with shape [n_months, height, width, n_features + n_features_fake].
    """
    # Merge the forecast volume with the storage volume along the feature axis
    full_vol = np.concatenate([forecast_storage_vol, vol_fake], axis=-1)

    # print the shape of the full volume
    print(f'Volume of shape {full_vol.shape} created. Should be ({forecast_storage_vol.shape[0]}, 180, 180, {forecast_storage_vol.shape[3] + vol_fake.shape[3]})')

    return full_vol


def check_vol_equal(vol, full_vol):
    """
    Unit test to verify the merging of two volumes.
    Checks if the original volume and the merged volume are equivalent.

    Args:
        vol (np.ndarray): The original volume.
        full_vol (np.ndarray): The merged volume.

    Returns:
        None: Prints the result of the equivalence test.
    """

    #print the shape of the volumes
    print(vol.shape)
    print(full_vol.shape)

    # trim original volume to the same shape as the full volume - ie. the last n months
    month_range = full_vol.shape[0]
    vol_trimmed = vol[-month_range:, :, :, :]

    # print the shape of the trimmed volume
    print(vol_trimmed.shape)

    # now go through each feature individually and check if they are the same

    list_features = ['pg_id', 'col', 'row', 'month_id', 'c_id', 'ln_sb_best', 'ln_ns_best', 'ln_os_best']

    for i in range(vol_trimmed.shape[-1]):
        print(f"Feature {i}, {list_features[i]} equal:", np.array_equal(vol_trimmed[:, :, :, i], full_vol[:, :, :, i]))


def check_month_id_consistency(forecast_storage_vol, df, month_range = 36):
    """
    Checks the consistency of month_id values between the forecast storage volume and the DataFrame.

    Args:
        forecast_storage_vol (np.ndarray): The forecast storage volume with shape [batch, time, feature, height, width].
        df (pd.DataFrame): The DataFrame containing month_id values.
        month_range (int): The expected range of months in the forecast storage volume.

    Raises:
        ValueError: If there is a mismatch in month_id values between the forecast storage volume and the DataFrame.
    """
    # print shapes for debugging
    print(forecast_storage_vol.shape)

    # Retrieve month_id values
    min_month_id_df = df["month_id"].min()
    max_month_id_df = df["month_id"].max()
    min_month_id_vol = forecast_storage_vol[:, :, 3, :, :].min()
    max_month_id_vol = forecast_storage_vol[:, :, 3, :, :].max()

    # Print month_id values for debugging
    print(f'Min month_id in df: {min_month_id_df}')
    print(f'Max month_id in df: {max_month_id_df}')
    print(f'Min month_id in forecast storage: {min_month_id_vol}')
    print(f'Max month_id in forecast storage: {max_month_id_vol}')

    # so we are forecasting 36 months ahead
    print(f'month forecasted ahead: {int(max_month_id_vol - min_month_id_vol + 1)}') 

    # Check if min month_id in the forecast storage volume is 1 above the max month_id in the df
    if min_month_id_vol != max_month_id_df + 1:
        raise ValueError(f"Mismatch in month_id: Expected minimum month_id in storage volume to be {max_month_id_df + 1}, but got {min_month_id_vol}.")

    # Check if max month_id in the forecast storage volume is month_range above the max month_id in the df
    if max_month_id_vol != max_month_id_df + month_range:
        raise ValueError(f"Mismatch in month_id: Expected maximum month_id in storage volume to be {max_month_id_df + month_range}, but got {max_month_id_vol}.")


def plot_vol_comparison(vol, new_vol, month_range=36):
    """
    Plots a comparison of slices from two 4D volume arrays for the specified month range.
    Displays different feature maps for each time step in separate subplots for both volumes.

    Args:
        vol (np.ndarray): The original 4D volume array with shape [n_months, height, width, n_features].
        new_vol (np.ndarray): The new 4D volume array to compare with, with the same shape as `vol`.
        month_range (int): The number of slices (time steps) to plot. Default is 36.

    Returns:
        None: Displays the plots.
    """
    features_titles = ['pg_id', 'col', 'row', 'month_id', 'c_id', 'ln_sb_best', 'ln_ns_best', 'ln_os_best']
    n_features = vol.shape[-1]

    # Ensure the volumes cover the last month_range months
    vol = vol[-month_range:, :, :, :]
    new_vol = new_vol[-month_range:, :, :, :]

    for i in range(month_range):
        fig, ax = plt.subplots(2, n_features, figsize=(20, 7))  # 2 rows, n_features columns
        
        for j in range(n_features):  # Adjusted to use n_features directly
            # Plot the original volume in the first row
            im1 = ax[0, j].imshow(vol[i, :, :, j], cmap='rainbow',
                                  vmin=vol[:, :, :, j].min(), vmax=vol[:, :, :, j].max())
            ax[0, j].set_title(features_titles[j] if j < len(features_titles) else f'Feature {j}')
            #plt.colorbar(im1, ax=ax[0, j])

            # Plot the new volume in the second row
            im2 = ax[1, j].imshow(new_vol[i, :, :, j], cmap='rainbow',
                                  vmin=new_vol[:, :, :, j].min(), vmax=new_vol[:, :, :, j].max())
            ax[1, j].set_title(f'New {features_titles[j]}' if j < len(features_titles) else f'New Feature {j}')
            #plt.colorbar(im2, ax=ax[1, j])

        # Adding title with specific adjustment
        fig.suptitle(f'Time Step {i + 1}', fontsize=16, y=1.05)  # Adjust `y` for title position

        # Remove ticks
        for a in ax.flat:
            a.set_xticks([])
            a.set_yticks([])

        # Adjust layout
        plt.subplots_adjust(left=0.05, right=0.95, top=0.85, bottom=0.15, wspace=0.2, hspace=0.4)
        plt.tight_layout(pad=2.0, rect=[0, 0, 1, 0.95])  # `rect` adjusts the position of subplots
        
        plt.show()
