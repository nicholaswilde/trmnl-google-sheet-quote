# Specification - Implement GitHub Sync for TRMNL Plugin

## Overview
This track implements automatic synchronization between this GitHub repository and the TRMNL platform using the `trmnlp` CLI tool and GitHub Actions. This ensures that code changes are pushed to TRMNL on releases (tags) and configuration changes made via the TRMNL UI are pulled back into the repository.

## Functional Requirements
- **Bi-directional Sync:** Implement both "Push" (Repository to TRMNL) and "Pull" (TRMNL to Repository) workflows.
- **Push Workflow:**
    - Trigger: On every new tag commit.
    - Action: Pushes the local state of the plugin (from `src/`) to the TRMNL platform.
- **Pull Workflow:**
    - Trigger: Daily at midnight PST and manual trigger via `workflow_dispatch`.
    - Action: Fetches the remote state from TRMNL and creates a Pull Request with any changes found.
- **Configuration:** Use a `.trmnlp.yml` file located in the `src/` directory to define the plugin mapping.
- **Authentication:** Use the `TRMNL_API_KEY` GitHub Secret for all API interactions.

## Non-Functional Requirements
- **Security:** Ensure the `TRMNL_API_KEY` is never logged or exposed in workflow outputs.
- **Conflict Handling:** The push workflow should include basic checks to avoid overwriting remote changes that haven't been pulled yet (handled by `trmnlp` tool logic).

## Acceptance Criteria
- [ ] A `.trmnlp.yml` file exists in `src/`.
- [ ] GitHub Actions workflow `trmnlp-push.yml` is triggered successfully on a tag push.
- [ ] GitHub Actions workflow `trmnlp-pull.yml` can be triggered manually and runs on the specified schedule.
- [ ] Documentation (README.md) is updated to include instructions for setting up the `TRMNL_API_KEY` secret.

## Out of Scope
- Automated installation of the `trmnlp` tool on local developer machines (this remains a manual setup step for developers).
- Management of multiple TRMNL plugins (this repo currently only hosts one).