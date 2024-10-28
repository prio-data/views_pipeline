from pathlib import Path
import pickle
import logging

logger = logging.getLogger(__name__)


def save_model_outputs(df_evaluation, df_output, PATH_GENERATED, config):
    Path(PATH_GENERATED).mkdir(parents=True, exist_ok=True)

    # Save the DataFrame of model outputs
    outputs_path = f"{PATH_GENERATED}/output_{config['steps'][-1]}_{config['run_type']}_{config['timestamp']}.pkl"
    with open(outputs_path, 'wb') as file:
        pickle.dump(df_output, file)
    logger.info(f"Model outputs saved at: {outputs_path}")

    # Save the DataFrame of evaluation metrics
    evaluation_path = f"{PATH_GENERATED}/evaluation_{config['steps'][-1]}_{config['run_type']}_{config['timestamp']}.pkl"
    with open(evaluation_path, 'wb') as file:
        pickle.dump(df_evaluation, file)
    logger.info(f"Evaluation metrics saved at: {evaluation_path}")


def save_predictions(df_predictions, PATH_GENERATED, config):
    Path(PATH_GENERATED).mkdir(parents=True, exist_ok=True)

    predictions_path = f"{PATH_GENERATED}/predictions_{config['steps'][-1]}_{config['run_type']}_{config['timestamp']}.pkl"
    with open(predictions_path, 'wb') as file:
        pickle.dump(df_predictions, file)
    logger.info(f"Predictions saved at: {predictions_path}")
