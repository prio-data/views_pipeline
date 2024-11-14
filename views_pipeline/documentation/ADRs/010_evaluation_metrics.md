# Evaluation Metrics


| ADR Info            | Details            |
|---------------------|--------------------|
| Subject             | Evaluation Metrics |
| ADR Number          | 010                |
| Status              | Proposed           |
| Author              | Xiaolong           |
| Date                | 12.09.2024         |

## Context
In the context of the VIEWS pipeline, it is necessary to evaluate the models using a robust set of metrics that account for the characteristics of conflict data, 
such as right-skewness and zero-inflation in the outcome variable. This decision was made at the Evaluation Metrics Workshop on May 24, 2024. More details can be found in the [Evaluation Metrics Workshop notes](https://www.notion.so/Notes-37de5410f8b547de8e03dddeb70193a6).


## Decision
Below are the evaluation metrics that will be used to assess the performance of models in the VIEWS pipeline:

| Metric                              | Abbreviation          | Task             | Notes                                                                            |
|-------------------------------------|-----------------------|------------------|------------------------------------------------------------------------------------------------------------|
| Continuous Ranked Probability Score | CRPS                  | Probabilistic    | Measures the difference between predicted and observed cumulative distributions                             |
| Brier Score                         | Brier                 | Probabilistic    | Evaluates the accuracy of predicted probabilities by comparing them to actual outcomes                    |
| Jeffreys Divergence                 | JD                    | Probabilistic    | Measures the divergence between two probability distributions                                               |
| Coverage (Histograms)               | -                     | Probabilistic    | Histogram-based measure of prediction coverage                                                             |
| Sinkhorn/Earth-mover Distance & pEMDiv| Sinkhorn/EMD & pEMDiv | Probabilistic | Measures the difference between two probability distributions by calculating the minimal cost to transform one distribution into another |
| Variogram                           | -                     | Probabilistic    | Measures spatial dependence in probabilistic models                                                        |
| Average Precision                   | AP                    | Classification   | Measures the precision-recall trade-off in classification tasks                                             |
| Root Mean Squared Logarithmic Error | RMSLE                 | Regression       | Evaluates the error between predicted and actual values, particularly suited for skewed data                |
| Pearson                             | -                     | Regression       | Evaluates the linear correlation between two variables                                                      |


## Consequences
**Positive Effects:**

- **More Accurate Model Evaluation**: By using metrics that account for the skewness and zero-inflation in the data, model performance can be more accurately assessed.
- **Improved Onset Detection**: Focusing on metrics that emphasize onset detection ensures models are evaluated on their ability to predict critical shifts in conflict.

**Negative Effects:**

- **Difficulty in Interpretation**: Some metrics may require additional expertise to interpret and understand, 
potentially making it harder to communicate results to non-technical.

## Rationale
The selected metrics are designed to address the unique characteristics of conflict prediction data, which tends to be zero-inflated and right-skewed. 
Relying solely on traditional error metrics such as MSE (MSLE) can result in poor performance on relevant tasks like identifying onsets of conflict.

Using a mix of probabilistic and point-based metrics will allow us to:
- Better capture the range of possible outcomes and assess predictions in terms of uncertainty.
- Focus evaluation on onsets of conflict, which are often the most critical and hardest to predict.
- Ensure consistency and calibration across different spatial and temporal resolutions, from grid-level to country-level predictions.

### Considerations
- **Skewed Data**: The distribution of fatalities is often zero-inflated and right-skewed, which makes evaluation more challenging. Metrics must account for this distribution to avoid favoring models that predict zeros too often.
- **Onset Sensitivity**: The ability to detect onsets of conflict is particularly important, as these events are often of the most interest to decision-makers.
