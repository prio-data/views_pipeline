## Error Logging and Alerts for Model Training

| ADR Info            | Details           |
|---------------------|-------------------|
| Subject             | Error Logging and Alerts for Model Training  |
| ADR Number          | 019   |
| Status              | Proposed |
| Author              | Xiaolong |
| Date                | 29.10.2024 |

## Context
To ensure clarity and efficiency in monitoring the model training pipeline, it’s essential to adopt structured logging and alerting practices. The current pipeline generates logs during training execution, but these logs need to be more informative and concise. Therefore, we need to define standards around what to log, where to log, and how to log to enhance the readability and utility of logs.

## Decision


### Logging Content
The followings

### Logging Format
`.log` files are used to save the loggings. 

### Logging Levels
The logging levels we set in this project are `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`. The default level is `INFO`, meaning that only levels above will be logged. Below are specific examples for each level that is logged:

#### 1. INFO
```
logger.info(f"Training model {config['name']}...")
```
At this level logging is used to confirm that things are working as expected.

#### 2. WARNING
```
logger.warning(f"DataFrame contains non-np.float64 numeric columns. Converting the following columns: {', '.join(non_float64_cols)}")
```
At this level logging is used to indicate that something not conforming to the standards happened, but it is still working as expected.

#### 3. ERROR
```
logger.error(f"Raw data for model {model_name} was not fetched in the current month. Exiting.")
```
At this level logging is used to show an error that prevents the preceeding of the pipeline.

#### 4. CRITICAL
Currently `CRITICAL` hasn't been used, but usually it means the program itself may be unable to continue running.

### Storage and Distribution:
The logs are generated at the terminal, in the `.log` file, and on W&B to ensure both internal accessibility and external sharing. Logs on W&B are permanently kept, while the `.log` files are kept until reaching the preset maximum amount .

### Integration with Alerting and Notification

## Consequences

**Positive Effects:**
- Informative logs provide detailed insights into model performance, resource utilization, and pipeline behavior.
- Automated alerts for critical errors or unusual behavior reduce manual monitoring efforts.
- Clear and informative logs create a common understanding of pipeline operations.

**Negative Effects:**
- Designing and setting up standardized logging and alerting practices can be complex, especially when integrating with external logging and alerting tools.
- Logs may contain sensitive information (e.g., model data, configurations) that could pose privacy or security risks if not managed properly.

## Rationale
*Explain the reasoning behind the decision, including any specific advantages that influenced the choice. This section should reflect the factors mentioned in the context.*

### Considerations
*List any considerations that were part of the decision-making process, such as potential risks, dependency issues, or impacts on existing systems.*

## Additional Notes
*Include any additional information that might be relevant to the decision, such as implications for development workflows, future maintenance, or related decisions.*

## Feedback and Suggestions
Feedbacks and suggestions are welcomed.
