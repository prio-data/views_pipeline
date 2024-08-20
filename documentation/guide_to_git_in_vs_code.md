# Step-by-Step Guide to Git with Visual Studio Code

## Checking Your Current Branch
1. **Ensure you are on the `main` branch.**
   - Verify this by checking the branch name in the lower-left corner of VS Code.

## Opening the Source Control Panel
2. **Navigate to the Source Control panel.**
   - Click on the icon that looks like three dots connected by lines on the left sidebar of VS Code.

## Pulling the Latest Changes from `main`
3. **Pull the latest changes from the `main` branch.**
   - Click on the ellipsis (three dots) at the top of the Source Control panel.
   - Go to `Pull, Push` and select `Pull` to ensure you have the latest changes from the `main` branch.

## Creating a New Branch
4. **Create a new branch.**
   - In the Source Control panel, click on the ellipsis again.
   - Go to `Branch` and select `Create Branch`.
   - Name your branch descriptively, reflecting the feature or bug fix you’re working on.

## Publishing Your Branch
5. **Publish your branch to the remote repository.**
   - After creating your branch, publish it by clicking on the ellipsis, selecting `Branch`, and then `Publish`.
   - Alternatively, after making your first commit, VS Code will prompt you to publish your branch if you haven’t already done so.

## Working on Your Branch
6. **Start making changes and committing your work to your new branch.**

## Merging `main` into Your Branch (When Needed)
If new features or functionalities are added to `main` and you need them in your branch, follow these steps:

1. **Save, commit, and push your local work.**
   - Ensure all your local changes are saved, committed, and pushed.
   - Go to the ellipsis in the Source Control panel, select `Pull, Push`, and then `Push`.

2. **Switch to the `main` branch.**
   - Use the lower-left corner of VS Code to switch to the `main` branch.

3. **Pull the latest changes from `main`.**
   - Pull the latest changes from the `main` branch to ensure you are up to date.
   - Optionally, verify that the expected updates are present.

4. **Switch back to your branch and merge `main`.**
   - Switch back to your branch by selecting it from the lower-left corner.
   - Merge `main` into your branch by going to the ellipsis, selecting `Branch`, and then `Merge`.

5. **Verify the merge.**
   - Ensure that your branch now includes the new features or updates from `main`.

## Preparing to Create a Pull Request (PR)
1. **Ensure your branch is up to date.**
   - Follow the steps above to ensure your branch is not behind `main`.
   - Double-check on GitHub (View all branches) to confirm that your branch is up to date.

2. **Create a Pull Request on GitHub.**
   - Once you are certain your branch is up to date, go to GitHub and create a Pull Request (PR).

3. **Do not merge to `main` locally.**
   - Never merge changes directly into `main` from your local environment. This should always be done via a GitHub Pull Request.
   - Most repositories will warn you if you attempt to merge locally, but it’s essential to avoid this practice.

Following this guide will help ensure a smooth workflow and reduce the chances of conflicts or issues during the development process.

Thanks for reading this and taking care of out pipeline!