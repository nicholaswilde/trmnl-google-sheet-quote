# Implementation Plan - Hide Title Bar Option

This plan outlines the steps to add a configuration option to hide the TRMNL title bar.

## Phase 1: Logic & Configuration Implementation (SHA: ec0d8be9eeda53e2a37124af06963252df73b925)
Add the configuration field and wrap title bars in conditional logic in the Liquid files.

- [x] Task: Add custom field `hide_title_bar` in `src/settings.yml`
    - [x] Configure keyname, name, type (select with Yes/No options), and default to No.
- [x] Task: Update title bar wrapper in `src/full.liquid`
    - [x] Wrap the title bar div with `{% unless trmnl.plugin_settings.custom_fields_values.hide_title_bar == 'Yes' %}` conditional.
- [x] Task: Update title bar wrapper in `src/half_horizontal.liquid`
    - [x] Wrap the title bar div with conditional logic.
- [x] Task: Update title bar wrapper in `src/half_vertical.liquid`
    - [x] Wrap the title bar div with conditional logic.
- [x] Task: Update title bar wrapper in `src/quadrant.liquid`
    - [x] Wrap the title bar div with conditional logic.
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Verification (SHA: da147ab2fbf3dcfa3805a2a07938da9093778a92)
Verify layout scaling with and without title bar rendering.

- [x] Task: Verify rendering with title bar enabled (Default)
    - [x] Open local preview server and check layout.
- [x] Task: Verify rendering with title bar disabled
    - [x] Update `.trmnlp.yml` custom_fields to include `hide_title_bar: "Yes"` and verify title bar is omitted.
- [x] Task: Run formatting task
    - [x] Execute `task format` to clean up file formatting.
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)
