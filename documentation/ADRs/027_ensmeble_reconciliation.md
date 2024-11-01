# Ensemble Reconcilation

| ADR Info            | Details                 |
|---------------------|-------------------------|
| Subject             | Ensemble Reconciliation |
| ADR Number          | 027                     |
| Status              | Accepted                |
| Author              | Jim                     |
| Date                | 01/11/2024              |

## Context
The notebook-based views3/fatalities002 pipeline generates a cm and a pgm ensemble. It was found that the pgm ensemble suffered from what might be termed normalisation issues, in that the peak and total numbers of fatalities forecast at pgm level are clearly too low. In particular, summing forecast fatalities over the pg cells belonging to a given country, a dcomapring to the fatalities forecast for the same country at cm level almost always gives the result that the summed pgm values are significantly - often an order of magnitude - lower
As a quick fix, therefore, a reconciliation function was created which accepts a pgm forecast dataframe and a cm forecast dataframe, fetches via viewser a pgm->cm mapping, computes for every country for every month the sum over its constituent pg cells, and renormalises the pgm forecasts for those cells so that the sum matches the cm-level forecast. A check is performed which ensures that the set of months in the two input dfs is the same.
This is then equivalent to an up-biasing of all the pgm models, which plainly is not a satisfying solution.
The reconciliation will be applied to every pgm-level constituent model from which the pgm ensemble is built.
this is a known issue with legacy models that were adapted in various forms from the old pipeline. Although some hyper-parameters might help mitigate these issues, the challenges are inherent to the models' architecture and loss functions.
Going forward, the explicit goal for all model development efforts is to design architectures, loss functions, optimization routines, sampling strategies, and other methods that address these issues.

## Decision
This reconciliation is to be implemented in the pipeline as a temporary fix in lieu of improvements to the pgm models. The reconciliation function itself needs to be globally available, so should live in common utils.
For each ensemble, a new item of metadata will be created, 'reconcile_with', whose value will either be None, or the name of another ensemble. No checks need be done on whether a valid choice has been made, since the function already checks to see that the two ensembles it is presented with have correctly-formatted indexes, and the identical month-sets. This change needs to be present in the ensemble-creation meta-tool, with the default value of None.
In an ensemble's generate_forecast.py, a code fragment needs to be added where if reconcile_with is not None, the ensemble named by reconcile_with is fetched from storage and presented to the reconciliation function along with each pgm constituent model in turn. 
Warnings are to be issued and logged if negative-valued forecasts are encountered (before setting them to zero) and if large normalisations are necessary.


### Overview
Reconciliation is being deployed partly to allow the aligning of forecasts from the new pipeline with those of the old. Warnings are issued to inform the user if large normalisations are being performed, which indicates poorly-performing pgm-level models.
This feature is very simple to disable via the ensemble metadata dict.
The reconciliation machinery will be maintained as a stable approach to maintain strict consistency between CM-level and aggregated PGM data. In future, it should NOT be viewed as a tool to systematically up-bias PGM models that underestimate conflict fatalities. This underestimation is fundamentally a modeling issue, not a reconciliation problem. Future work will be directed at finding genuine solutions to these issues, as opposed to sticking-plasters.

## Consequences

**Positive Effects:**
- Allows replication of a necessary but frowned-upon feature of the old pipeline
- Keeps the user informed about the relative performance of the pgm and cm models. Serious inconsistency between the two sets of models is a useful indicator of poor (probably pgm-level) model performance.

**Negative Effects:**
- This solution is little more than a hack which we arguably do not want in the codebase
- This does require changes to the ensemble template and all extant ensembles to ensure that their metadata contains the new key.

## Rationale
This is the least intrusive means of implementing this feature, and allowing it to be easily turned on and off

### Considerations
None

## Additional Notes
None

## Feedback and Suggestions
Feedback welcomed
