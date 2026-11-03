# Implementation Plan - Git Pre-commit Hook for Prettier Formatting

This plan outlines the steps to implement a custom Git pre-commit hook that formats staged files using Prettier.

## Phase 1: Hook and Bootstrap Setup
Create the hook script and update the bootstrapping configurations.

- [ ] Task: Create `.githooks/pre-commit` script
    - [ ] Write a shell script that identifies staged `.liquid`, `.yml`, `.yaml`, `.json`, and `.md` files.
    - [ ] Run `npx prettier --write` on those files.
    - [ ] Automatically re-stage the formatted files using `git add`.
    - [ ] Make the script executable.
- [ ] Task: Integrate hook configuration in `Taskfile.yml`
    - [ ] Update the `bootstrap` task to run `git config core.hooksPath .githooks`.
- [ ] Task: Update development instructions in `README.md`
    - [ ] Document the pre-commit hook and mention that it is configured during `task bootstrap`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Verification
Verify that the hook functions correctly during git commits.

- [ ] Task: Verify hook configuration
    - [ ] Run `task bootstrap` and verify `core.hooksPath` is set to `.githooks`.
- [ ] Task: Verify formatting behavior on commit
    - [ ] Modify a `.liquid` file to contain unformatted spacing.
    - [ ] Stage the file using `git add`.
    - [ ] Run `git commit` and verify the pre-commit hook triggers and formats the file.
    - [ ] Check `git show` to confirm the formatted code was committed.
- [ ] Task: Verify commit failure on syntax error
    - [ ] Introduce a deliberate syntax error in a staged file.
    - [ ] Attempt to commit and verify the hook fails and aborts the commit.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)
