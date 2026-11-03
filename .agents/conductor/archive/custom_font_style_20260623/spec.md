# Specification - Custom Font Style Selection

## Overview
This feature introduces a configuration setting allowing users to choose between a clean modern Sans-Serif font (e.g., *Inter*) and a classic editorial Serif font (e.g., *Merriweather*) for displaying the quote content, enhancing visual presentation flexibility.

## Functional Requirements
- **Configuration Option:** Add a new custom field `font_style` under `settings.yml`:
  - `keyname`: `font_style`
  - `field_type`: `select`
  - `name`: `Font Style`
  - `description`: `Select the typography style for the quote rendering.`
  - `options`: `Sans-Serif`, `Serif`
  - `default`: `Sans-Serif`
- **Font Assets Loading:** Load the Google Font asset for the Serif font family (*Merriweather*, regular and italic weights) in all layouts.
- **Dynamic CSS Styling:** Update the Liquid templates to conditionally apply inline font-family CSS declarations (or CSS class names) depending on the selected `font_style` value.
  - If `Serif`, render the quote with `font-family: 'Merriweather', serif;` style.
  - If `Sans-Serif`, default to the existing `Inter` font family style.
- **Affected Layouts:**
  - `src/full.liquid`
  - `src/half_horizontal.liquid`
  - `src/half_vertical.liquid`
  - `src/quadrant.liquid`

## Non-Functional Requirements
- **Design Cleanliness:** The Serif font must behave gracefully under auto-scaling (`data-value-fit`) restrictions.
- **Fallbacks:** Standard local system fonts must be declared in CSS as fallbacks (e.g., `Georgia, serif` for Serif, and system-ui for Sans-Serif).

## Acceptance Criteria
- [ ] Custom field `font_style` is defined in `src/settings.yml`.
- [ ] Google Fonts *Merriweather* link tag is included in all layouts.
- [ ] Choosing `Serif` renders the quote text using the Serif font.
- [ ] Choosing `Sans-Serif` (or default) renders the quote using Sans-Serif font.
