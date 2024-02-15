import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_squared_error
from ...configs import wandb_config
from ..utils.utils import wandb_log
import wandb
def evaluate_mse() -> float:
    data = pd.read_parquet(
        f"{Path(__file__).parent.parent.parent}/data/generated/forecasts.parquet")
    mse_mean = 0
    for i in range(1, 37):
        mse_mean = mse_mean + mean_squared_error(data['ln_ged_sb_dep'], data[f'step_pred_{i}'])
    print('The MSE is ', mse_mean/36)
    
    #project = wandb_config.project_config['project']
    #entity=wandb_config.project_config['entity']
    
    #wandb_log(project, entity, mse_mean/36, 'mse_mean_36_months')
    wandb.log({'Mean MSE 36 months': mse_mean/36})
    
    return mse_mean/36


