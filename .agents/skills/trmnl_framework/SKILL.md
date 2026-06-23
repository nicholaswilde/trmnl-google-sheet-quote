---
name: trmnl_framework
description: Maintain, verify, and update the TRMNL UI framework version in settings.yml.
---

# TRMNL Framework Version Management Skill

Use this skill to inspect, verify, and update the pinned `framework_version` configuration in the `src/settings.yml` file.

## Usage

### 1. Verification
To verify that the workspace contains a pinned framework version (e.g., target version `3.1`):
```bash
task verify-framework
```
Or directly using the Ruby script:
```bash
ruby .agents/skills/trmnl_framework/scripts/manage_framework.rb verify 3.1
```

### 2. Update
To update the pinned framework version to a new version (e.g. `3.2`):
```bash
task update-framework -- 3.2
```
Or directly using the Ruby script:
```bash
ruby .agents/skills/trmnl_framework/scripts/manage_framework.rb update 3.2
```
