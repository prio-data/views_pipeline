# Log Files and Real-Time Alerts

| ADR Info            | Details                   |
|---------------------|---------------------------|
| Subject             | Log files and real-time alerts |
| ADR Number          | 020                       |
| Status              | Approved                  |
| Author              | Marina                    |
| Date                | 01.11.2024                |


## Context
Previous iterations of the VIEWS data processing pipeline encountered errors that went unnoticed at various stages due to inadequate or missing monitoring and alerting mechanisms. To address this, we are developing a robust MLOps infrastructure with comprehensive logging to enhance visibility, responsiveness, and operational efficiency across the pipeline.

This logging framework will improve the timely detection and handling of critical issues, directly supporting reliability and transparency. By enabling proactive monitoring and faster resolution of issues, the pipeline will maintain high performance standards and be better equipped to adapt to changing conditions.

Our goal is to set new MLOps standards in early warning systems, establishing a benchmark for reliable, data-driven decision-making in high-stakes social science applications.

For related ADRs on the generation of different log files and other general logging standards/routines, please see the ADRs below:  

[NOTE: new relevant ADRs links should be added]

[009_log_file_for_generated_data](/documentation/ADRs/009_log_file_for_generated_data.md)

[016_input_drift_detection_logging](/documentation/ADRs/016_input_drift_detection_logging.md)

[017_log_files_for_offline_evaluation](/documentation/ADRs/017_log_files_for_offline_evaluation.md)

[018_log_files_for_online_evaluation](/documentation/ADRs/018_log_files_for_online_evaluation.md)

[019_log_files_for_model_training](/documentation/ADRs/019_log_files_for_model_training.md)

[025_log_level_standards](/documentation/ADRs/025_log_level_standards.md)

[026_log_files_for_input_data](/documentation/ADRs/026_log_files_for_input_data.md)

## Decision
We will implement a real-time alert and notification system that distributes alerts through designated channels — Slack, Email, Prefect, and Weights & Biases (W&B). To ensure clear communication and streamlined response, dedicated Slack channels will be set up for different log levels, with critical alerts (e.g., ERROR and CRITICAL) prioritized to prevent bottlenecks in high-stakes processes. Alerts will also be targeted to specific audiences, including Infrastructure teams, Model Development & Deployment (MD&D) teams, Outreach teams, and individuals responsible for monthly runs.

This targeted and structured approach ensures each alert reaches the appropriate stakeholders promptly, enabling efficient and effective issue resolution aligned with best MLOps practices.

## Overview
Alert channels: 
- Slack (dedicated channels)
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

The table below shows designated channels for distributing alerts by log level and audience, supporting a balanced approach that prioritizes critical issues while keeping teams informed of less urgent warnings. Alerts are segmented into **Critical** (ERROR, CRITICAL) and **Non-Critical** (DEBUG, INFO, WARNING) categories.


| Channel                  | Log Level         | Alert Type                                     | Audience                       | Purpose |
|--------------------------|-------------------|------------------------------------------------|--------------------------------|---------|
| **Slack (Warning Channel)**   | WARNING           | Real-time alert with brief summary | MD&D, Infrastructure           | Alerts teams to potential issues that may require attention if they persist |
| **Slack (Error Channel)**     | ERROR             | Real-time alert with concise summary and link to detailed log | MD&D, Infrastructure           | Immediate notification of high-priority errors needing prompt investigation |
| **Slack (Critical Channel)**  | CRITICAL          | Real-time alert with prominent notification, link to log, and escalation tag | MD&D, Infrastructure, Outreach   | Urgent notification of severe issues requiring instant response to prevent outages |
| **Email**                | ERROR             | Real-time alert with expanded details and troubleshooting guidance | MD&D, Infrastructure           | Allows asynchronous review of high-priority errors, ensuring comprehensive context |
| **Email**      | CRITICAL          | Immediate escalation for critical issues, triggering on-call response | MD&D, Infrastructure, Outreach         | Ensures CRITICAL issues are immediately addressed even outside regular hours |
| **Prefect**              | INFO, WARNING     | Real-time updates on standard workflow stages and performance | MD&D, Infrastructure           | Provides visibility into routine pipeline health and workflow status |
| **Prefect**              | WARNING, ERROR, CRITICAL | Real-time alerts for pipeline issues that could impact outputs | MD&D, Infrastructure, Outreach | Ensures Outreach is notified of impactful warnings or errors relevant to stakeholders |
| **Weights & Biases (W&B)** | INFO, WARNING, ERROR, CRITICAL | Model performance metrics and anomaly detection alerts | All | Enables access to critical model metrics for monitoring, supporting data-driven decisions |


**NOTES**
- **Slack Channels (Warning, Error, Critical)** provide a structured, priority-based notification system tailored to severity. The **Warning channel** alerts MD&D and Infrastructure teams to potential issues that may need attention, while the **Error channel** notifies them of significant errors requiring prompt investigation. The **Critical channel** sends urgent notifications to MD&D, Infrastructure, and Outreach teams, enabling rapid response to severe issues that could impact system stability or outputs.
  
- **Email** serves as an asynchronous channel for ERROR and CRITICAL alerts, providing expanded details and troubleshooting guidance. This channel allows teams to follow up outside of immediate notifications, ensuring comprehensive context for high-priority issues.

- **Prefect** provides real-time visibility into workflow stages and pipeline health for MD&D, Infrastructure, and Outreach teams. INFO and WARNING levels inform MD&D and Infrastructure of routine stages, while WARNING and higher alerts keep Outreach updated on impactful issues.

- **Weights & Biases (W&B)** offers continuous access to model performance metrics and anomaly detection, with INFO, WARNING, ERROR, and CRITICAL levels available to all stakeholders. This channel supports comprehensive monitoring, allowing teams to track model health and proactively adjust as needed.


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
    - Use structured logging (yaml) for easy log parsing and filtering.
    - Set rules for triggering alerts based on event severity.

- Testing and Reliability:
    - Implement a testing strategy with unit, integration, and end-to-end tests for alert verification.
    - Simulate error conditions to validate alert accuracy and reliability.
    - Monitor the alerting system to detect and resolve delivery issues.


Maintaining: 
- The levels of the tresholds may have to be adjusted over time in order to fine-tune the alerts. Thus, it is good to have a periodic review of how (in)effective they are.
- Audience responsibility: possibly develop guidelines which alerts require which audience to act. This can keep everyone in the loop, yet maintain clarity on individual tasks and responsibilities
- In the long-term make sure that the alerts are being distributed to the (still) relevant audiences, and adjust accordingly
- Alert noise reduction: introduce possible ways of grouping similar or related alerts in order to avoid alert channel overflows 

## Additional Notes
...

## Feedback and Suggestions
Feedback is welcome!

