# Specification - Git Pre-commit Hook for Prettier Formatting

## Overview
This track implements a Git pre-commit hook to automatically run Prettier formatting on staged changes before they are committed. This ensures code format compliance across all files (Liquid, YAML, JSON, Markdown, etc.) without manual developer intervention.

## Functional Requirements
- **Automatic Formatting on Commit:** When a developer runs `git commit`, the hook must run Prettier on the staged files.
- **Staged Files Only:** The formatting should target only staged files to keep commit times fast and prevent formatting unstaged changes.
- **File Types Covered:** Format Liquid (`.liquid`), YAML (`.yml`, `.yaml`), JSON (`.json`), and Markdown (`.md`) files.
- **Re-stage Formatted Files:** Staged files that are formatted by Prettier during the commit process must be re-staged so the formatting is included in the commit.

## Non-Functional Requirements
- **Speed:** The hook must execute quickly to avoid delaying the git workflow.
- **Portability:** The pre-commit hook setup should be easily bootstrapped by other developers in the repository.
- **Transparency:** The hook should print clear output showing which files were formatted or if any formatting check failed.

## Acceptance Criteria
- [ ] Running `git commit` triggers the pre-commit hook script automatically.
- [ ] Any staged files that are not formatted correctly are automatically formatted and included in the commit.
- [ ] If a syntax error is present (e.g. invalid JSON), the commit should fail with a descriptive error.
- [ ] Hook setup is documented or automated so developers can easily initialize it.

## Out of Scope
- Global linting checks (e.g. running Shopify Theme Check on all files) during pre-commit.
