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

def training():
    model = config.model
    modelstore = storage.Storage()
    print('Calibration partition')
    model['Algorithm_text'] = str(config.model['algorithm'])
    
    model['RunResult_calib'] = RunResult.retrain_or_retrieve(
        retrain=bool(config.common_config['force_retrain']),
        store=modelstore,
        partitioner=DataPartitioner({"calib": config.common_config['calib_partitioner_dict']}),
        stepshifted_models=StepshiftedModels(
            config.model['algorithm'], config.common_config['steps'], model['depvar']),
        dataset=get_querysets(),
        queryset_name=model['queryset'],
        partition_name="calib",
        timespan_name="train",
        storage_name=model['modelname'] + '_calib',
        author_name="MDnD",
    )

    model['predstore_calib'] = config.common_config['level'] + '_' + model['modelname'] + '_calib'
    if config.common_config['force_rewrite']:
        print(model['predstore_calib'], ', run',
              config.common_config['run_id'], 'force_rewrite=True, predicting')
        predictions_calib = model['RunResult_calib'].run.predict(
            "calib", "predict", model['RunResult_calib'].data)

        predictions_calib.to_parquet(model['predstore_calib']+'.parquet')
        if config.common_config['store_remote']:
            predictions_calib.forecasts.set_run(config.common_config['run_id'])
            predictions_calib.forecasts.to_store(
                name=model['predstore_calib'], overwrite=True)
        print('Predictions:', predictions_calib)

    else:
        print('Trying to retrieve predictions')
        try:
            predictions_calib = pd.DataFrame.forecasts.read_store(
                run=config.common_config['run_id'], name=model['predstore_calib'])
        except KeyError:
            print(model['predstore_calib'], ', run',
                  config.common_config['run_id'], 'does not exist, predicting')
            predictions_calib = model['RunResult_calib'].run.predict(
                "calib", "predict", model['RunResult_calib'].data)
            predictions_calib.forecasts.set_run(config.common_config['run_id'])
            predictions_calib.forecasts.to_store(name=model['predstore_calib'])
        
        print('Predictions retrieved:', predictions_calib)
    print('Calibration partition done')