---
name: release
description: Automates the versioning, tagging, and deployment process for the project using scripts/release.sh.
---

# /release [patch|minor|major|<version>]

Automates the versioning, tagging, and deployment process for the project.

## Description

This skill handles the release process by executing the `scripts/release.sh` utility. The script will automatically determine the target version (default: next patch, or increments minor/major, or accepts an explicit version), run static analysis and unit tests (`task lint`, `task test`), bump `package.json` and `package-lock.json`, commit, tag, and push atomically to the remote repository.

## Protocol

1. Execute the release script directly or via task runner:

   ```bash
   # Release next patch version (e.g. 1.1.0 -> 1.1.1)
   ./scripts/release.sh
   # or
   task release

   # Release minor or major version
   ./scripts/release.sh minor
   ./scripts/release.sh major
   ```

2. If it succeeds, the new version will be tagged and pushed atomically to the remote repository.
