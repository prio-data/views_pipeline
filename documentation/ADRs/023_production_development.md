# Production and Development Branches

| ADR Info            | Details           |
|---------------------|-------------------|
| Subject             | Production and Development Branches  |
| ADR Number          | 023   |
| Status              | Accepted   |
| Author              | Borbála   |
| Date                | 29.10.2024.     |

## Context
Historically, the `main` branch was used for production and development work occurred directly via feature branched pulled from `main`. This required increased testing and restrictions on `main` such as making it protected or creating a GitHub action that prevents merging if branch is behind. These additional restrictions made the development cumbersome and increased the risk of merging unstable features.

Therefore, we decided to establish a dedicated `production`(renamed from `main`) branch and a `development` branch, from where the feature branches are pulled instead of the former `main`. The `development` branch is synchronized with the `production` branch.


## Decision

### Overview

We renamed the `main` branch to `production` and established a new `development` branch as the main source for feature branches. Development work will now occur in feature branches off `development`, which will be synced periodically with `production`. The exact synchronization procedure is to be discussed, decided, and documented in [024_development_and_production_sync.md](/documentation/ADRs/024_development_and_production_sync.md). The `production` branch remains protected with the condition that two reviewers should accept the Pull Request in order to be merged. There GitHub action that prevents merging if branch is behind still applies to `production` branch (although this workflow ensures that the `development` branch is never behind `production` branch) and a new action is created for the same reason targeting `development` branch.

## Consequences

**Positive Effects:**
- Clear separation of production-ready code and active development work.
- Only well-tested and stable features can reach production.
- Future GitHub actions can push directly to `development` branch, but `production` is still protected.
- Improved alignment with CI/CD workflows.

**Negative Effects:**
- Existing Pull Requests to `production` cause `development` to be behind `production`.
- `production` branch requires constant synchronization and additional testing to prevent the risk of unstable features reaching production.

## Rationale

A separate `development` branch allows for a stable, tested `production` branch (production) that is not impacted by experimental changes. This decision supports the integration of CI/CD workflows.

### Considerations

- GitHub action (e.g. updating the model catalogs) could not push to the `main` branch
- Every small feature required to be approved by two reviewers, which made the development process slower. The `development` branch aims to accelerate the development of small features.
