import os
import wandb
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")
os.environ['WANDB_SILENT'] = 'true'

from lightgbm import LGBMRegressor

from stepshift.views import StepshiftedModels
from views_runs import storage
from views_partitioning.data_partitioner import DataPartitioner
from views_runs.run_result import RunResult
from views_forecasts.extensions import *

from ..dataloaders.get_data import *


def train(common_config, para_config):
    modelstore = storage.Storage()
    suffix = ""
    if common_config['sweep']:
        for key, value in para_config.items():
            suffix += f"_{key}_{value}"
        
    model = globals()[common_config['algorithm']](**para_config)
    dataset = pd.read_parquet(f"{Path(__file__).parent.parent.parent}/data/raw/raw.parquet")

    # Training
    common_config["RunResult"] = RunResult.retrain_or_retrieve(
        retrain=common_config["force_retrain"],
        store=modelstore,
        partitioner=DataPartitioner({"future": common_config["future_partitioner_dict"]}),
        stepshifted_models=StepshiftedModels(model, common_config["steps"], common_config['depvar']),
        dataset=dataset,
        queryset_name=common_config['queryset'],
        partition_name="future",
        timespan_name="train",
        storage_name=common_config['name'] + suffix,
        author_name="xiaolong",
    )
    common_config["storage_name"] = common_config['name'] + suffix



    

    



    

    
    
    
    


