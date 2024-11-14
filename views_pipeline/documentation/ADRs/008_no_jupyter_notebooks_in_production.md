# No use of Jupyter Notebooks in production*

| ADR Info            | Details                                       |
|---------------------|-----------------------------------------------|
| Subject             | No Use of Jupyter Notebooks in Production     |
| ADR Number          | 008                                           |
| Status              | Accepted                                      |
| Author              | Jim, Mihai, Xiaolong, Simon, Sara             |
| Date                | 30.07.2024                                    |

## Context
The decision to not use Jupyter Notebooks (.ipynb) in production environments is driven by the need for maintainable, efficient, and scalable production code. Jupyter Notebooks, while excellent for exploration and prototyping, introduce challenges when used in production systems. These challenges include issues with version control, code modularity, testing, and deployment consistency.

## Decision
Jupyter Notebooks will not be used in production environments. Instead, they will be reserved for internal development and small experiments. All notebooks must be saved in the appropriate `view_pipeline/models/"model"/notebooks` directory. These notebooks must not be part of any production processes or integrated into the main codebase outside of individual experiments.

### Overview
- **Notebooks in Production**: Absolutely Prohibited
- **Notebooks for Internal Development and experimentation**: Allowed for prototyping and experiments only
- **Example of Storage Location**: `view_pipeline/models/"model"/notebooks`

## Consequences
**Positive Effects:**
- **Maintainability**: Production code is easier to manage and maintain without the complexities introduced by notebooks.
- **Modularity**: Encourages modular and reusable code practices.
- **Testing**: Simplifies the process of writing and running tests.
- **Deployment**: Streamlines deployment processes, ensuring consistency across environments.

**Negative Effects:**
- **Prototyping Overhead**: Developers may need to translate notebook-based experiments into scripts for production use, adding some initial overhead.
- **Learning Curve**: Team members accustomed to using notebooks for all tasks may need to adjust to a script-based workflow for production code.

## Rationale
The primary rationale behind this decision is to ensure that our production code remains clean, maintainable, and efficient. Jupyter Notebooks, while powerful for development and experimentation, do not lend themselves well to the rigorous demands of production environments.

### Considerations
- **Risks**: Potential resistance from developers used to notebooks; need for additional steps to convert notebook code to scripts.
- **Dependencies**: Requires adherence to script-based workflows for production code.
- **Impact**: Facilitates a more robust and maintainable codebase.

## Additional Notes
- **Development Workflow**: Developers can use Jupyter Notebooks for prototyping and experiments but should migrate successful code/prototypes into scripts suitable for production.
- **Version Control**: Notebooks should be version-controlled within their designated directories to preserve the history of experiments and prototyping.
- **Collaboration**: While notebooks can be shared for collaborative development, the final implementation for production should always be script-based.

## Feedback and Suggestions
Team members and stakeholders are encouraged to provide feedback or suggest improvements on this decision. Please submit any feedback through the project's standard communication channels or by opening an issue in the repository.
