import os

import numpy as np
import pickle
import time
import functools

import torch
import torch.nn as nn
import torch.nn.functional as F

#from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import average_precision_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import brier_score_loss

import wandb

import sys
from pathlib import Path

PATH = Path(__file__)
sys.path.insert(0, str(Path(*[i for i in PATH.parts[:PATH.parts.index("views_pipeline")+1]]) / "common_utils")) # PATH_COMMON_UTILS  
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)


from utils import choose_model, choose_loss, choose_sheduler, get_train_tensors, get_full_tensor, apply_dropout, execute_freeze_h_option, train_log, init_weights, get_data
from utils_prediction import predict, sample_posterior
from utils_artifacts import get_latest_model_artifact
from utils_wandb import generate_wandb_log_dict
from config_sweep import get_swep_config
from config_hyperparameters import get_hp_config
from utils_hydranet_outputs import output_to_df, evaluation_to_df


from utils_model_outputs import ModelOutputs
from utils_evaluation_metrics import EvaluationMetrics


# so if this is mand more general and the if evals in activated then it should be in the utils_prediction.py file.
# also it could 100% be multiple functions...
def evaluate_posterior(model, views_vol, config, device): # is eval in config?

    posterior_list, posterior_list_class, out_of_sample_vol, out_of_sample_meta_vol, full_tensor, metadata_tensor = sample_posterior(model, views_vol, config, device)

    #if eval:
    dict_of_eval_dicts = {}
    dict_of_eval_dicts = {k: EvaluationMetrics.make_evaluation_dict(steps=config.time_steps) for k in ["sb", "ns", "os"]}

    dict_of_outputs_dicts = {}
    dict_of_outputs_dicts = {k: ModelOutputs.make_output_dict(steps=config.time_steps) for k in ["sb", "ns", "os"]}

    # Get mean and std
    mean_array = np.array(posterior_list).mean(axis = 0) # get mean for each month!
    std_array = np.array(posterior_list).std(axis = 0)

    mean_class_array = np.array(posterior_list_class).mean(axis = 0) # get mean for each month!
    std_class_array = np.array(posterior_list_class).std(axis = 0)

    #NEW
    log_dict_list = []

    for t in range(mean_array.shape[0]): #  0 of mean array is the temporal dim    

        log_dict = {}
        log_dict["monthly/out_sample_month"] = t +1 # 1 indexed, bc the first step is 1 month ahead

        for i, j in enumerate(dict_of_eval_dicts.keys()): # this is the same as the above but with the dict keys

            step = f"step{str(t+1).zfill(2)}"

            # get the scores
            y_score = mean_array[t,i,:,:].reshape(-1) # make it 1d  # nu 180x180 
            y_score_prob = mean_class_array[t,i,:,:].reshape(-1) # nu 180x180 

            # do not really know what to do with these yet.
            y_var = std_array[t,i,:,:].reshape(-1)  # nu 180x180  
            y_var_prob = std_class_array[t,i,:,:].reshape(-1)  # nu 180x180 

            # see this is the out of sample vol - fine for evaluation but not for forecasting
            # but also the place where you get the pgm.. 

            #if eval:
            y_true = out_of_sample_vol[:,t,i,:,:].reshape(-1)  # nu 180x180 . dim 0 is time     THE TRICK IS NOW TO USE A df -> vol and not out_of_sample_vol...
            y_true_binary = (y_true > 0) * 1

            # in theorty you could just use the metadata tensor to get pg and c id here
            pg_id = out_of_sample_meta_vol[:,t,0,:,:].reshape(-1)  # nu 180x180, dim 1 is time . dim 2 is feature. feature 0 is pg_id
            c_id = out_of_sample_meta_vol[:,t,4,:,:].reshape(-1)  # nu 180x180, dim 1 is time . dim 2 is feature. feature 4 is c_id
            month_id = out_of_sample_meta_vol[:,t,3,:,:].reshape(-1)  # nu 180x180, dim 1 is time . dim 2 is feature. feature 3 is month_id

            dict_of_outputs_dicts[j][step].y_true = y_true
            dict_of_outputs_dicts[j][step].y_true_binary = y_true_binary

            #else: # you need to make sure this works for forecasting
                # in theorty you could just use the metadata tensor to get pg and c id here
            pg_id = out_of_sample_meta_vol[:,t,0,:,:].reshape(-1)  # nu 180x180, dim 1 is time . dim 2 is feature. feature 0 is pg_id
            c_id = out_of_sample_meta_vol[:,t,4,:,:].reshape(-1)  # nu 180x180, dim 1 is time . dim 2 is feature. feature 4 is c_id
            month_id = out_of_sample_meta_vol[:,t,3,:,:].reshape(-1)  # nu 180x180, dim 1 is time . dim 2 is feature. feature 3 is month_id


            dict_of_outputs_dicts[j][step].y_score = y_score
            dict_of_outputs_dicts[j][step].y_score_prob = y_score_prob
            dict_of_outputs_dicts[j][step].y_var = y_var
            dict_of_outputs_dicts[j][step].y_var_prob = y_var_prob

            dict_of_outputs_dicts[j][step].pg_id = pg_id # in theory this should be in the right order
            dict_of_outputs_dicts[j][step].c_id = c_id # in theory this should be in the right order
            dict_of_outputs_dicts[j][step].step = t +1 # 1 indexed, bc the first step is 1 month ahead
            dict_of_outputs_dicts[j][step].month_id = month_id

            #if eval:   

            dict_of_eval_dicts[j][step].MSE = mean_squared_error(y_true, y_score)
            dict_of_eval_dicts[j][step].AP = average_precision_score(y_true_binary, y_score_prob)
            dict_of_eval_dicts[j][step].AUC = roc_auc_score(y_true_binary, y_score_prob)
            dict_of_eval_dicts[j][step].Brier = brier_score_loss(y_true_binary, y_score_prob)

            log_dict = generate_wandb_log_dict(log_dict, dict_of_eval_dicts, j, step)

        # if eval:
        log_dict_list.append(log_dict)
        wandb.log(log_dict)

    if not config.sweep:

        _ , _, PATH_GENERATED = setup_data_paths(PATH)

        # if the path does not exist, create it - maybe doable with Pathlib, but this is a well recognized way of doing it.
        #if not os.path.exists(PATH_GENERATED):
        #    os.makedirs(PATH_GENERATED)

        # Pathlib alternative 
        Path(PATH_GENERATED).mkdir(parents=True, exist_ok=True)

        # print for debugging
        print(f'PATH to generated data: {PATH_GENERATED}')

        # pickle the posterior dict, metric dict, and test vol
        # Should be time_steps and run_type in the name....

        posterior_dict = {'posterior_list' : posterior_list, 'posterior_list_class': posterior_list_class, 'out_of_sample_vol' : out_of_sample_vol}

        # You don't use this anymore.
        # metric_dict = {'out_sample_month_list' : out_sample_month_list, 'mse_list': mse_list,
        #                'ap_list' : ap_list, 'auc_list': auc_list, 'brier_list' : brier_list}

        # BUG FIX THIS
        df_sb_os_ns_output = output_to_df(dict_of_outputs_dicts)
        df_sb_os_ns_evaluation = evaluation_to_df(dict_of_eval_dicts)
        #df_sb_os_ns_eval = evaluation_to_df(dict_of_eval_dicts)

        # Note: we are using the model_time_stamp from the model artifact to denote the time stamp for the pkl files
        # This is to ensure that the pkl files are easily identifiable and associated with the correct model artifact
        # But it also means that running evaluation on the same model artifact multiple times will overwrite the pkl files
        # I think this is fine, but we should think about cases where we might want to evaluate the same model artifact multiple times - maybe for robustiness checks or something for publication. 

        with open(f'{PATH_GENERATED}/posterior_dict_{config.time_steps}_{config.run_type}_{config.model_time_stamp}.pkl', 'wb') as file:
            pickle.dump(posterior_dict, file)       

        # used to be made out of lists above. You don't do that now... 
        #with open(f'{PATH_GENERATED}/metric_dict_{config.time_steps}_{config.run_type}_{config.model_time_stamp}.pkl', 'wb') as file:
        #    pickle.dump(metric_dict, file)

        with open(f'{PATH_GENERATED}/df_sb_os_ns_output_{config.time_steps}_{config.run_type}_{config.model_time_stamp}.pkl', 'wb') as file: # make it numpy
            pickle.dump(df_sb_os_ns_output, file)

        with open(f'{PATH_GENERATED}/df_sb_os_ns_evaluation_{config.time_steps}_{config.run_type}_{config.model_time_stamp}.pkl', 'wb') as file:
            pickle.dump(df_sb_os_ns_evaluation, file)

        with open(f'{PATH_GENERATED}/test_vol_{config.time_steps}_{config.run_type}_{config.model_time_stamp}.pkl', 'wb') as file: # make it numpy
            pickle.dump(full_tensor.cpu().numpy(), file)

        with open(f'{PATH_GENERATED}/metadata_vol_{config.time_steps}_{config.run_type}_{config.model_time_stamp}.pkl', 'wb') as file:
            pickle.dump(metadata_tensor.cpu().numpy(), file)

        print('Posterior dict, (no metric dict?) but df and test vol pickled and dumped!')

    else:
        print('Running sweep. NO posterior dict, metric dict, or test vol pickled+dumped')

        # prolly just use Xialong's new function in eval for this. 
        #log_wandb_mean_metrics(config, mse_list, ap_list, auc_list, brier_list) # correct and reimplment this
    #log_wandb_mean_metrics(config, df_sb_os_ns_evaluation) # correct and reimplment this


def evaluate_model_artifact(config, device, views_vol, PATH_ARTIFACTS, artifact_name=None):
#def handle_evaluation(config, device, views_vol, PATH_ARTIFACTS, artifact_name=None):

    """
    Loads a model artifact and evaluates it given the respective trian and eval set within each data partition (Calibration, Testing).

    This function handles the loading of a model artifact either by using a specified artifact name
    or by selecting the latest model artifact based on the run type (default). It then evaluates the model's
    posterior distribution and prints the result.

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
    evaluate_posterior(model, views_vol, config, device)
    
    # done. 
    print('Done testing') 



# note:
# Going with the argparser, there is less of a clear reason to have to separate .py files for evaluation sweeps and single models. I think. Let me know if you disagree.
# naturally its a question of generalization and reusability, and i could see I had a lot of copy paste code between the two scripts.