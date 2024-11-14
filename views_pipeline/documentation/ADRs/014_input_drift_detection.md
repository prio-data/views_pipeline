# Drift-detection

| ADR Info          | Details               |
|-------------------|-----------------------|
| Subject           | Input Drift-Detection |
| ADR Number        | 014                   |
| Status            | Accepted              |
| Author            | Jim Dale              |
| Date              | 02.10.2024            |

## Context
The pipeline needs machinery for checking that the input data entering it has not been compromised by problems or errors in the monthly data ingestion. This machinery also needs the ability to test itself.

## Decision
In discussions involving Simon Polichinel von der Maase, Mihai Croicu and James Dale at the PRIO cabin retreat in Feb 2024, it was decided that input drift detection should be done by the viewser data-fetching client itself, so that drift-detection can be conducted at any time when data is read into the pipeline.

## Consequences

**Positive Effects:**
- Making drift-detection the purview of the data-fetching machinery has made drift-detection an integral part of getting data, as it should be.
- The key infrastructure tool viewser, which is also extensively used *outside* the pipeline, now has very useful additional functionality.

Principal benefits to the pipeline are:

1. Data Ingestion Failure Monitoring:

Consistency & Integrity: Ensures data is received consistently and without corruption. Detects missing or faulty data early.
Alerts for Pipeline Issues: Provides early warning if ingestion fails, allowing for quick intervention and preventing faulty predictions.

2. Detecting Large Shifts in Input Data:

Real-World Event Alerts: Identifies significant shifts in data that may indicate important real-world changes, such as spikes in conflict.
Performance Context: Helps explain performance drops by identifying whether changes in data reflect actual developments or pipeline issues.

3. Monitoring Data Source Reliability:

Detecting 'Bad' Data: Alerts when data sources degrade in quality or become unreliable, preventing contamination of model predictions.
Dynamic Validation: Compares new data against historical patterns, flagging anomalies or corrupted inputs.

**Negative Effects:**
- Viewser is not an easy package to modify. One of the most important steps in the self-test process - fetching a standard dataset - CANNOT be done inside the viewser package, since it would require a circular import, so this must be done externally. Building the self-test machinery into viewser makes that machinery non-zero-config, in that some external 'set-up' is required.
- Since self-test is now an option at every data-fetching event, some additional flags need to be set and unset in the orchestration to prevent self-testing being done every time data is fetched.
- An additional level of complexity has been added to a key infrastructure package

## Rationale
It was considered that drift-detection should be a natural part of the data-fetching process, and that it would therefore be better to upgrade the data-fetching machinery itself, rather than creating a separate module for drift-detection

### Considerations
Viewser is already a very complex package which is difficult to upgrade and modify. However, harnessing ti to do drift-detection avoids creating yet another package needing maintenance. The overall maintenance and development should be lessened, after the initial investment of time involved in upgrading viewser.

## Additional Notes
An enduring challenge is to distinguish between data/measurement problems or irregularities, and genuine shifts or trends in the real-world. Input data might change due to actual events (e.g., novel political instability) or due to errors like faulty data sources, reporting biases, or missing information. These two causes can look similar, making it hard to tell whether a model's performance changes are due to genuine developments or technical problems.
Defining thresholds, limits, and intervals to determine when a new observed value is "different" or "extreme" is an ongoing effort. The challenge lies in setting meaningful boundaries that capture significant changes in the data, without overreacting to normal variability or noise.

Being able to make a more informed effort to distinguish between bad data and real-world evolutions is warranted - but not currently a priority

## Feedback and Suggestions
Feedback is welcomed.