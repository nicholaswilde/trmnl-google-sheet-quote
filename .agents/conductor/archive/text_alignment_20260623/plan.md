# Implementation Plan - Layout Text Alignment Control

This plan outlines the steps to add a configuration option to choose the layout text alignment.

## Phase 1: Logic & Styling Implementation (SHA: 15d8c922fa5f78471f4d39ca8d9c572a3daa6b4a)
Add the configuration field and apply alignment styling depending on user selection in all Liquid files.

- [x] Task: Add custom field `text_alignment` in `src/settings.yml`
    - [x] Configure keyname, name, type (select with Center/Left/Right options), and default to Center.
- [x] Task: Update styling in `src/full.liquid`
    - [x] Map user alignment choice to CSS classes (or style updates) applied to quote text and author elements.
- [x] Task: Update styling in `src/half_horizontal.liquid`
    - [x] Apply layout text alignment styling based on selection.
- [x] Task: Update styling in `src/half_vertical.liquid`
    - [x] Apply layout text alignment styling based on selection.
- [x] Task: Update styling in `src/quadrant.liquid`
    - [x] Apply layout text alignment styling based on selection.
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Verification (SHA: 01dc4308e12ba4dae3a48b41300de3f3cce214f6)
Verify layout rendering under different alignment selections.

- [x] Task: Verify rendering with Centered alignment (Default)
    - [x] Open local preview server and check layout alignment.
- [x] Task: Verify rendering with Left alignment
    - [x] Update `.trmnlp.yml` custom_fields to include `text_alignment: "Left"` and verify text is left-aligned.
- [x] Task: Verify rendering with Right alignment
    - [x] Update `.trmnlp.yml` custom_fields to include `text_alignment: "Right"` and verify text is right-aligned.
- [x] Task: Run formatting task
    - [x] Execute `task format` to clean up file formatting.
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)
