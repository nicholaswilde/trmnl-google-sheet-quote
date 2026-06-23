# Specification - Hide Title Bar Option

## Overview
This feature introduces a user-configurable setting in `settings.yml` allowing users to hide the TRMNL title bar at the bottom of the layout, freeing up valuable screen space for larger quote presentation on e-ink screens.

## Functional Requirements
- **Configuration Option:** Add a new custom field `hide_title_bar` under `settings.yml`:
  - `keyname`: `hide_title_bar`
  - `field_type`: `select`
  - `name`: `Hide Title Bar`
  - `description`: `Hide the bottom plugin title bar to maximize quote size.`
  - `options`: `No`, `Yes`
  - `default`: `No`
- **Conditional Layout Rendering:** Update the four Liquid templates to check the value of `hide_title_bar`. If set to `Yes`, completely omit the `<div class="title_bar">` DOM node from rendering.
- **Affected Layouts:**
  - `src/full.liquid`
  - `src/half_horizontal.liquid`
  - `src/half_vertical.liquid`
  - `src/quadrant.liquid`

## Non-Functional Requirements
- **Layout Adaptability:** The layout must scale cleanly without throwing errors when the title bar is hidden.
- **Consistent UX:** The default setting must preserve the title bar (`No`) to match existing installations.

## Acceptance Criteria
- [ ] Custom field `hide_title_bar` is configured in `src/settings.yml`.
- [ ] Title bar is hidden when `hide_title_bar` is set to `Yes` across all 4 layouts.
- [ ] Title bar is shown when `hide_title_bar` is set to `No` (or not set) across all 4 layouts.
- [ ] Local preview server renders layout variations correctly.
