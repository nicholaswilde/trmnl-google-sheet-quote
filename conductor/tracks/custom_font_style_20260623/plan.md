# Implementation Plan - Custom Font Style Selection

This plan outlines the steps to add a configuration option to choose the typography font style (Sans-Serif vs. Serif).

## Phase 1: Logic & Assets Implementation
Add the configuration field, import font assets, and apply inline CSS styling in all Liquid files.

- [ ] Task: Add custom field `font_style` in `src/settings.yml`
    - [ ] Configure keyname, name, type (select with Sans-Serif/Serif options), and default to Sans-Serif.
- [ ] Task: Update assets and typography style in `src/full.liquid`
    - [ ] Add the Google Fonts link tag for *Merriweather* font family.
    - [ ] Conditionally apply `font-family: 'Merriweather', serif;` style to the quote text container when Serif is selected.
- [ ] Task: Update assets and style in `src/half_horizontal.liquid`
    - [ ] Add the fonts import and conditional styling.
- [ ] Task: Update assets and style in `src/half_vertical.liquid`
    - [ ] Add the fonts import and conditional styling.
- [ ] Task: Update assets and style in `src/quadrant.liquid`
    - [ ] Add the fonts import and conditional styling.
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Verification
Verify font rendering under different selections.

- [ ] Task: Verify rendering with Sans-Serif font (Default)
    - [ ] Open local preview server and check layout font rendering.
- [ ] Task: Verify rendering with Serif font
    - [ ] Update `.trmnlp.yml` custom_fields to include `font_style: "Serif"` and verify Serif font is rendered correctly.
- [ ] Task: Run formatting task
    - [ ] Execute `task format` to clean up file formatting.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)
