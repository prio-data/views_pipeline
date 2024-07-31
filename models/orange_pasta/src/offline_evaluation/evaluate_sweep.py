from pathlib import Path
import pandas as pd
import wandb
from sklearn.metrics import mean_squared_error

PATH = Path(__file__)  
from set_path import setup_project_paths, setup_data_paths
setup_project_paths(PATH)

from utils import get_standardized_df
from utils_wandb import generate_wandb_log_dict
from utils_evaluation_metrics import generate_metric_dict


def evaluate_sweep(config, stepshift_model):
    PATH_RAW, _, _ = setup_data_paths(PATH)

    dataset = pd.read_parquet(PATH_RAW / f'raw_{config.run_type}.parquet')

    df = stepshift_model.predict(dataset)
    df = get_standardized_df(df, config.run_type)

    # Temporarily keep this because the metric to minimize is MSE
    pred_cols = [f"step_pred_{str(i)}" for i in config.steps]
    df["mse"] = df.apply(lambda row: mean_squared_error([row[config["depvar"]]] * 36,
                                                        [row[col] for col in pred_cols]), axis=1)

    wandb.log({'MSE': df['mse'].mean()})

    evaluation, df_evaluation = generate_metric_dict(df, config)
    for t in config.steps:
        log_dict = {}
        log_dict["monthly/out_sample_month"] = t
        step = f"step{str(t).zfill(2)}"
        log_dict = generate_wandb_log_dict(log_dict, evaluation, step)
        wandb.log(log_dict)