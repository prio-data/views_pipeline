import sys
import pandas as pd
from pathlib import Path
import pickle

PATH = Path(__file__)
sys.path.insert(0, str(Path(
    *[i for i in PATH.parts[:PATH.parts.index("views_pipeline") + 1]]) / "common_utils"))  # PATH_COMMON_UTILS
from set_path import setup_project_paths, setup_data_paths, setup_artifacts_paths
setup_project_paths(PATH)

from set_partition import get_partitioner_dict
from utils import get_partition_data, get_standardized_df
from utils_artifacts import get_latest_model_artifact


def forecast_model_artifact(config, artifact_name):
    PATH_RAW, _, PATH_GENERATED = setup_data_paths(PATH)
    PATH_ARTIFACTS = setup_artifacts_paths(PATH)
    run_type = config['run_type']

    # if an artifact name is provided through the CLI, use it.
    # Otherwise, get the latest model artifact based on the run type
    if artifact_name:
        print(f"Using (non-default) artifact: {artifact_name}")

        if not artifact_name.endswith('.pkl'):
            artifact_name += '.pkl'
        PATH_ARTIFACT = PATH_ARTIFACTS / artifact_name
    else:
        # use the latest model artifact based on the run type
        print(f"Using latest (default) run type ({run_type}) specific artifact")
        PATH_ARTIFACT = get_latest_model_artifact(PATH_ARTIFACTS, run_type)

    config["timestamp"] = PATH_ARTIFACT.stem[-15:]

    try:
        stepshift_model = pd.read_pickle(PATH_ARTIFACT)
    except:
        raise FileNotFoundError(f"Model artifact not found at {PATH_ARTIFACT}")

    df_predictions = stepshift_model.predict(run_type)
    df_predictions = get_standardized_df(df_predictions, config)
    
    predictions_path = f"{PATH_GENERATED}/predictions_{config['steps'][-1]}_{run_type}_{config['timestamp']}.pkl"
    with open(predictions_path, 'wb') as file:
        pickle.dump(df_predictions, file)

