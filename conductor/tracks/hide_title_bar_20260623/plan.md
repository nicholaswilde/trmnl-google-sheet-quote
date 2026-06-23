# Implementation Plan - Hide Title Bar Option

This plan outlines the steps to add a configuration option to hide the TRMNL title bar.

## Phase 1: Logic & Configuration Implementation
Add the configuration field and wrap title bars in conditional logic in the Liquid files.

- [ ] Task: Add custom field `hide_title_bar` in `src/settings.yml`
    - [ ] Configure keyname, name, type (select with Yes/No options), and default to No.
- [ ] Task: Update title bar wrapper in `src/full.liquid`
    - [ ] Wrap the title bar div with `{% unless trmnl.plugin_settings.custom_fields_values.hide_title_bar == 'Yes' %}` conditional.
- [ ] Task: Update title bar wrapper in `src/half_horizontal.liquid`
    - [ ] Wrap the title bar div with conditional logic.
- [ ] Task: Update title bar wrapper in `src/half_vertical.liquid`
    - [ ] Wrap the title bar div with conditional logic.
- [ ] Task: Update title bar wrapper in `src/quadrant.liquid`
    - [ ] Wrap the title bar div with conditional logic.
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Verification
Verify layout scaling with and without title bar rendering.

- [ ] Task: Verify rendering with title bar enabled (Default)
    - [ ] Open local preview server and check layout.
- [ ] Task: Verify rendering with title bar disabled
    - [ ] Update `.trmnlp.yml` custom_fields to include `hide_title_bar: "Yes"` and verify title bar is omitted.
- [ ] Task: Run formatting task
    - [ ] Execute `task format` to clean up file formatting.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)
