# Common Querysets for Model Pipelines


| ADR Info            | Details                           |
|---------------------|-----------------------------------|
| Subject             | Common Querysets for Model Pipelines |
| ADR Number          | 011                               |
| Status              | Accepted                          |
| Author              | Simon, Jim, Borbála               |
| Date                | 16.09.2024                        |

## Context
Currently, querysets used by different models are stored under the path `views_pipeline/models/[model]/configs/config_input_data.py`. Each queryset is model-specific. We want to keep to option to have model specific querysets but we also want the option to share querysets across multiple models. Additionally we would like some locality and easy of access to all querysets for the sake of documantion and ease of overview.

To address these points, we propose to modify the directory structure slightly to allow for easier access to querysets and promote reusability. By moving the querysets into a centralized `views_pipeline/common_queryset` directory, querysets can be shared across models without compromising modularity. This change also enhances clarity in the organization of querysets and their associations with models.

## Decision
- All querysets will now be stored as individual scripts under `views_pipeline/common_querysets`. 
- Each queryset will have its own script, and both the script and the function defining the queryset will follow a consistent naming convention based on the first model using it.
- For instance, a queryset for the model "purple_alien" will be named `get_queryset_purple_alien.py` with the function `get_queryset_purple_alien()`. If another queryset merges existing querysets (e.g., `purple_alien` and `orange_pasta`), the merged queryset will also follow the naming convention of the first model using it (e.g., `get_queryset_big_boss.py`).
- The intenal naming of the queryset (the naming send to viewser) should also follow this convention. E.g. for `purple_alien` or `orange_pasta` respectively would be the name of the queryset send to viewser 
- This naming convention ensures traceability and prevents confusion when querysets are shared across multiple models.
- A gradual migration will be employed, moving querysets from model-specific directories to `views_pipeline/common_querysets` as necessary.
- All dataloader's etc will need updating to refelct this change. 
- The `set_path` function have been edited to include the new `common_querysets` directory.
- Queryset names will remain static once assigned to ensure consistency.

## Consequences
**Positive Effects:**
- **Modularity**: Querysets will be easier to locate, understand, and reuse across models, promoting consistency and reducing redundancy.
- **Maintainability**: Shared querysets will ensure that changes to one queryset are reflected in all models using it, simplifying future updates.
- **Clarity**: Maintaining a clear separation of querysets from models will ensure a modular organization of the pipeline.

**Negative Effects:**
- **Migration Overhead**: The migration of querysets to the new structure will be gradual, requiring coordination between model code, dataloaders, and documentation updates.
- **Shared Dependencies**: Merged and shared querysets will inherit changes made to individual querysets, which could introduce unintentional side effects such as unexpected feature transformations or data discrepancies in models using the merged queryset. This is inherently a feature, but one that could led to bugs. As such, developer should be cautious and mindful about functionality.  

## Rationale
The decision to move querysets to a centralized directory aims to make them more accessible and reusable, particularly as models evolve and the pipeline grows. The goal is to improve organization and reduce redundancy without adding unnecessary complexity.

By naming querysets after the first model using them, we ensure traceability and prevent potential conflicts. Naming will remain static to avoid confusion in shared usage across models.

Merged querysets offer flexibility, but it is crucial to understand the implications of changing individual querysets when they are part of a merged set.

## Considerations
- The decision to merge querysets should be carefully evaluated. Merging ensures that changes to individual querysets automatically affect the merged queryset, whereas creating a new queryset from scratch will keep it independent.
- Creating new querysets is most appropriate when models diverge substantially in their feature requirements or when modifications to existing querysets may disrupt dependent models.
- Documentation should point back to the actual queryset being used, avoiding outdated references. Model READMEs and catalogs should clearly state which queryset is associated with each model.
- Developers are encouraged to follow existing docstring examples to document their querysets.

## Additional Notes
- Unit tests for queryset are not required at this time - but should be later on.
- viewser have specific tools for for combining querysets, and this functionality is already documented.

## Feedback and Suggestions
Please provide feedback or suggestions for improvement through the repository’s issue tracker or during regular team meetings.
