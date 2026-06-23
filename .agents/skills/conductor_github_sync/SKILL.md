---
name: conductor_github_sync
description: Sync Conductor tracks and GitHub issues. Automates creating GitHub issues from Conductor tracks and importing GitHub issues as Conductor tracks.
---

# Conductor GitHub Synchronization Skill

This skill provides utilities to synchronize local Conductor tracks with remote GitHub issues using the `gh` CLI.

## Instructions

To synchronize the tracks and issues, you can run the following automated tasks:

1. **Bidirectional Sync:**

   ```bash
   task conductor:sync
   ```

   This command will:
   - Identify any local Conductor tracks (active or archived) that do not have an associated GitHub issue. It will automatically create a new draft issue for them on GitHub and write the issue number back to the track's `metadata.json`.
   - Scan for any open/closed GitHub issues in the repository that are not associated with any Conductor track. It will prompt the user to import them as local Conductor tracks automatically.

2. **Sync Tracks to Issues (Only):**

   ```bash
   ruby .agents/skills/conductor_github_sync/scripts/sync_tracks.rb tracks-to-issues
   ```

3. **Sync Issues to Tracks (Only):**

   ```bash
   ruby .agents/skills/conductor_github_sync/scripts/sync_tracks.rb issues-to-tracks
   ```

4. **Auto-Import Unmapped Issues as Tracks:**
   ```bash
   ruby .agents/skills/conductor_github_sync/scripts/sync_tracks.rb issues-to-tracks-auto
   ```
