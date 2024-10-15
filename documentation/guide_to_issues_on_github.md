# Guide to GitHub Issues

## Description
To ensure that our team handles GitHub issues correctly and consistently. This guide will serve as a quick reference for all team members, new and experienced, by outlining best practices for creating, addressing, and resolving issues. Our intention is to streamline our workflow, reduce misunderstandings, and ensure that all issues are addressed swiftly and without the need for follow-up questions. If you are new to GitHub and issues, start [here](https://docs.github.com/en/issues).

## Objectives
**Consistency**: Establish a common procedure for creating, discussing, and resolving issues in all repositories.

**Efficiency**: Ensure that all relevant information is included in issues from the outset, and that they are properly assigned, prioritized, and monitored.

**Clarity**: Provide clear, actionable guidelines for communication within issues, including how to ask for help, provide updates, and close issues when resolved.

## Templates

For issues related to [bugfixes](https://github.com/prio-data/views_pipeline/blob/github_issue_guide/documentation/github_bugfix_issue_template.md) and [feature requests](https://github.com/prio-data/views_pipeline/blob/github_issue_guide/documentation/github_feature_request_template.md).

## Guide Content
### Creating an Issue
1. **Writing a Clear and Concise Issue Title**
    * Use descriptive and specific titles.
    * Avoid vague terms like “bug” or “issue.”
    
2. **Essential Details to Include in the Issue Description**
    * Steps to Reproduce: Detailed steps to replicate the issue.
    * Expected Behavior: What should happen.
    * Actual Behavior: What actually happens.
    * Screenshots/Logs: Attach relevant screenshots or logs.

3. **Guidelines for Labeling Issues**
    * Use predefined labels such as `bug`, `documentation`, `help wanted`, `improvement`. See [label guide](https://github.com/prio-data/views_pipeline/labels) for more information.
    * Ensure labels are applied consistently.

4. **Assigning Issues**
    * Assign issues to **at least two** appropriate team members based on expertise. If the task is increasingly significant, additional members may be added.
    * Use the Assignees feature in GitHub.

### Addressing an Issue
1. **Effective Communication within Issue Comments**
    * Be clear and concise.
    * Use [@mentions](https://github.blog/news-insights/the-library/introducing-team-mentions/) to notify specific team members.

2. **Asking for Clarification or Additional Information**
    * Politely request more details if needed.
    * Specify what information is required.

3. **Linking Related Issues or Pull Requests**
    * Use keywords like closes #issue_number to link PRs.
    * Reference related issues using #issue_number.

4. **Requesting a Review or Second Opinion**
    * Use @mentions to request reviews.
    * Provide context for the review.

5. **Updating the Issue Status**
    * Use labels like in `progress`, `blocked`, `needs more info`.
    * Regularly update the status to reflect the current state.

### Handling and Resolving Issues
1. **Confirming Issue Resolution**
    * Ensure the issue is resolved through testing or peer review.
    * Verify that the solution addresses the problem.

2. **Closing an Issue**
    * [Close the issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/administering-issues/closing-an-issue) once resolved.
    * Provide a summary of the resolution.

3. **Documenting the Resolution**
    * [Link to the relevant pull request](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).
    * Summarize the solution and any important details.
  
4. **Updating the ADR**
    * Ensure that any decisions made as part of the feature/bugfix implementations are properly documented as one or more ADRs and linked to in the pull request if the solution involves major changes to the codebase.

5. **Reopening Issues**
    * Reopen if the problem persists.
    * Provide additional context or information.

### Common Pitfalls

1. **Overloading Issues**
   * Avoid combining multiple problems or features into a single issue. This can make it difficult to track and resolve each aspect effectively.

2. **Ignoring Conversations**
   * GitHub Issues are not just for reporting problems; they are also a forum for discussion. Engaging in conversations, providing feedback, and asking questions can lead to better solutions.

3. **Not Using Milestones**
   * Milestones help track progress and set expectations for when issues should be resolved. Neglecting to use them can lead to a lack of direction and missed deadlines.

4. **Poorly Written Titles and Descriptions**
   * Clear, descriptive titles and detailed descriptions make it easier for team members to understand and address issues. Vague or incomplete information can lead to confusion and delays.

5. **Lack of Labels**
   * Labels help categorize and prioritize issues. Not using them can make it harder to manage and sort through issues effectively.

6. **Not Linking Issues to Commits or Pull Requests**
   * Linking issues to relevant commits or pull requests provides context and makes tracking progress easier. This practice is often overlooked but is crucial for maintaining a clear development history.

7. **Ignoring Duplicate Issues**
   * Encourage team members to search for existing issues before creating new ones. Duplicate issues can clutter the tracker and waste time.

8. **Inadequate Error Handling and Logging**
   * Ensure that issues related to error handling and logging are addressed promptly. Neglecting these can lead to recurring problems and difficulty in diagnosing issues.

9. **Not Updating or Closing Issues**
   * Regularly update the status of issues and close them when resolved. Leaving issues open despite being resolved can clutter the tracker and misinform both users and developers.

10. **Lack of Assignments**
    * Assigning issues to specific team members ensures accountability and helps in tracking who is responsible for resolving each issue.


