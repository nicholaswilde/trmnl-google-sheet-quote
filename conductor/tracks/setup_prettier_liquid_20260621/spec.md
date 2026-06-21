# Specification: Set up Prettier Formatter for Liquid

## Overview
Install and configure Prettier with the Shopify Liquid plugin to auto-format Liquid code in the project.

## Requirements
- Install `prettier` and `@shopify/prettier-plugin-liquid` as `devDependencies` in `package.json`.
- Create a `.prettierrc` configuration file and `.prettierignore`.
- Add a `format` script to `package.json`.
- Run formatter to clean up all source files in `src/`.

## Acceptance Criteria
- `package.json` contains dependencies and scripts; all files are formatted.
