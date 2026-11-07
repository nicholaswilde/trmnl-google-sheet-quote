<!-- rtk-begin -->
## RTK Command Guidelines
- **Git Operations**: Prefix `git` commands with `rtk` (e.g., `rtk git status`, `rtk git diff`, `rtk git log`, `rtk git commit`, `rtk git push`).
- **GitHub CLI**: Prefix `gh` commands with `rtk` and pipe to `cat` (e.g., `rtk gh issue list | cat`, `rtk gh pr status | cat`). Always pipe to bypass interactive pagers.
- **File & Directory Inspection**: Use `rtk ls`, `rtk tree`, `rtk find`, or `rtk read` when listing or reading files for token-optimized output.
- **Searching**: Use `rtk rg` or `rg` (ripgrep) for line search pattern matching to save tokens.
- **Node / NPX Operations**: Prefix `npx` commands with `rtk` (e.g., `rtk npx ...`, `rtk test npx ...`, `rtk err npx ...`). Automatically routes known tools (ESLint, Prettier, TypeScript, Vitest) to specialized filters and strips package execution boilerplate.
- **Build & Test Outputs**: Use `rtk err` or `rtk test` when running build/test commands to filter output to errors/failures only (e.g., `rtk test npx shopify theme check`).
- **Exceptions**: Inside `ctx_execute` / `ctx_batch_execute` sandbox code, skip `rtk` (only printed output enters context). Drop `rtk` when exact raw bytes or patch required (`git diff` patch).
<!-- rtk-end -->

<!-- context-mode-begin -->
## Context-Mode Routing Guidelines
- **Derive, Do Not Dump**: Do NOT use `ctx_execute_file` or `ctx_execute` to dump whole file or full config. Print only specific value, matches, count, or known line range needed.
- **Tool Call Surface**: When using MCP wrappers, call `call_mcp_tool` with `ServerName: "context-mode_context-mode"` (or `"context-mode"`) and `ToolName: "ctx_execute"`, `"ctx_execute_file"`, `"ctx_batch_execute"`, `"ctx_fetch_and_index"`, `"ctx_search"`, or `"ctx_index"`.
- **Mandatory Routing**:
  - For analyze/count/filter/compare/search/parse/transform tasks, write code with `ctx_execute` and print only final answer.
  - For analyzing/exploring inside file, use `ctx_execute_file`. Use native `read_file` only when editing requires exact bytes or small known range.
  - Use `ctx_batch_execute` for multi-command repository reconnaissance.
  - Use `ctx_execute` for shell commands whose output may exceed short fixed answer.
  - Use `ctx_fetch_and_index` for web content, then `ctx_search` to query it.
  - Return only derived answers, concise summaries, selected snippets, or file paths.
<!-- context-mode-end -->

<!-- ponytail-begin -->
## Ponytail (Lazy Senior Dev Mode) Guidelines
- **Stop at first rung that holds**:
  1. Need to build at all? (YAGNI)
  2. Already in codebase? Reuse existing helpers/utils/patterns.
  3. Stdlib does it? Use it.
  4. Native platform feature covers it? Use it.
  5. Installed dependency solves it? Use it.
  6. Can be one line? One line.
  7. Only then: write minimum working code.
- **Bug fix = root cause, not symptom**: Fix shared function/path rather than individual callers.
- **Rules**:
  - No unrequested abstractions, boilerplate, or avoidable dependencies.
  - Deletion over addition. Boring over clever. Fewest files possible.
  - Shortest working diff wins once problem understood.
  - Mark deliberate simplifications cutting real corner with `ponytail:` comment naming ceiling and upgrade path.
  - Ensure logic leaves behind ONE runnable check (assert-based demo/self-check or small test file). Trivial one-liners need none.
<!-- ponytail-end -->

<!-- caveman-begin -->
## Caveman Guidelines
Respond terse like smart caveman. All technical substance stay. Only fluff die.

Rules:
- Drop: articles (a/an/the), filler (just/really/basically), pleasantries, hedging.
- Fragments OK. Short synonyms. Technical terms exact. Code unchanged.
- Pattern: [thing] [action] [reason]. [next step].
- Not: "Sure! I'd be happy to help you with that."
- Yes: "Bug in auth middleware. Fix:"

Switch level: /caveman lite|full|ultra|wenyan
Stop: "stop caveman" or "normal mode"

Auto-Clarity: drop caveman for security warnings, irreversible actions, user confused. Resume after.

Boundaries: code/commits/PRs written normal.
<!-- caveman-end -->

<!-- codegraph-begin -->
## CodeGraph

In repositories indexed by CodeGraph (`.codegraph/` directory exists at repo root), reach for it BEFORE grep/find or reading files when exploring code:

- **MCP tool**: `codegraph_explore` answers source + call path + blast radius in one call. Dynamic-dispatch hops included. Name file or symbol in query to read current line-numbered source.
- **Shell**: `codegraph explore "<symbol names or question>"`.

If no `.codegraph/` directory exists, skip CodeGraph entirely.
<!-- codegraph-end -->

<!-- serena-begin -->
## Serena Semantic Navigation & LSP Integration
Use Serena (`serena`) MCP tools for semantic navigation, AST symbol inspection, LSP diagnostics, and project memories:
1. **Map first**: Call `get_symbols_overview` on target file instead of reading entire file.
2. **Read target symbol only**: Call `find_symbol` with `include_body: true` for target function/class/method.
3. **Check callers**: Call `find_referencing_symbols` or `find_implementations` before signature or behavior changes.
4. **Edit by symbol**: Use `replace_symbol_body`, `insert_after_symbol`, `insert_before_symbol`, or `rename_symbol`. Use standard edit for small tweaks or non-code files.
5. **Verify diagnostics**: Call `get_diagnostics_for_file` after edits to catch LSP errors before full test run.
<!-- serena-end -->

<!-- headroom-begin -->
## Headroom MCP (Context Window Compression)
Use Headroom (`headroom`) MCP tools to manage context window consumption on large payloads:
- `headroom_compress`: Shrink large tool outputs or raw data.
- `headroom_retrieve`: Retrieve original content by hash if specific details needed.
- `headroom_stats`: Monitor headroom cache usage.
<!-- headroom-end -->

<!-- ripwire-begin -->
## Ripwire CLI Guidelines

Use `ripwire` CLI (prefixed with `rtk ripwire`) for AST codebase mapping, call graphs, blast radius, and structural queries:

- **CLI First**: Always invoke `rtk ripwire <dir> [flags]` via CLI; do NOT use MCP server.
- **Task Orientation**: `rtk ripwire <dir> --for="<task>"` for ranked signatures and bodies.
- **Task Bundle**: `rtk ripwire <dir> --pack-task="<task>" --legend=compact`.
- **Stack Trace / Error**: `rtk ripwire <dir> --from-trace=FILE --legend=compact` (`-` for stdin).
- **Call Graph**: `rtk ripwire <dir> --callers=SYM`, `--callees=SYM`, `--uses=SYM`.
- **Blast Radius**: `rtk ripwire <dir> --impact=SYM --legend=compact` before changing shared code.
- **Quality Delta & Gate**: `rtk ripwire <dir> --quality-delta --legend=compact` and `--test-gate --legend=compact`.
- **Atomic Edits**: `rtk ripwire <dir> --replace-symbol-body=SYM --edit-payload=FILE` without whole-file re-reading.
<!-- ripwire-end -->

<!-- ripgrep-guidelines-begin -->
## Ripgrep Guidelines
- **Pattern Searching**: Always use `rg` (ripgrep) or `rtk rg` instead of standard `grep` to search text inside files quickly and save token output.
- **Scope**: Use `-t liquid` or `-t yaml` where appropriate, `-l` for file listing, keep context small (`-C 1`).
<!-- ripgrep-guidelines-end -->

<!-- fd-rules-begin -->
## File Discovery (`fd`)
- **Prefer `fd`**: Use `fd` (or `rtk fd`) instead of `find` for finding files and directories across repositories.
- **Scope**: Respects `.gitignore`, skips build directories and caches, runs faster, and saves context tokens.
<!-- fd-rules-end -->

<!-- uv-rules-begin -->
## Python Execution with `uv`
- **Prefix with `uv`**: Always execute Python scripts, tools, and tests via `uv run python3 <script>` (e.g. `uv run python3 scripts/generate_daily_quote.py`) or `uv run <command>`. Never run bare `python3` or `python`.
<!-- uv-rules-end -->

<!-- sensitive-information-protection-begin -->
## Sensitive Information & Secret Protection
- Never commit secrets, passwords, tokens, API keys, `.trmnlp.yml`, or `.env` files.
- Never use blanket staging (`git add .` or `git add -A`). Stage files explicitly and review staged changes.
- Ensure configuration templates (`.trmnlp.yml.example`) contain placeholders only.
<!-- sensitive-information-protection-end -->

# Workspace Rules & TRMNL Reference

This document provides workspace-specific guidelines and technical references for TRMNL private plugin development in this repository.

## TRMNL Plugin System Reference

### 1. Configuration (`settings.yml`)
- **Refresh Interval**: The `refresh_interval` setting is defined in **minutes** (e.g. `15`, `60`, `360`, `720`, `1440`). For once-daily updates, use `1440`. Setting a large value like `3600` results in 60 hours.

### 2. URL Templating & Caching
- **URL Templating**: `polling_url` supports Liquid variable interpolation and filters. The Google Sheet URL template extracts the spreadsheet ID from either a raw ID or full URL and appends `&t={{ "now" | date: "%Y%m%d" }}` for daily cache-busting.
- **Dual Data Handling**: Liquid templates support both CSV datasets (polled directly from Google Sheets) and JSON payloads (`api/today.json`). For CSV data, pure Liquid date indexing (`now | date: "%j"`) determines the daily rotating quote row.

### 3. Liquid Template Syntax
- **Accessing User Settings**: Access user-configured custom fields using:
  `{{ trmnl.plugin_settings.custom_fields_values.field_key }}`
- **Arithmetic Limitation**: Inline math expressions (e.g. `data.size - 1`) are not supported as filter arguments in standard Liquid. Perform calculations beforehand:
  ```liquid
  {% assign limit = data.size | minus: 1 %}
  {% assign formatted_data = data | slice: 1, limit %}
  ```

### 4. Client-Side JavaScript execution
- Client-side `<script>` tags inside Liquid templates are executed on the TRMNL server within a headless browser during the graphic generation phase.
- To skip rendering/displaying a plugin dynamically (e.g. when there is no new data), set `window.TRMNL_SKIP_DISPLAY = true;` inside a `<script>` tag.

## Testing & Quality Gates

### Test-Driven Development (TDD) Protocol
Development in this repository strictly adheres to TDD principles:
1. **Red Phase**: Write failing unit or regression tests in `tests/` before writing any feature or fix implementation. Run `task test` to verify failure.
2. **Green Phase**: Write the minimum code necessary to make the tests pass.
3. **Refactor Phase**: Clean and optimize code while keeping tests green, adhering to ponytail minimalism.

### Quality Gates
Before completing or committing any task:
- [ ] `task test` passes all unit and regression tests (`uv run python3 -m unittest discover tests`).
- [ ] `task format` / `npx prettier --check "src/**/*.liquid" "src/**/*.yml"` passes formatting validation.
- [ ] `npm run lint` (`shopify theme check`) passes without errors.

## Task & Issue Tracking
- **Remote GitHub Issues Only**: All features, enhancements, and bugs are tracked directly in remote GitHub issues using `gh` CLI. Do not initialize or maintain local Conductor tracks.
- **Commit References**: Use `Fixes #<issue_id>` in commit messages to automatically close issues when pushed.

## What To Do Next
- When asked "what to do next" (or similar), **always check the remote repository issues first** using `gh`:
  ```bash
  rtk gh issue list | cat
  ```
