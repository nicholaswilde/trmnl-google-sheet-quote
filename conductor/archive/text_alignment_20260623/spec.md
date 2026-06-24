# Specification - Layout Text Alignment Control

## Overview
This feature introduces a user-configurable text alignment setting, allowing users to choose how quotes and authors are aligned on the screen (Center, Left, or Right), enhancing layout design options.

## Functional Requirements
- **Configuration Option:** Add a new custom field `text_alignment` under `settings.yml`:
  - `keyname`: `text_alignment`
  - `field_type`: `select`
  - `name`: `Text Alignment`
  - `description`: `Select alignment for quote and author text.`
  - `options`: `Center`, `Left`, `Right`
  - `default`: `Center`
- **Dynamic Styling Classes:** Update the Liquid templates to conditionally apply alignment styling classes to the quote content container.
  - If `Left`, replace centered layout container styling (e.g. `text--center`, `richtext--center`, `--center`) with left-aligned equivalents (or apply inline styling `text-align: left;`).
  - If `Right`, apply right-aligned equivalents (or apply inline styling `text-align: right;`).
  - If `Center` (default), preserve current centered classes.
- **Affected Layouts:**
  - `src/full.liquid`
  - `src/half_horizontal.liquid`
  - `src/half_vertical.liquid`
  - `src/quadrant.liquid`

## Non-Functional Requirements
- **Visual Balance:** Ensure left/right alignment styling preserves margins and padding, keeping the layout visually appealing.
- **Scaling:** Aligning text must not interfere with text auto-scaling (`data-value-fit`).

## Acceptance Criteria
- [ ] Custom field `text_alignment` is defined in `src/settings.yml`.
- [ ] Text is left-aligned when `text_alignment` is set to `Left` in all 4 layouts.
- [ ] Text is right-aligned when `text_alignment` is set to `Right` in all 4 layouts.
- [ ] Text is centered when `text_alignment` is set to `Center` (or default) in all 4 layouts.
