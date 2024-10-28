import pickle
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def save_model_outputs(df_evaluation, df_output, path_generated, config):
    Path(path_generated).mkdir(parents=True, exist_ok=True)

    # Save the DataFrame of model outputs
    outputs_path = f'{path_generated}/output_{config["steps"][-1]}_{config["run_type"]}_{config["timestamp"]}.pkl'
    with open(outputs_path, "wb") as file:
        pickle.dump(df_output, file)
    logger.info(f"Model outputs saved at: {outputs_path}")

    # Save the DataFrame of evaluation metrics
    evaluation_path = f'{path_generated}/evaluation_{config["steps"][-1]}_{config["run_type"]}_{config["timestamp"]}.pkl'
    with open(evaluation_path, "wb") as file:
        pickle.dump(df_evaluation, file)
    logger.info(f"Evaluation metrics saved at: {evaluation_path}")


def save_predictions(df_predictions, path_generated, config):
    Path(path_generated).mkdir(parents=True, exist_ok=True)

    predictions_path = f'{path_generated}/predictions_{config["steps"][-1]}_{config["run_type"]}_{config["timestamp"]}.pkl'
    with open(predictions_path, "wb") as file:
        pickle.dump(df_predictions, file)
    logger.info(f"Predictions saved at: {predictions_path}")