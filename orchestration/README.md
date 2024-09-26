## Pipeline Orchestration & Execution
Follow the steps below to execute / orchestrate an entire run of the VIEWS pipeline.

### 1. Clone the Repository:

```bash
git clone <https://github.com/prio-data/views_pipeline>
cd orchestration
```
### 2. Make sure Prefect is set up
In your viewser environment, make sure prefect is pip installed. You can check with ```pip show prefect```

To login to your account write:
```bash
prefect cloud login
```
and subsequently login online.

### 3. Make desired changes to common configs and utils

For changing the months in data partitions, go to [common_configs/set_partition.py](../common_configs/set_partition.py).

### 4. Run the orchestration script
The script executes every main.py file in every model and ensemble folder. Currently, it only allows you to do **either single 
models or ensemble models**, which is decided by whether the argument '--aggregation' is provided. 

If you want to train and evaluate all the single models, you can run the following command:
```bash
python orchestration.py --run_type <run_type> --train --evaluate 
```
If you want to train and evaluate all the ensemble models, you can run the following command:
```bash
python orchestration.py --run_type <run_type> --train --evaluate --ensemble 
```

The progress of the pipeline execution will be logged online on Prefect.

More arguments can be found in the [common_utils/utils_cli_parser.py](../common_utils/utils_cli_parser.py)

### 5. Monitor pipeline execution
Once the pipeline is initiated, you can monitor its execution using the Prefect UI dashboard or CLI. You can copy the 
link given in the terminal, go to the website, or use the following command to launch the Prefect UI:
```bash
prefect server start
```

Once models are run, you can also check their logs and visualizations in [Weights & Biases](https://wandb.ai/views_pipeline).