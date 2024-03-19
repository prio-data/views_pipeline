import pandas as pd
from pathlib import Path

from views_runs import Storage, StepshiftedModels
from views_partitioning.data_partitioner import DataPartitioner
from viewser import Queryset, Column
from views_runs import operations
from views_runs.run_result import RunResult
from views_runs import storage
from views_runs.storage import store, retrieve, fetch_metadata
from viewser.operations import fetch
import views_runs
from views_partitioning import data_partitioner, legacy
from stepshift import views


from ...configs import config
from ..dataloaders.queryset import get_querysets


def forecast():
    model = config.model
    modelstore = storage.Storage()
    print('Test partition')
    model['Algorithm_text'] = str(config.model['algorithm'])

    model['RunResult_test'] = RunResult.retrain_or_retrieve(
        retrain=bool(config.common_config['force_retrain']),
        store=modelstore,
        partitioner=DataPartitioner(
            {"test": config.common_config['future_partitioner_dict']}),  # changed from calib to future
        stepshifted_models=StepshiftedModels(
            config.model['algorithm'], config.common_config['steps'], model['depvar']),
        dataset=get_querysets(),
        queryset_name=model['queryset'],
        partition_name="test",  # changed from calib to test    
        timespan_name="train",  # changed from train to train
        storage_name=model['modelname'] + '_forecast',  # changed from calib to forecast
        author_name="MDnD",
    )

    predictions_test = model['RunResult_test'].run.predict(
            "test", "predict", model['RunResult_test'].data)
    
    predictions_test.to_parquet(
        f"{Path(__file__).parent.parent.parent}/data/generated/{model['modelname']}_true_forecasts.parquet")

        
    print('Predictions:', predictions_test)