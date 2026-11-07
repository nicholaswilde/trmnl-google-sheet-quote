# TRMNL Google Sheet Quote Project Rules

- **Test-Driven Development (TDD)**: Strictly mandatory. Always write failing tests first (Red), implement minimum code to pass (Green), then refactor. Never write unverified implementation code without prior failing tests.
- **Pure Liquid First**: Prioritize pure Liquid templating for rendering, layout, and daily rotation. Avoid unnecessary client-side JavaScript execution dependencies unless platform constraints strictly require it.
- **Dual Payload Compatibility**: Always support both Google Sheets CSV row arrays and JSON payloads (`quote`, `author`) across all templates (`full.liquid`, `half_horizontal.liquid`, `half_vertical.liquid`, `quadrant.liquid`).
- **Google Sheet URL & ID Handling**: `polling_url` must support bare Spreadsheet IDs as well as full Google Sheets URLs (`/edit`, `#gid=0`, query parameters) with daily cache-busting timestamp (`&t={{ "now" | date: "%Y%m%d" }}`).
- **Standard Stack Tools**:
  - Task runner: `task` (`Taskfile.yml`).
  - Test runner: `task test` or `npm test` (`uv run python3 -m unittest discover tests`).
  - Python runner: `uv run` (`rtk uv run`).
  - Linter & Formatter: `shopify theme check` and `prettier`.
  - Secret safety: Never commit plain secrets, tokens, `.trmnlp.yml` with private keys, or `.env`.
