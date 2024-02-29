from sklearn.ensemble import RandomForestClassifier

from stepshift.views import StepshiftedModels
from views_runs import DataPartitioner, ViewsRun

from configs.config_common import common_config
from configs.config_hyperparameters import hp_config

def train_model(common_config, hp_config, data): #not sure about data

    #TBD: Dataloader store?

    # Extract common configurations  >> TBD: link to common_config
    calib_partitioner_dict = common_config["calib_partitioner_dict"]
    future_partitioner_dict = common_config["future_partitioner_dict"]
    steps = common_config["steps"]
    target = common_config["target"]

    # Extract hyperparameters >> TBD: link to hp_config
    learning_rate = hp_config["learning_rate"]
    n_estimators = hp_config["n_estimators"]
    n_jobs = hp_config["n_jobs"]

    # Create data partitioners
    calib_partition = DataPartitioner({'calib': calib_partitioner_dict})
    future_partition = DataPartitioner({'future': future_partitioner_dict})

    # Define base model and stepshifter
    base_model = RandomForestClassifier(n_estimators=n_estimators, n_jobs=n_jobs)
    stepshifter_def = StepshiftedModels(base_model, steps, target)

    # Fitting for calibration run
    stepshifter_model_calib = ViewsRun(calib_partition, stepshifter_def)
    stepshifter_model_calib.fit('calib', 'train', data)

    # Fitting for future run
    stepshifter_model_future = ViewsRun(future_partition, stepshifter_def)
    stepshifter_model_future.fit('future', 'train', data)

if __name__ == "__main__":
    # Load your data
    # data = Load your data here

    # Call the train_model function
    train_model(common_config, hp_config, data)