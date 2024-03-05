import numpy as np
import pickle
import time
import sys
import os
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


# ------------------------- CHANGE TO A COMMON UTIL ---------------------------------
from pathlib import Path

def setup_project_paths():
    root_path = Path(__file__).resolve().parents[3]

    # Define common paths
    common_utils_path = root_path / "common_utils"
    common_configs_path = root_path / "common_configs"

    # Define model-specific paths
    model_path = Path(__file__).resolve().parents[1]
    configs_path = model_path / "configs"
    src_path = model_path / "src"
    utils_path = src_path / "utils"
    architectures_path = src_path / "architectures"

    paths_to_add = [common_utils_path, common_configs_path, configs_path, utils_path, architectures_path]

    for path in paths_to_add:
        path_str = str(path)
        if path.exists() and path_str not in sys.path:
            sys.path.insert(0, path_str)

# Call the function to setup the project paths
setup_project_paths()
# -----------------------------------------------------------------------------------


from utils import choose_model, choose_loss, choose_sheduler, get_train_tensors, get_test_tensor, apply_dropout, execute_freeze_h_option, get_log_dict, train_log, init_weights, get_data
from config_sweep import get_swep_config
from config_hyperparameters import get_hp_config


def test(model, test_tensor, time_steps, config, device): # should be called eval/validation

    """
    Function to test the model on the hold-out test set.
    The function takes the model, the test tensor, the number of time steps to predict, the config, and the device as input.
    The function returns **two lists of numpy arrays**. One list of the predicted magnitudes and one list of the predicted probabilities.
    Each array is of the shap **fx180x180**, where f is the number of features (currently 3 types of violence).
    """

    model.eval() # remove to allow dropout to do its thing as a poor mans ensamble. but you need a high dropout..
    model.apply(apply_dropout)

    # wait until you know if this work as usually
    pred_np_list = []
    pred_class_np_list = []

    h_tt = model.init_hTtime(hidden_channels = model.base, H = 180, W  = 180).float().to(device) # should infere the dim...
    seq_len = test_tensor.shape[1] # og nu køre eden bare helt til roden
    print(f'\t\t\t\t sequence length: {seq_len}', end= '\r')


    for i in range(seq_len-1): # need to get hidden state... You are predicting one step ahead so the -1

        if i < seq_len-1-time_steps: # take form the test set

            print(f'\t\t\t\t\t\t\t in sample. month: {i+1}', end= '\r')

            t0 = test_tensor[:, i, :, :, :].to(device) # THIS IS ALL YOU NEED TO PUT ON DEVICE!!!!!!!!!
            t1_pred, t1_pred_class, h_tt = model(t0, h_tt)

        else: # take the last t1_pred
            print(f'\t\t\t\t\t\t\t Out of sample. month: {i+1}', end= '\r')
            t0 = t1_pred.detach()

            t1_pred, t1_pred_class, h_tt = execute_freeze_h_option(config, model, t0, h_tt)

            t1_pred_class = torch.sigmoid(t1_pred_class) # there is no sigmoid in the model (the loss takes logits) so you need to do it here.
            pred_np_list.append(t1_pred.cpu().detach().numpy().squeeze()) # squeeze to remove the batch dim. So this is a list of 3x180x180 arrays
            pred_class_np_list.append(t1_pred_class.cpu().detach().numpy().squeeze()) # squeeze to remove the batch dim. So this is a list of 3x180x180 arrays

    return pred_np_list, pred_class_np_list



def sample_posterior(model, views_vol, config, device): 

    """
    Samples from the posterior distribution of Hydranet.

    Args:
    - model: HydraNet
    - views_vol (torch.Tensor): Input views data.
    - config: Configuration file
    - device: Device for computations.

    Returns:
    - tuple: (posterior_magnitudes, posterior_probabilities, out_of_sample_data)
    """

    print(f'Drawing {config.test_samples} posterior samples...')

    # Why do you put this test tensor on device here??!? 
    test_tensor = get_test_tensor(views_vol, config, device) # better cal thiis evel tensor
    out_of_sample_vol = test_tensor[:,-config.time_steps:,:,:,:].cpu().numpy() # From the test tensor get the out-of-sample time_steps. 

    posterior_list = []
    posterior_list_class = []

    for i in range(config.test_samples): # number of posterior samples to draw - just set config.test_samples, no? 

        # test_tensor is need on device here, but maybe just do it inside the test function? 
        pred_np_list, pred_class_np_list = test(model, test_tensor, config.time_steps, config, device) # Returns two lists of numpy arrays (shape 3/180/180). One list of the predicted magnitudes and one list of the predicted probabilities.
        posterior_list.append(pred_np_list)
        posterior_list_class.append(pred_class_np_list)

        #if i % 10 == 0: # print steps 10
        print(f'Posterior sample: {i}/{config.test_samples}', end = '\r')

    return posterior_list, posterior_list_class, out_of_sample_vol, test_tensor



def get_posterior(model, views_vol, config, device):

    """
    Function to get the posterior distribution of Hydranet.
    """

    posterior_list, posterior_list_class, out_of_sample_vol, test_tensor = sample_posterior(model, views_vol, config, device)

    # YOU ARE MISSING SOMETHING ABOUT FEATURES HERE WHICH IS WHY YOU REPORTED AP ON WandB IS BIASED DOWNWARDS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!RYRYRYRYERYERYR
    # Get mean and std
    mean_array = np.array(posterior_list).mean(axis = 0) # get mean for each month!
    std_array = np.array(posterior_list).std(axis = 0)

    mean_class_array = np.array(posterior_list_class).mean(axis = 0) # get mean for each month!
    std_class_array = np.array(posterior_list_class).std(axis = 0)

    out_sample_month_list = [] # only used for pickle...
    ap_list = []
    mse_list = []
    auc_list = []
    brier_list = []

    for i in range(mean_array.shape[0]): #  0 of mean array is the temporal dim

        y_score = mean_array[i].reshape(-1) # make it 1d  # nu 180x180
        y_score_prob = mean_class_array[i].reshape(-1) # nu 180x180

        # do not really know what to do with these yet.
        y_var = std_array[i].reshape(-1)  # nu 180x180
        y_var_prob = std_class_array[i].reshape(-1)  # nu 180x180

        y_true = out_of_sample_vol[:,i].reshape(-1)  # nu 180x180 . dim 0 is time
        y_true_binary = (y_true > 0) * 1

        mse = mean_squared_error(y_true, y_score)  
        ap = average_precision_score(y_true_binary, y_score_prob)
        auc = roc_auc_score(y_true_binary, y_score_prob)
        brier = brier_score_loss(y_true_binary, y_score_prob)

        log_dict = get_log_dict(i, mean_array, mean_class_array, std_array, std_class_array, out_of_sample_vol, config)# so at least it gets reported sep.

        wandb.log(log_dict)

        out_sample_month_list.append(i) # only used for pickle...
        mse_list.append(mse)
        ap_list.append(ap) # add to list.
        auc_list.append(auc)
        brier_list.append(brier)

    # DUMP
        
    # computerome dump location
    #dump_location = '/home/projects/ku_00017/data/generated/conflictNet/' # should be in config

    # fimbulthul dump location
    dump_location = config.path_generated_data #'/home/simmaa/HydraNet_001/data/generated/' # should be in config <---------------------------------------------------------------------------------------------------

        
    posterior_dict = {'posterior_list' : posterior_list, 'posterior_list_class': posterior_list_class, 'out_of_sample_vol' : out_of_sample_vol}
        
    metric_dict = {'out_sample_month_list' : out_sample_month_list, 'mse_list': mse_list,
                    'ap_list' : ap_list, 'auc_list': auc_list, 'brier_list' : brier_list}

    with open(f'{dump_location}posterior_dict_{config.time_steps}_{config.model_type}.pkl', 'wb') as file:
        pickle.dump(posterior_dict, file)       

    with open(f'{dump_location}metric_dict_{config.time_steps}_{config.model_type}.pkl', 'wb') as file:
        pickle.dump(metric_dict, file)

    with open(f'{dump_location}test_vol_{config.time_steps}_{config.model_type}.pkl', 'wb') as file: # make it numpy
        pickle.dump(test_tensor.cpu().numpy(), file)

    print('Posterior dict, metric dict and test vol pickled and dumped!')

    wandb.log({f"{config.time_steps}month_mean_squared_error": np.mean(mse_list)})
    wandb.log({f"{config.time_steps}month_average_precision_score": np.mean(ap_list)})
    wandb.log({f"{config.time_steps}month_roc_auc_score": np.mean(auc_list)})
    wandb.log({f"{config.time_steps}month_brier_score_loss":np.mean(brier_list)})


def model_pipeline(config = None, project = None):

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)

    # tell wandb to get started
    with wandb.init(project=project, entity="nornir", config=config): # project and config ignored when runnig a sweep

        wandb.define_metric("monthly/out_sample_month")
        wandb.define_metric("monthly/*", step_metric="monthly/out_sample_month")

        # access all HPs through wandb.config, so logging matches execution!
        config = wandb.config

        views_vol = get_data(config)

        # computerome artifacts path
        #artifacts_path = f"/home/projects/ku_00017/people/simpol/scripts/conflictNet/artifacts"
        
        # fimbulthul artifacts path
        artifacts_path = config.path_artifacts # f"/home/simmaa/HydraNet_001/artifacts" # should be in config <---------------------------------------------------------------------------------------------------

        model = torch.load(f"{artifacts_path}/calibration_model.pt") # you rpolly need configs for both train and test...

        get_posterior(model, views_vol, config, device) # actually since you give config now you do not need: time_steps, run_type, is_sweep,
        print('Done testing')

        return(model)


if __name__ == "__main__":

    wandb.login()

    time_steps_dict = {'a':12,
                       'b':24,
                       'c':36,
                       'd':48,}

    time_steps = time_steps_dict[input('a) 12 months\nb) 24 months\nc) 36 months\nd) 48 months\nNote: 48 is the current VIEWS standard.\n')]

    model_type_dict = {'a' : 'calibration', 'b' : 'testing'}
    model_type = model_type_dict[input("a) Calibration\nb) Testing\n")]
    print(f'Run type: {model_type}\n')

    project = f"imp_new_structure_{model_type}" # temp.

    hyperparameters = get_hp_config()

    hyperparameters['time_steps'] = time_steps
    hyperparameters['model_type'] = model_type
    hyperparameters['sweep'] = False

    start_t = time.time()

    model = model_pipeline(config = hyperparameters, project = project)

    end_t = time.time()
    minutes = (end_t - start_t)/60
    print(f'Done. Runtime: {minutes:.3f} minutes')


