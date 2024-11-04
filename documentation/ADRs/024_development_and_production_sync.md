
# Production and Development Sync


| ADR Info            | Details           |
|---------------------|-------------------|
| Subject             | Production and Development Branch Synchronization  |
| ADR Number          | 024   |
| Status              | Accepted   |
| Author              | Simon  |
| Date                | 31.10.2024.    |

## Context

We aim to establish a new benchmark in MLOps for early warning systems (EWS), specifically for conflict forecasting, which demands high standards of reliability, transparency, and seamless update processes. Given the high stakes of forecasting in EWS, the branching strategy must support robust, transparent, and consistent updates, with a focus on ensuring production stability while accommodating active, iterative development. See [023_production_development.md](documentation/ADRs/023_production_development.md) for more information.

To support continuous quality assurance, real-time monitoring, and rapid model updates, the synchronization between development and production branches must be structured to maintain reliability and performance while addressing the following critical needs:
- Irregular Deployment Frequency: The project requires deployments ranging from weekly to monthly, demanding a workflow that can handle periodic updates without disrupting production stability.
- Critical Model Monitoring: Ensuring real-time model monitoring is essential to maintain the accuracy and reliability of predictions, with a strong focus on data drift detection, model performance assessment, and feature validation across deployment cycles.
- Coupled ML and Non-ML Components: Some non-ML components are tightly integrated with ML workflows, requiring synchronized updates to avoid dependency issues in production.
- Versioning and Traceability: Maintaining version control and artifact management is crucial for reproducibility, rollback, and historical comparison, particularly in a pipeline that supports high-stakes decision-making and early action.

This ADR defines the branching and synchronization structure necessary to support these requirements while adhering to MLOps best practices, ensuring the production branch remains stable and reliable for operational forecasting while allowing iterative improvements in development. 
## Decision

To achieve the requirements described in the Context section, we will implement the following strategy for branching and synchronization strategy, optimized for the EWS pipeline:

### Overview

**Branch Structure and Sync Strategy**

1. **Primary Branches**
- **Production:** Serves as the stable branch for all production-ready code and models. Only validated updates are merged here, ensuring production stability for high-stakes decision-making.
- **Development:** Acts as the main integration branch for feature development, model updates, and experiment integration. All new features are developed in dedicated feature branches based on this branch and merged via Pull Requests (PRs) to ensure controlled updates and testing.

2. **Feature Branch Workflow**
- Feature branches are created off development for isolated testing of new features, models, or configurations.
- Each feature branch undergoes rigorous PR reviews and automated testing to ensure compatibility, stability, and performance before merging into development. This approach maintains the stability of development, reducing errors upon merging to production.

3. **Syncing Development to Production**
- **Periodic Pull Requests:** At regular intervals (between weekly and monthly), development will be merged into production via a Pull Request once a full validation cycle is completed.
- **Staging Environment Validation:** A staging environment replicates production settings to validate the integrity of development before merging into production. This includes running inference tests, drift detection, performance checks, and monitoring to detect issues pre-deployment, ensuring production stability.

4. **Hotfix Branches**
- For urgent issues in production, hotfix branches are created directly from production, fixed, tested, and merged back into production. These hotfixes are then backported to development to maintain consistency between branches.

5. **Versioning**
- **Semantic Versioning:** Each production release is tagged with semantic versioning (e.g., v1.0.0, v1.1.0) to facilitate traceability and rollback.

## Consequences

**Positive Effects:**
- **Production Stability:** Clear separation between development and production minimizes the risk of untested code or model updates affecting production stability.
- **Enhanced Monitoring and Quality Assurance:** The use of a staging environment and comprehensive validation checks before each merge ensures consistent quality and reliability in production.
- **Rapid Issue Resolution:** Hotfix branches allow urgent fixes to be deployed directly to production, reducing downtime and maintaining model performance for critical decision-making.

**Negative Effects:**
- **Increased Complexity in Workflow:** Multiple branches and regular sync requirements add to the complexity of the branching strategy, necessitating disciplined version control and coordination across teams.
- **Resource Overhead for Staging and Testing:** Maintaining a staging environment and conducting extensive validation tests for each update demands additional resources but is justified by the critical need for model reliability in production.


## Rationale
This branching and sync structure balances flexibility in development with reliability in production. By keeping development and production branches separate and introducing a staging validation step, we ensure that production remains stable and capable of handling high-stakes forecasts while enabling iterative development in development. The addition of hotfix branches further reduces the risk of downtime due to critical issues in production.

### Considerations
- **Sync Delays:** Frequent updates in development may slow down synchronization with production if not carefully managed. Scheduled periodic merges and staging validation cycles mitigate this risk.
- **Resource Allocation:** The staging environment and enhanced testing for each PR demand additional computational resources and time but align with the need for stability and reliability in conflict forecasting.

## Additional Notes


## Feedback and Suggestions
Feedback is welcome on any additional sync requirements, monitoring tools, or branching conventions. Input on optimizing the staging environment and hotfix management process is also appreciated to ensure alignment with best practices.

---

