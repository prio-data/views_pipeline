# Step-by-Step Guide to a Good Branch and Pull Request (PR)

## Creating a New Branch

1. **Always start from the `main` branch.**
   - Before starting any new task, ensure you are on the latest `main` branch. 
   - Pull the latest changes to make sure your branch is up to date, preventing conflicts and ensuring you're working with the current version of the codebase.

2. **Create a new branch for each specific task.**
   - Create a new branch with a clear and descriptive name. 
   - Use a consistent naming convention such as `feature/short-description` or `bugfix/issue-number` to reflect the task you’re working on.

## Keep Branch Scope Focused

3. **Ensure each branch focuses on a single task or issue.**
   - Each branch should focus on a single task or issue. Avoid including multiple, unrelated changes in one branch. 
   - If fixing multiple small, closely related issues, they may be grouped into one branch, but limit this to avoid scope creep and ensure easy review.

## Committing Work to Your Branch

4. **Commit frequently and with clear messages.**
   - Each commit should represent a logical chunk of work. Commit often, but ensure your changes are relevant and cohesive.
   - Avoid bundling unrelated changes in a single commit. Write clear, descriptive commit messages that explain what has changed.

## Keeping Your Branch Up to Date

5. **Regularly pull changes from `main` to keep your branch up to date.**
   - If `main` has changed significantly, pull the latest changes into your branch. 
   - This helps prevent merge conflicts later on and ensures that your branch remains compatible with the rest of the codebase. It’s best to do this frequently rather than waiting until the end of your task.

## Writing a Clear Pull Request (PR)

6. **Ensure the PR focuses on one task.**
   - Your pull request should be scoped to one feature or bug fix. 
   - Keeping the PR focused makes the review process faster, easier, and ensures that testing is straightforward.

7. **Reference related GitHub issues.**
   - In the PR description, reference the GitHub issue number that the PR addresses (e.g., `Fixes #123`). 
   - This creates a clear link between the issue and the PR and ensures the issue is automatically closed when the PR is merged.

8. **Provide a clear and concise description in the PR.**
   - Write a brief summary of what the PR changes and why. 
   - If relevant, include instructions for testing or screenshots for UI changes. 
   - If the PR introduces something experimental or incomplete, clearly note it so reviewers know what to expect.

## Avoid Including Unnecessary Changes

9. **Do not include unrelated changes in the PR.**
   - Avoid adding unrelated "cleanup" or refactoring work in the same PR unless it directly relates to the task at hand. 
   - Any unrelated changes should be handled in a separate branch and PR to maintain focus and ease of review.

## Reviewing and Merging the PR 
**(PLEASE ALSO READ views_pipeline/documentation/guide_to_git_in_vs_code.md)**

10. **Wait for review and feedback.**
    - After submitting your PR, wait for feedback from your reviewers. Be open to suggestions as they help improve the code quality. 
    - If changes are requested, commit the updates to the same branch and resubmit for review.

11. **Do not merge the PR yourself unless explicitly allowed.**
    - PRs should be merged by a designated reviewer or team lead. 
    - They will ensure that all checks pass, no conflicts remain, and that the PR is ready to be integrated into the codebase.

## Closing the Branch

12. **Delete the branch after merging.**
    - After your PR is merged, delete the branch both locally and from the remote repository. 
    - This keeps the repository clean and prevents confusion over stale or unnecessary branches.

---

Following this guide ensures a clean, organized, and efficient workflow for working with branches and pull requests. It also promotes best practices for clear communication, review, and collaboration.
