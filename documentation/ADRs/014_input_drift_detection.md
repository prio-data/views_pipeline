# Drift-detection

| ADR Info          | Details               |
|-------------------|-----------------------|
| Subject           | Input drift detection |
| ADR Number        | 014                   |
| Status            | proposed              |
| Author            | Jim Dale              |
| Date              | 02/10/2024            |

## Context
The pipeline needs machinery for checking that the input data entering it has not been compromised by problems or errors in the monthly data ingestion. This machinery also needs the ability to test itself.

## Decision
In discussions involving Simon Polichinel von der Maase, Mihai Croicu and James Dale at the PRIO cabin retreat in Feb 2024, it was decided that input drift detection should be done by the viewser data-fetching client itself, so that drift-detection can be conducted at any time when data is read into the pipeline.

## Consequences

**Positive Effects:**
- Making drift-detection the purview of the data-fetching machinery has made drift-detection an integral part of getting data, as it should be.
- The key infrastructure tool viewser, which is also extensively used *outside* the pipeline, now has very useful additional functionality.

**Negative Effects:**
- Viewser is not an easy package to modify. One of the most important steps in the self-test process - fetching a standard dataset - CANNOT be done inside the viewser package, since it would require a circular import, so this must be done externally. Building the self-test machinery into viewser makes that machinery non-zero-config, in that some external 'set-up' is required.
- Since self-test is now an option at every data-fetching event, some additional flags need to be set and unset in the orchestration to prevent self-testing being done every time data is fetched.
- An additional level of complexity has been added to a key infrastructure package

## Rationale
It was considered that drift-detection should be a natural part of the data-fetching process, and that it would therefore be better to upgrade the data-fetching machinery itself, rather than creating a separate module for drift-detection

### Considerations
Viewser is already a very complex package which is difficult to upgrade and modify. However, harnessing ti to do drift-detection avoids creating yet another package needing maintenance. The overall maintenance and development should be lessened, after the initial investment of time involved in upgrading viewser.

## Additional Notes
None.

## Feedback and Suggestions
Feedback is welcomed.