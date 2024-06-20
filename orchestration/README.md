## Pipeline Orchestration/Execution
> [!CAUTION]
> We are still in the process of migrating our models to this repository. Until then, the monthly VIEWS run is conducted with the [viewsforecasting repository](https://github.com/prio-data/viewsforecasting). The following information is not yet operational.

For the monthly run, ensure that the latest input data has been ingested into the VIEWS database prior.

This pipeline uses two tools for logging relevant information, in order to enhance transparency and collaboration. For the individual models, we use Weights & Biases (W&B / wandb) as a centralized platform for logging and monitoring model outputs, system metrics, and experiment metadata. This is especially relevant when tuning hyperparameters, for which we conduct so-called sweeps. For the entire pipeline, we use Prefect to log as a "flow run". 

Follow the steps below to execute / orchestrate an entire run of the VIEWS pipeline.

1. **Clone the Repository:**

   ```bash
   git clone <https://github.com/prio-data/views_pipeline>

2. **Make sure Prefect is set up**

In your viewser environment, make sure prefect is pip installed.
You can check with ```pip show prefect```

To login to your account write:
```bash
prefect cloud login
```
and subsequently login online.

3. **Make desired changes to common configs and utils**
For changing the months in data partitions, go to [common_utils/set_partition.py](https://github.com/prio-data/views_pipeline/blob/main/common_utils/set_partition.py).

4. **Run the Orchestration Script:**
Execute the Prefect flow script to run all models in this repository.
```bash
python orchestration.py
```
The script executes every main.py file in every model and ensemble folder. For every model, you will be prompted in the terminal to:
    a) Do sweep 
    b) Do one run and pickle results
To conduct the monthly run, type `b` and enter.

The progress of the pipeline execution will be logged online on Prefect.

5. **Monitor Pipeline Execution:**
Once the pipeline is initiated, you can monitor its execution using the Prefect UI dashboard or CLI. You can copy the link given in the terminal, go to the website, or use the following command to launch the Prefect UI:
```bash
prefect server start
```

Once models are run, you can also check their logs and visualizations in [Weights & Biases](https://wandb.ai/views_pipeline).