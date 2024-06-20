import os

import numpy as np
import pickle
import time
import functools

import torch
import torch.nn as nn
import torch.nn.functional as F

import wandb

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)


from utils import choose_model, choose_loss, choose_sheduler, get_train_tensors, get_full_tensor, apply_dropout, execute_freeze_h_option, train_log, init_weights, get_data
from utils_prediction import predict, sample_posterior
from utils_forecasting import make_forecast_storage_vol
from utils_artifacts import get_latest_model_artifact
from hydra_net_outputs import output_to_df, save_model_outputs 
from config_hyperparameters import get_hp_config
from utils_hydranet_outputs import output_to_df, evaluation_to_df, save_model_outputs, update_output_dict


from utils_model_outputs import ModelOutputs
from utils_evaluation_metrics import EvaluationMetrics



def forecast_posterior(model, views_vol, df, config, device):
#def forecast_posterior(df, config):

    """
    Retrive true forecasts form sample_posterior and generate comprehensive DataFrame and volume representations of these forecasts.

    This function handles posterior predictions for multiple features over time, calculates mean and standard deviations,
    and compiles these metrics along with metadata into a DataFrame suitable for evaluation or further analysis.
    Additionally, it constructs a volume for visualizations or plotting purposes.

    Args:
        model (torch.nn.Module): Trained model used to generate posterior predictions.
        df (pd.DataFrame): DataFrame containing the initial data for generating forecast storage volume (month_id, pg_id, c_id, col, row).
        config (dict): Configuration dictionary with model parameters, including 'time_steps' and 'month_range'. BAD TERMONOLOGY!!!!
        device (torch.device): Device to run model computations (e.g., 'cuda' or 'cpu').

    Returns:
        Tuple[pd.DataFrame, np.ndarray]: 
            - DataFrame containing processed model outputs with scores, variances, and metadata.
            - 4D volume array suitable for testing and plotting.
    """

    posterior_list, posterior_list_class, _, _, _, _ = sample_posterior(model, views_vol, config, device)

    month_range = config['time_steps']

    # storage volume for forecasts
    forecast_storage_vol = make_forecast_storage_vol(month_range = month_range, to_tensor=True) # CONFIG

    # Initialize dictionary to store outputs for different features
    dict_of_outputs_dicts = {k: ModelOutputs.make_output_dict(steps = month_range) for k in ["sb", "ns", "os"]} # CONFIG - step is month_range... BAD NAME!
 
    # Calculate mean and standard deviation for posterior predictions and class probabilities
    mean_array = np.array(posterior_list).mean(axis=0)
    std_array = np.array(posterior_list).std(axis=0)
    mean_class_array = np.array(posterior_list_class).mean(axis=0)
    std_class_array = np.array(posterior_list_class).std(axis=0)

    for t in range(mean_array.shape[0]):  # Iterate over time steps
        for i, feature_key in enumerate(dict_of_outputs_dicts.keys()):  # Iterate over feature keys ('sb', 'ns', 'os')
            step = f"step{str(t + 1).zfill(2)}"

            # Extract scores and variances for each feature
            y_score = mean_array[t, i, :, :].reshape(-1)
            y_score_prob = mean_class_array[t, i, :, :].reshape(-1)
            y_var = std_array[t, i, :, :].reshape(-1)
            y_var_prob = std_class_array[t, i, :, :].reshape(-1)

            # Extract metadata: pg_id, c_id, month_id from the forecast storage volume
            pg_id = forecast_storage_vol[:, t, 0, :, :].reshape(-1)
            c_id = forecast_storage_vol[:, t, 4, :, :].reshape(-1)
            month_id = forecast_storage_vol[:, t, 3, :, :].reshape(-1)

            # Store extracted values in the output dictionary
            output_dict = dict_of_outputs_dicts[feature_key][step]
            output_dict.y_score = y_score
            output_dict.y_score_prob = y_score_prob
            output_dict.y_var = y_var
            output_dict.y_var_prob = y_var_prob
            output_dict.pg_id = pg_id
            output_dict.c_id = c_id
            output_dict.step = t + 1
            output_dict.month_id = month_id

    # Convert the output dictionaries to a DataFrame
    df_full = output_to_df(dict_of_outputs_dicts, forecast=True)

    # Drop columns related to observed data, as this is forecast-specific
    df_full = df_full.drop(columns=['y_true_sb', 'y_true_binary_sb', 'y_true_ns', 'y_true_binary_ns', 'y_true_os', 'y_true_binary_os'])

    # and make the vol just for testing and plotting - you should do this for eval as well. 
    vol_full = np.concatenate((mean_array, mean_class_array, forecast_storage_vol.squeeze().numpy()), axis=1)
    vol_full = np.transpose(vol_full, (0, 2, 3, 1))

  
    posterior_dict = {'posterior_list' : posterior_list, 'posterior_list_class': posterior_list_class, 'out_of_sample_vol' : None}
    #save_model_outputs(PATH, config, posterior_dict, dict_of_outputs_dicts)

    return df_full, vol_full, output_dict, posterior_dict



def forecast_with_model_artifact(config, device, views_vol, PATH_ARTIFACTS, artifact_name=None):
#def handle_evaluation(config, device, views_vol, PATH_ARTIFACTS, artifact_name=None):

    """
    Loads a model artifact and use to to produce true forecasts using the correcet partition (Forecasting).

    This function handles the loading of a model artifact either by using a specified artifact name
    or by selecting the latest model artifact based on the run type (default). It then produced true forecasts 
    using the the model's posterior distribution and saves the output.

    Args:
        config: Configuration object containing parameters and settings.
        device: The device to run the model on (CPU or GPU).
        views_vol: The tensor containing the input data for evaluation.
        PATH_ARTIFACTS: The path where model artifacts are stored.
        artifact_name (optional): The specific name of the model artifact to load. Defaults to None.

    Raises:
        FileNotFoundError: If the specified or default model artifact cannot be found.

    """

    # if an artifact name is provided through the CLI, use it. Otherwise, get the latest model artifact based on the run type
    if artifact_name:
        print(f"Using (non-default) artifact: {artifact_name}")
        
        # If the pytorch artifact lacks the file extension, add it. This is obviously specific to pytorch artifacts, but we are deep in the model code here, so it is fine.
        if not artifact_name.endswith('.pt'):
            artifact_name += '.pt'
        
        # Define the full (model specific) path for the artifact
        #PATH_MODEL_ARTIFACT = os.path.join(PATH_ARTIFACTS, artifact_name)

        # pathlib alternative as per sara's comment
        PATH_MODEL_ARTIFACT = PATH_ARTIFACTS / artifact_name # PATH_ARTIFACTS is already a Path object
    
    else:
        # use the latest model artifact based on the run type
        print(f"Using latest (default) run type ({config.run_type}) specific artifact")
        
        # Get the latest model artifact based on the run type and the (models specific) artifacts path
        PATH_MODEL_ARTIFACT = get_latest_model_artifact(PATH_ARTIFACTS, config.run_type)

    # Check if the model artifact exists - if not, raise an error
    #if not os.path.exists(PATH_MODEL_ARTIFACT):
    #    raise FileNotFoundError(f"Model artifact not found at {PATH_MODEL_ARTIFACT}")
    
    # Pathlib alternative as per sara's comment
    if not PATH_MODEL_ARTIFACT.exists(): # PATH_MODEL_ARTIFACT is already a Path object
        raise FileNotFoundError(f"Model artifact not found at {PATH_MODEL_ARTIFACT}")

    # load the model
    model = torch.load(PATH_MODEL_ARTIFACT)
    
    # get the exact model date_time stamp for the pkl files made in the evaluate_posterior from evaluation.py
    #model_time_stamp = os.path.basename(PATH_MODEL_ARTIFACT)[-18:-3] # 18 is the length of the timestamp string + ".pt", and -3 is to remove the .pt file extension. a bit hardcoded, but very simple and should not change.


    # Pathlib alternative as per sara's comment
    model_time_stamp = PATH_MODEL_ARTIFACT.stem[-15:] # 15 is the length of the timestamp string. This is more robust than the os.path.basename solution above since it does not rely on the file extension.

    # print for debugging
    print(f"model_time_stamp: {model_time_stamp}")

    # add to config for logging and conciseness
    config.model_time_stamp = model_time_stamp

    # evaluate the model posterior distribution
    df_full, vol_full, posterior_dict = forecast_posterior(model, views_vol, config, device)
    
    save_model_outputs(PATH, config, posterior_dict, dict_of_outputs_dicts, forecast_vol = None):


    # done. 
    print('Done testing') 




























































#
#
#def generate_forecast(model, views_vol, config, device, PATH):
#    """
#    Function to generate forecast using the provided model and views_vol.
#    It saves the generated posterior distributions and out-of-sample volumes.
#    
#    Args:
#        model: The trained model used for forecasting.
#        views_vol: The input data tensor for forecasting.
#        config: Configuration object containing settings.
#        device: The device (CPU or GPU) to run the predictions on.
#        PATH: The base path where generated data will be saved.
#    
#    Returns:
#        None
#    """
#    # Ensure the model is in evaluation mode
#    model.eval()
#    model.apply(apply_dropout)
#
#    # Generate posterior samples and out-of-sample volumes
#    posterior_list, posterior_list_class, out_of_sample_vol, _ = sample_posterior(model, views_vol, config, device) # the _ is the full tensor. 
#    
#    # I suspect you'll need the out_of_sample_vol to create the df (it has pg and ocean info)
#    # However, I see in the test_prediction_store notebook in "conflictnet" repo that I load the "calibration_vol" from the pickle file.... Investigate... 
#
#
#    # Set up paths for storing generated data
#    _, _, PATH_GENERATED = setup_data_paths(PATH)
#
#    # Create the directory if it does not exist
#    os.makedirs(PATH_GENERATED, exist_ok=True)
#
#    # Print the path for debugging
#    print(f'PATH to generated data: {PATH_GENERATED}')
#
#    # Create a dictionary to store posterior data
#    posterior_dict = {
#        'posterior_list': posterior_list,
#        'posterior_list_class': posterior_list_class,
#        'out_of_sample_vol': out_of_sample_vol          # you might need this for the df creation before predstore. Experiments in notebook test_to_prediction_store.ipynb
#    }
#
#    # Save the posterior data to a pickle file
#    filename = f'posterior_dict_{config.time_steps}_{config.run_type}_{config.model_time_stamp}.pkl'
#    with open(os.path.join(PATH_GENERATED, filename), 'wb') as file:
#        pickle.dump(posterior_dict, file)
#
#    print('Posterior dict and test vol pickled and dumped!')
#
#
#def forecast_with_model_artifact(config, device, views_vol, PATH_ARTIFACTS, artifact_name=None):
##def handle_forecasting(config, device, views_vol, PATH_ARTIFACTS, artifact_name=None):
#
#    """
#    Loads a model artifact and performs true forecasting.
#
#    This function handles loading a model artifact either by using a specified artifact name
#    or by selecting the latest model artifact based on the run type (default). It then performs forecasting
#    using the model and the current forecasting partition.
#
#    Args:
#        config: Configuration object containing parameters and settings.
#        device: The (torch) device to run the model on (CPU or GPU).
#        views_vol: The tensor containing the input data for forecasting.
#        PATH_ARTIFACTS: The path where model artifacts are stored.
#        artifact_name(optional): The specific name of the model artifact to load. Defaults to None which will lead to the latest runtype-specific artifact being loaded.
#
#    Raises:
#        FileNotFoundError: If the specified or default model artifact cannot be found.
#        NotImplementedError: Indicates that forecasting is not yet implemented.
#    """
#
#    # the thing above might work, but it needs to be tested thoroughly....
#    raise NotImplementedError('Forecasting not implemented yet')
#
#
#

# Ensure utils_prediction.py and any other dependencies are imported correctly
# from utils_prediction import sample_posterior, apply_dropout
# from utils_data import setup_data_paths


















## you always load an artifact for forecasting - like with the evaluate you take the latest artifact unless you specify another one
## But that is done in main.py - just passed to here as an argument
#
## Then the load the offical forescasting partition
## And the first steps must be usign the function from utils_prediction.py to get the predictions and the posetrior
#
## model, views_vol, config, device should be passed as arguments to this function
#
#def generate_forecast(model, views_vol, config, device):
#
#
#    # THIS IS ALL PURE MESS RIGHT NOW!!! 
#
#
#    posterior_list, posterior_list_class, out_of_sample_vol, full_tensor = sample_posterior(model, views_vol, config, device)
#
## then to prediction store I guess? Or perhaps just the generated data for now... 
#
#    _ , _, PATH_GENERATED = setup_data_paths(PATH)
#
#    # if the path does not exist, create it
#
#    if not os.path.exists(PATH_GENERATED):
#
#        os.makedirs(PATH_GENERATED)
#
#    # print for debugging
#    print(f'PATH to generated data: {PATH_GENERATED}')
#
#    # pickle the posterior dict, metric dict, and test vol
#
#    # Should be time_steps and run_type in the name....
#    posterior_dict = {'posterior_list' : posterior_list, 'posterior_list_class': posterior_list_class, 'out_of_sample_vol' : out_of_sample_vol}
#
#
#    with open(f'{PATH_GENERATED}/posterior_dict_{config.time_steps}_{config.run_type}_{config.model_time_stamp}.pkl', 'wb') as file:
#
#        pickle.dump(posterior_dict, file)       
#
#
#    print('Posterior dict, metric dict and test vol pickled and dumped!')
#
#