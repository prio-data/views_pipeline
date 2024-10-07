# Issue Template for Bugfixes

## **Title**
Provide a clear and descriptive title for the issue.

## **Description**
A concise description of the issue or feature request.

## **Steps to Reproduce**
1. List the steps to reproduce the issue.
2. Include any relevant code snippets or screenshots.

## **Expected Behavior**
Describe what you expected to happen.

## **Actual Behavior**
Describe what actually happened.

## **Environment**
- **OS**: (e.g., Windows 10, macOS 11.2)
- **Relevant model**: (e.g., purple_alien)
- **Relevant Library Version**: (e.g., 1.0.0)
- If possible, include the environment.yml file from your current conda environment by running `conda env export | grep -v "^prefix: " > environment.yml`.

## **Additional Context**
Add any other context about the problem here.

## **Checklist**
- [ ] I have searched for existing issues that might be related to this one.
- [ ] I have provided detailed steps to reproduce the issue.
- [ ] I have included all necessary information about my environment.
- [ ] I have attached relevant screenshots or code snippets.

## **Labels**
Assign appropriate labels to categorize the issue (e.g., bug, enhancement, question).

## **Assignees**
Assign the issue to relevant team members.

## **Milestones**
Link the issue to a milestone if applicable.

## **Linked Issues**
Link to any related issues or pull requests.

## **Error Handling & Logging**
- Ensure that any error messages are clear and actionable.
- Include logs if applicable.

## **Future Flexibility**
- Consider how this issue might affect future development and document any potential impacts.

## **ADR Generation**
- Consider whether resolving this issue necessitates the updating and/or the creation of one or more [ADRs](https://github.com/prio-data/views_pipeline/tree/github_issue_guide/documentation/ADRs) to ensure that the ADRs accurately represent the current codebase.

## **Branch**
- Work on a new branch named `issue_<issue_number>_<short_description>`.
