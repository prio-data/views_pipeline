from pathlib import Path
import pandas as pd
import wandb
from sklearn.metrics import mean_squared_error

PATH = Path(__file__)  
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)

from utils import get_standardized_df
from utils_wandb import log_wandb_log_dict
from utils_evaluation_metrics import generate_metric_dict


def evaluate_sweep(config, stepshift_model):
    PATH_RAW, _, _ = setup_data_paths(PATH)
    run_type = config['run_type']
    steps = config['steps']

    df_viewser = pd.read_pickle(PATH_RAW / f"{run_type}_viewser_df.pkl")
    df = stepshift_model.predict(run_type, df_viewser)
    df = get_standardized_df(df, config)

    # Temporarily keep this because the metric to minimize is MSE
    pred_cols = [f"step_pred_{str(i)}" for i in steps]
    df["mse"] = df.apply(lambda row: mean_squared_error([row[config['depvar']]] * 36,
                                                        [row[col] for col in pred_cols]), axis=1)

    wandb.log({'MSE': df['mse'].mean()})

    evaluation, df_evaluation = generate_metric_dict(df, config)
    log_wandb_log_dict(config, evaluation)
