import sys
from datetime import datetime
import pandas as pd
from pathlib import Path
import pickle

PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths, setup_data_paths, setup_artifacts_paths, setup_root_paths
setup_project_paths(PATH)

from set_partition import get_partitioner_dict
from utils import get_standardized_df, get_aggregated_df
from utils_artifacts import get_latest_model_artifact


def forecast_ensemble(config):
    run_type = config['run_type']
    PATH_MODELS = setup_root_paths(PATH) / "models"
    _, _, PATH_GENERATED_E = setup_data_paths(PATH)
    dfs = []
    timestamp = ''

    for model in config["models"]:
        print(f"Single model {model}...")

        PATH_MODEL = PATH_MODELS / model
        PATH_RAW, _, PATH_GENERATED = setup_data_paths(PATH_MODEL)
        PATH_ARTIFACTS = setup_artifacts_paths(PATH_MODEL)
        PATH_ARTIFACT = get_latest_model_artifact(PATH_ARTIFACTS, config.run_type)

        ts = PATH_ARTIFACT.stem[-15:]
        timestamp += model + ts + '_'

        pkl_path = f'{PATH_GENERATED}/predictions_{config.steps[-1]}_{config.run_type}_{ts}.pkl'
        if Path(pkl_path).exists():
            with open(pkl_path, 'rb') as file:
                df = pickle.load(file)
        else:
            df_viewser = pd.read_pickle(PATH_RAW / f"{run_type}_viewser_df.pkl")
            try:
                stepshift_model = pd.read_pickle(PATH_ARTIFACT)
            except:
                raise FileNotFoundError(f"Model artifact not found at {PATH_ARTIFACT}")

            partition = get_partitioner_dict(run_type)['predict']
            df = stepshift_model.future_point_predict(partition[0]-1, df_viewser, keep_specific=True)
            df = get_standardized_df(df, config)
        dfs.append(df)
    df_prediction = get_aggregated_df(dfs, config["aggregation"])

    # I don't think timestamp is useful here.
    # Timestamp of single models is more important but how should we register them in ensemble config?
    config["timestamp"] = timestamp[:-1]
    predictions_path = f'{PATH_GENERATED_E}/predictions_{config.steps[-1]}_{config.run_type}_{config.timestamp}.pkl'
    with open(predictions_path, 'wb') as file:
        pickle.dump(df_prediction, file)
