# Tech Stack

## Frontend / Templating
- **Liquid:** Used for defining the structure and logic of the TRMNL display across various layouts (Full, Half, Quadrant).
- **HTML/CSS:** Standard web technologies used within the Liquid templates to style the quote presentation.

## Configuration & Metadata
- **YAML:** Used in `settings.yml` to define the plugin's configuration options and metadata for the TRMNL platform.

## Data Integration
- **Google Sheets API:** Content is dynamically sourced from Google Sheets.
- **TRMNL Private Plugin Framework:** The underlying platform that handles data fetching, polling intervals, and rendering the Liquid templates on the device.

## Development Tools
- **Git:** For version control and repository management.
- **Gemini CLI:** For project management and workflow automation using the Conductor methodology.
- **trmnlp CLI (via trmnl_preview gem):** Used for local rendering, preview, and syncing with the TRMNL developer platform. Note: Due to limitations in the upstream gem (v0.8.7), it must be patched locally (in `lib/trmnlp/poller.rb`) to follow redirects (for Google Sheets CSV export) and parse `text/csv` content types.
- **GitHub Actions:** Automates code synchronization (pushing layouts on tags and daily pulling configuration changes).
- **Shopify Theme Check:** Linter for verifying Liquid file syntax and best practices.
- **Prettier & @shopify/prettier-plugin-liquid:** Formatter for consistent Liquid and YAML file styling.

## Runtime Environment
The plugin runs within the TRMNL environment; there is no local Node.js or Python server to run. `package.json` exists primarily for metadata.

## Key Files
- `src/settings.yml`: The core configuration. Defines the `polling_url` (Google Sheet CSV export), the user-facing input fields (Spreadsheet ID, column indices), and metadata.
- `src/full.liquid`: The main view template for the full-screen layout.
- `src/half_horizontal.liquid`, `src/half_vertical.liquid`, `src/quadrant.liquid`: Templates for other TRMNL layout sizes.
- `src/img/`: Contains assets like the plugin icon and screenshot.

## Conventions
- **Structure:** Keep all plugin source files inside `src/`.
- **Templating:** Use standard Liquid syntax. Ensure layouts handle dynamic content length gracefully (e.g., long quotes) given the small e-ink screen.
- **Configuration:** Changes to plugin behavior (like adding new user inputs) happen in `src/settings.yml`.
- **Versioning:** Use semantic versioning (SemVer) for version tracking, prefixed by a `v` (e.g., `v1.0.0`). Update `package.json` to match this versioning scheme.
- **TRMNL Integration Rules:**
  - **Refresh Interval:** `refresh_interval` in `settings.yml` is in seconds. Use `3600` for 1 hour. Avoid low intervals (e.g., `60`) in production.
  - **Dynamic Cache Busting:** Append `&t={{ "now" | date: "%Y%m%d" }}` to `polling_url` to bypass lazy-refresh caching daily for static feeds.
  - **Accessing Settings:** Access custom fields in Liquid templates using `{{ trmnl.plugin_settings.custom_fields_values.<keyname> }}`.
  - **Liquid Math:** Do not perform math inside filter arguments (like `data.size - 1`). Use `| minus: 1` filter to assign a helper variable first.
  - **Dynamic Skip:** Set `window.TRMNL_SKIP_DISPLAY = true;` inside scripts to dynamically skip the plugin layout display.
