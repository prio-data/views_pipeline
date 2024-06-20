import numpy as np
from pathlib import Path
import pickle

def split_hurdle_parameters(parameters_dict):
    """
    Split the parameters dictionary into two separate dictionaries, one for the
    classification model and one for the regression model. 
    """

    cls_dict = {}
    reg_dict = {}
    
    for key, value in parameters_dict.items():
        if key.startswith('cls_'):
            cls_key = key.replace('cls_', '')
            cls_dict[cls_key] = value
        elif key.startswith('reg_'):
            reg_key = key.replace('reg_', '')
            reg_dict[reg_key] = value
            
    return cls_dict, reg_dict


def ensure_float64(df):
    """
    Check if the DataFrame only contains np.float64 types. If not, raise a warning
    and convert the DataFrame to use np.float64 for all its numeric columns.
    """
    
    non_float64_cols = df.select_dtypes(include=['number']).columns[df.select_dtypes(include=['number']).dtypes != np.float64]

    if len(non_float64_cols) > 0:
        print(f"Warning: DataFrame contains non-np.float64 numeric columns. Converting the following columns: {', '.join(non_float64_cols)}")

        for col in non_float64_cols:
            df[col] = df[col].astype(np.float64)

    return df


def get_parameters(config):
    '''
    Get the parameters from the config file.
    If not sweep, then get directly from the config file, otherwise have to remove some parameters.
    '''

    if config["sweep"]:
        keys_to_remove = ["algorithm", "depvar", "steps", "sweep", "run_type", "model_cls", "model_reg"]
        parameters = {k: v for k, v in config.items() if k not in keys_to_remove}
    else:
        parameters = config["parameters"]

    return parameters


def save_model_outputs(df_evaluation, df_output, PATH_GENERATED, config):
    Path(PATH_GENERATED).mkdir(parents=True, exist_ok=True)
    print(f'PATH to generated data: {PATH_GENERATED}')

    # Save the DataFrame of model outputs
    outputs_path = f'{PATH_GENERATED}/df_output_{config.steps[-1]}_{config.run_type}_{config.timestamp}.pkl'
    with open(outputs_path, 'wb') as file:
        pickle.dump(df_output, file)

    # Save the DataFrame of evaluation metrics
    evaluation_path = f'{PATH_GENERATED}/df_evaluation_{config.steps[-1]}_{config.run_type}_{config.timestamp}.pkl'
    with open(evaluation_path, 'wb') as file:
        pickle.dump(df_evaluation, file)



