# Log Files and Real-Time Alerts

| ADR Info            | Details                   |
|---------------------|---------------------------|
| Subject             | Log files and real-time alerts |
| ADR Number          | 020                       |
| Status              | Proposed                  |
| Author              | Marina                    |
| Date                | 28.10.2024                |


## Context
In order to have a more effective overview of the orchestration in the pipeline, there is a need for better handling of log files and implementing real-time alerts which would allow for timely and relevant error handling for critical issues. 


## Decision
To implement a real-time alert and notification system which will distribute alerts through specific channels (eg. Slack, email, W&B, Prefect), targeted at particular audiences (eg. Infrastructure, MD&D, individual) depending on the type of alert being handled. 


### Overview

Alert channels: Slack, email, Prefect and Weights&Biases

Logging levels: INFO, WARNING, ERROR, CRITICAL

Audience: MD&D, Infrastructure, Outreach, monthly-run responsible 

| Channel | Threshold        | Alert Type                         | Audience                  |
|---------|-------------------|------------------------------------|---------------------------|
| Slack   | ERROR, CRITICAL   | Real-Time, Short Summary + Link to Full Log | MD&D, Infrastructure      |
| Email   | ERROR, CRITICAL   | Real-Time, Expanded Summary       | MD&D, Infrastructure      |
| Prefect | ALL               | Real-Time, Workflow Status        | MD&D, Infrastructure, Outreach |
| W&B     | ALL               | Performance Metrics               | MD&D, Infrastructure, Outreach |


For alert prioritization, "critical" and "non-critical" alerts are separated, with critical alerts stemming from logging levels ERROR and CRITICAL. 


## Consequences

**Positive Effects:**
- Real-time alerts allow for timely handling of errors which may be critical 
- Alerts can reach their target audiences immediately which limits time and makes information flows more direct and effective 
- Having real-time alerts is useful in generating a record of (reoccuring) issues in the pipeline 
- Increased transparency


**Negative Effects:**
- Alerts must be set up in a way to be concise and informative in order to be useful, with carefully chosen levels of detail to avoid "alert fatigue"
- The audience for each type of alert must be carefully selected in order for alerts to stay relevant 
- Potential increase in maintanence work 

## Rationale
Easier, quicker and more efficient handling of potential issues, errors or obstacles in the pipeline. Additionally, a better overview of the pipeline orchestration process. 

### Considerations

Implementation: 
- how the channels are integrated with the logger
- what types of events or errors trigger alerts at each logging level 
- testing accuracy and reliability of the alerts

Maintaining: 
- Should logs be archived or deleted? If so, which ones and when? Log rotation system? 
- The levels of the tresholds may have to be adjusted over time in order to fine-tune the alerts. Thus, it is good to have a periodic review of how (in)effective they are.
- Audience responsibility: possibly develop guidelines which alerts require which audience to act. This can keep everyone in the loop, yet maintain clarity on individual tasks and responsibilities
- In the long-term make sure that the alerts are being distributed to the (still) relevant audiences, and adjust accordingly
- Alert noise reduction: introduce possible ways of grouping similar or related alerts in order to avoid alert channel overflows 

## Additional Notes
This ADR relates to *insert all other log and alert ADRs* 

## Feedback and Suggestions


