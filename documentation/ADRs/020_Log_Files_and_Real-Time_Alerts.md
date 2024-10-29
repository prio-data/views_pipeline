# Log Files and Real-Time Alerts

| ADR Info            | Details                   |
|---------------------|---------------------------|
| Subject             | Log files and real-time alerts |
| ADR Number          | 020                       |
| Status              | Proposed                  |
| Author              | Marina                    |
| Date                | 28.10.2024                |


## Context
In the previous iterations of the VIEWS data processing pipeline, there were several occurences of errors (at different stages) being unnoticed for extended period of time. As these oversights primarily originated from inadequate monitoring and alerting mechanisms, or lack thereof. In order to avoid such oversights, as well as enhance visibility and responsiveness, there is a necesity to implement more comprehensive log handling throughout the pipeline. This ensures timely detection and relevant handling of critical issues, in turn improving the overall reliability, transparency and operational efficiency of the entire pipeline.

For related ADRs on the generation of different log files, please see the ADRs below:  [NOTE: once all relevant ADRs are on github, links must be added]
[ADR 009 - Log Files for Generated Data](https://github.com/prio-data/views_pipeline/blob/main/documentation/ADRs/009_log_file_for_generated_data.md)
[ADR 016 - Logging and Alerting for Input Drift Detection]()
[ADR 019 - Error Logging and Alerts for Model Training]() 


## Decision
We will implement a real-time alert and notification system that distributes alerts through designated channels — Slack, Email, Prefect, and Weights & Biases (W&B). Alerts will be targeted to specific audiences such as Infrastructure teams, Model Development & Deployment (MD&D) teams, Outreach teams, and individuals responsible for monthly runs. This targeted approach ensures that each alert reaches the appropriate stakeholders promptly, in turn facilitating efficient and effective issue resolution.


## Overview
Alert channels: 
- Slack 
- Email 
- Prefect
- Weights & Biases (W&B)

Logging levels: 
- INFO 
- WARNING 
- ERROR 
- CRITICAL

Audiences: 
- Model Development & Deployment (MD&D): Team responsible for maintaining and deploying systems.
- Infrastructure: Team managing the underlying infrastructure.
- Outreach: Team handling communication and external interactions.
- Monthly-Run Responsible: Individuals overseeing monthly pipeline executions.


Below is a summary of which channels are designated for distributions of specific alerts to the assigned audiences. For alert prioritization, "critical" and "non-critical" alerts are separated, with critical alerts stemming from logging levels ERROR and CRITICAL. 


| Channel | Threshold        | Alert Type                         | Audience                  |
|---------|-------------------|------------------------------------|---------------------------|
| Slack   | ERROR, CRITICAL   | Real-Time, Short Summary + Link to Full Log | MD&D, Infrastructure, Outreach|
| Email   | ERROR, CRITICAL   | Real-Time, Expanded Summary       | MD&D, Infrastructure      |
| Prefect | ALL               | Real-Time, Workflow Status        | MD&D, Infrastructure, Outreach |
| W&B     | ALL               | Performance Metrics               | MD&D, Infrastructure, Outreach |


## Consequences

**Positive Effects:**
- **Timely Issue Resolution:** Real-time alerts enable prompt handling of critical errors, reducing downtime and minimizing impact.
- **Targeted Communication:** Alerts reaching specific audiences ensure that relevant teams are immediately informed, enhancing the efficiency of response efforts.
- **Historical Insights:** Real-time alerts contribute to a log of recurring issues, facilitating trend analysis and proactive problem-solving.
- **Enhanced Transparency:** Improved logging and alerting mechanisms provide greater visibility into pipeline operations, fostering accountability and informed decision-making.

**Negative Effects:**
- **Alert Fatigue:** Without careful configuration, the volume of alerts may overwhelm recipients, leading to important alerts being overlooked.
- **Relevance of Alerts:** Incorrectly targeted alerts can result in irrelevant notifications, causing confusion and reducing trust in the alerting system.
- **Increased Maintenance:** Setting up and maintaining the alerting infrastructure requires additional resources and ongoing adjustments to thresholds and channels.

## Rationale

Implementing a real-time alert and logging system will establish high standards for pipeline reliability by enabling the swift detection and resolution of issues. By categorizing and targeting alerts to the appropriate audiences, we create a robust MLOps infrastructure that supports continuous quality assurance and proactive issue management. This approach minimizes the impact of errors, enhances overall productivity, and ensures high system availability. Comprehensive logging offers valuable insights into pipeline performance, behavior, and potential problems, facilitating continuous improvement and effective orchestration management. Additionally, real-time monitoring and targeted alerts promote transparency and enable teams to adapt quickly to changing conditions. This decision aligns with our organizational goals of maintaining high availability, ensuring robust operational processes, and fostering a culture of proactive and continuous improvement in our MLOps practices.


## Considerations

Implementation: 

- Logger Integration:
    - Choosing a compatible logging framework: we will use Python’s logging.
    - Connect the logger to alert channels using middleware (i.e. Slack API, Mail).
    - Integrate with Prefect and Weights & Biases (W&B) for workflow and performance metrics.
   
- Event and Error Triggers
    - Define clear criteria and examples for each logging level (INFO, WARNING, ERROR, CRITICAL).
    - Use structured logging (e.g., JSON) for easy log parsing and filtering.
    - Set rules for triggering alerts based on event severity.

- Testing and Reliability:
    - Implement a testing strategy with unit, integration, and end-to-end tests for alert verification.
    - Simulate error conditions to validate alert accuracy and reliability.
    - Monitor the alerting system to detect and resolve delivery issues.




Maintaining: 
- Should logs be archived or deleted? If so, which ones and when? Log rotation system? 
- The levels of the tresholds may have to be adjusted over time in order to fine-tune the alerts. Thus, it is good to have a periodic review of how (in)effective they are.
- Audience responsibility: possibly develop guidelines which alerts require which audience to act. This can keep everyone in the loop, yet maintain clarity on individual tasks and responsibilities
- In the long-term make sure that the alerts are being distributed to the (still) relevant audiences, and adjust accordingly
- Alert noise reduction: introduce possible ways of grouping similar or related alerts in order to avoid alert channel overflows 

## Additional Notes


## Feedback and Suggestions
Feedback is welcome!

