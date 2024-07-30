# Naming Convention for Models in VIEWS Pipeline

| ADR Info            | Details                                      |
|---------------------|----------------------------------------------|
| Subject             | Naming Convention for Models in VIEWS Pipeline |
| ADR Number          | 003                                          |
| Status              | Accepted                                     |
| Author              | Mihai, Sara, Simon                           |
| Date                | 29.07.2024                                   |

## Context
In the context of the VIEWS pipeline, there is a need to standardize the naming convention for models to ensure consistency and ease of identification. This involves defining a clear and simple convention that can be applied uniformly across all models.

## Decision
The decision is to adopt a naming convention for models that follows the format `[adjective_noun]`. Examples include `orange_pasta` and `purple_alien`. This convention provides a unique and memorable identifier for each model while maintaining simplicity.

### Overview
This decision establishes a standardized naming convention for models in the VIEWS pipeline, using the format `[adjective_noun]`.

## Consequences
**Positive Effects:**
- Ensures a clear and consistent naming convention for models.
- Simplifies identification and communication about specific models.
- Reduces the likelihood of naming conflicts.

**Negative Effects:**
- The chosen adjectives and nouns may seem arbitrary or lack immediate meaning.

## Rationale
The rationale behind this decision is to promote consistency and ease of identification across the VIEWS pipeline. A standardized naming convention ensures models can be managed and referenced efficiently, especially as their number increases.

Using highly descriptive names like algorithm_queryset_target_date would become cumbersome and unwieldy, particularly since some models are only distinguished by their hyperparameters. Therefore, detailed information about each model should be documented in the model's README and the appropriate configuration files (see documentation/ADRs/002_separation_of_configs.md for more info).

### Considerations
- Potential challenges include ensuring that all team members adhere to the new naming convention.
- Choosing appropriate adjectives and nouns that are distinctive.

## Additional Notes
Tools or scripts can be developed to assist in generating compliant model names if necessary.

### Example Names
- `blue_sky`
- `vast_forest`
- `sleeping_dragon`

### Implementation
All new models should be named according to this convention. Existing models should be reviewed and renamed if necessary to align with the new standard.

## Feedback and Suggestions
Team members and stakeholders are encouraged to provide feedback or suggest improvements on the naming convention through repository issues or during regular team meetings.