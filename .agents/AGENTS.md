# Workspace Rules & TRMNL Reference

This document provides workspace-specific guidelines and technical references for TRMNL private plugin development in this repository.

## TRMNL Plugin System Reference

### 1. Configuration (`settings.yml`)
- **Refresh Interval**: The `refresh_interval` setting is defined in **seconds** (e.g., `3600` for 1 hour, `86400` for 24 hours). Setting it to a low value (like `60`) will cause excessive polling and may trigger rate limits or drain device batteries.

### 2. URL Templating & Caching
- **Lazy Refreshing**: TRMNL only re-renders the plugin graphic if the fetched data payload has changed. If the data source returns identical content (e.g. a static Google Sheet CSV), TRMNL skips rendering.
- **Cache Busting**: To force daily re-rendering on static data feeds, append a Liquid date cache-buster parameter to the `polling_url` in `settings.yml`:
  `polling_url: https://example.com/data?t={{ "now" | date: "%Y%m%d" }}`
- Google Sheets export endpoint ignores unknown query parameters but TRMNL evaluates the changing URL as a new cache key.

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
