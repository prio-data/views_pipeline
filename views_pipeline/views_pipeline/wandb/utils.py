import wandb

def add_wandb_monthly_metrics():
    """
    Defines the WandB metrics for monthly evaluation.

    This function sets up the metrics for logging monthly evaluation metrics in WandB.
    It defines a step metric called "monthly/out_sample_month" and specifies that any
    metric under the "monthly" namespace will use "monthly/out_sample_month" as its step metric.

    Usage:
        This function should be called at the start of a WandB run to configure
        how metrics are tracked over time steps.

    Example:
        >>> wandb.init(project="example_project")
        >>> add_wandb_monthly_metrics()
        >>> wandb.log({"monthly/mean_squared_error": 0.02, "monthly/out_sample_month": 1})

    Notes:
        - The step metric "monthly/out_sample_month" will be used to log metrics for each time  (i.e. forecasted month).
        - Any metric prefixed with "monthly/" will follow the "monthly/out_sample_month" step metric.

    See Also:
        - `wandb.define_metric`: WandB API for defining metrics and their step relationships.
    """

    # Define "new" monthly metrics for WandB logging
    wandb.define_metric("monthly/out_sample_month")
    wandb.define_metric("monthly/*", step_metric="monthly/out_sample_month")


def generate_wandb_log_dict(log_dict, dict_of_eval_dicts, step):
    """
    Adds evaluation metrics to a WandB log dictionary for a specific time step (i.e. forcasted month).

    This function updates the provided log dictionary with evaluation metrics from
    a specified feature and step, formatted for WandB logging. It appends the metrics
    to the log dictionary using the "monthly/{metric_name}" format.

    Args:
        log_dict (dict): The log dictionary to be updated with new metrics.
        dict_of_eval_dicts (Dict[str, Dict[str, EvaluationMetrics]]): A dictionary of evaluation metrics,
            where the keys are feature identifiers and the values are dictionaries with time steps as keys
            and `EvaluationMetrics` instances as values.
        step (str): The specific time step (month forecasted) for which metrics are logged (e.g., 'step01').

    Returns:
        dict: The updated log dictionary with the evaluation metrics for the specified feature and step.

    Example:
        >>> log_dict = {}
        >>> dict_of_eval_dicts = {
        ...     'step01': EvaluationMetrics(MSE=0.1, AP=0.2, AUC=0.3, Brier=0.4),
        ...     'step02': EvaluationMetrics(MSE=0.2, AP=0.3, AUC=0.4, Brier=0.5),
                ...
        ... }
        >>> log_dict = generate_wandb_log_dict(log_dict, dict_of_eval_dicts, 'step01')
        >>> print(log_dict)
        {
            'monthly/MSE': 0.1,
            'monthly/AP': 0.2,
            'monthly/AUC': 0.3,
            'monthly/Brier': 0.4
        }

    Notes:
        - Only non-None values from the `EvaluationMetrics` instance are added to the log dictionary.
        - The metrics are formatted with the "monthly/{metric_name}" naming convention for WandB logging.

    See Also:
        - `wandb.log`: WandB API for logging metrics.
    """

    for key, value in dict_of_eval_dicts[step].items():
        if value is not None:
            log_dict[f"monthly/{key}"] = value

    return log_dict


def log_wandb_log_dict(config, evaluation):
    for t in config["steps"]:
        log_dict = {}
        log_dict["monthly/out_sample_month"] = t
        step = f"step{str(t).zfill(2)}"
        log_dict = generate_wandb_log_dict(log_dict, evaluation, step)
        wandb.log(log_dict)
