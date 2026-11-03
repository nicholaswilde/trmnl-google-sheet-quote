# Specification: Pin TRMNL UI Framework Version to 3.1

## Overview
This track updates the TRMNL Google Sheet Quote private plugin to use the latest version of the TRMNL UI Framework (version `3.1`), ensuring compatibility, performance optimizations, and access to new ePaper components while preventing future breaking changes by pinning the version.

## Functional Requirements
- Modify `src/settings.yml` to specify `framework_version: 3.1` at the top level.
- Audit and verify all layout templates inside `src/` (`full.liquid`, `half_horizontal.liquid`, `half_vertical.liquid`, `quadrant.liquid`) to ensure they comply with the TRMNL UI Framework version `3.1` layout classes and best practices.

## Non-Functional Requirements
- Maintain backward compatibility with the Google Sheets data polling strategy.
- Ensure layouts render correctly within the e-ink limits of the TRMNL framework.

## Acceptance Criteria
- `src/settings.yml` contains `framework_version: 3.1`.
- All liquid templates are reviewed and verified to correctly use the layout class selectors (e.g. `layout`, `title_bar`, `columns`, `column`, `markdown`, `richtext`, `content`).
- `conductor/tech-stack.md` is updated to document the target UI Framework version.

## Out of Scope
- Upgrading to other third-party frameworks.
- Modifying the core quote retrieval logic or Javascript execution.
