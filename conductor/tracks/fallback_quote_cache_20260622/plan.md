# Implementation Plan - Fallback Offline Quote Cache

This plan outlines the steps to implement a fallback offline quote cache in the Liquid templates.

## Phase 1: Logic Implementation
Add fallback quote caches and trigger logic to all four Liquid templates.

- [x] Task: Define Fallback Cache and Logic in `src/full.liquid`
    - [x] Add JS fallback quotes array (5+ quotes).
    - [x] Update JS try-catch and empty-data conditional logic to load from fallback.
- [x] Task: Define Fallback Cache and Logic in `src/half_horizontal.liquid`
    - [x] Replicate fallback quotes array and logic.
- [x] Task: Define Fallback Cache and Logic in `src/half_vertical.liquid`
    - [x] Replicate fallback quotes array and logic.
- [x] Task: Define Fallback Cache and Logic in `src/quadrant.liquid`
    - [x] Replicate fallback quotes array and logic.
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Verification
Verify that the fallback mechanism displays correctly under simulated error states.

- [~] Task: Verify fallback rendering via local preview server
    - [ ] Test layout rendering with empty data source configuration.
    - [ ] Verify that a random fallback quote and author are successfully displayed on the simulated screen.
    - [ ] Check console warnings to ensure fallback activation is logged.
- [ ] Task: Verify fallback layout formatting
    - [ ] Ensure formatting, margins, text scaling, and fonts behave identically to standard quotes.
- [ ] Task: Run format task to ensure Prettier compliance
    - [ ] Run `task format` to clean up syntax/formatting.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)
