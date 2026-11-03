---
name: release-summary
description: Generates a clean, professional GitHub release summary based on git logs using scripts/release_summary.py.
---

# /release-summary [range]

Generates a clean, professional GitHub release summary based on git logs.

## Description

This skill uses `scripts/release_summary.py` to retrieve git commit logs, format them into a structured markdown summary (Features, Bug Fixes, etc.), and updates the existing GitHub draft release.

## Protocol

1. Execute the Python script. If no range is provided, it automatically detects the latest two tags.

   ```bash
   uv run python3 scripts/release_summary.py [range]
   # or
   task release:summary
   ```

2. **Special Thanks**: If the user asks to add special thanks (e.g. to a contributor or tester), pass `--thanks` (and optionally `--for` / reason):

   ```bash
   # Name and reason
   uv run python3 scripts/release_summary.py [range] --thanks "<Name>" --for "<reason>"

   # Or full message
   uv run python3 scripts/release_summary.py [range] --thanks "Huge thanks to **<Name>** for <reason>!"
   ```

   This generates the section:

   ```markdown
   ### 🙏 **Special Thanks**

   Huge thanks to **<Name>** for <reason>!
   ```

3. The script will parse the commits, generate the markdown, and automatically run `gh release edit` (or `gh release create`) to update the draft release in-place.
