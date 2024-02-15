import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error


def evaluate_model(config):
    print('Evaluating...')
    steps = config['steps']
    stepcols = [config['depvar']]
    for step in steps:
        stepcols.append('step_pred_' + str(step))

    df = pd.DataFrame.forecasts.read_store(name=config["storage_name"]).replace([np.inf, -np.inf], 0)[stepcols]

    pred_cols = [f'step_pred_{str(i)}' for i in steps]
    df['mse'] = df.apply(lambda row: mean_squared_error([row['ged_sb_dep']] * 36,
                                                        [row[col] for col in pred_cols]), axis=1)
    
    print(df['mse'].mean())