# Specification: Set up Shopify Theme Check Linter

## Overview
Install and configure Shopify Theme Check to lint Liquid files in the repository.

## Requirements
- Create a `.theme-check.yml` file to configure the linter.
- Configure rules to ignore `node_modules/`, `conductor/`, and `.agents/`.
- Update `tech-stack.md` and document usage instructions in `README.md`.

## Acceptance Criteria
- `.theme-check.yml` is present at the root, ignoring non-source directories.
