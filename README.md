# :framed_picture: TRMNL Google Sheet Quote :bar_chart:

[![task](https://img.shields.io/badge/Task-Enabled-brightgreen?style=for-the-badge&logo=task&logoColor=white)](https://taskfile.dev/#/)
[![ci](https://img.shields.io/github/actions/workflow/status/nicholaswilde/trmnl-google-sheet-quote/ci.yml?label=ci&style=for-the-badge&branch=main&logo=github-actions)](https://github.com/nicholaswilde/trmnl-google-sheet-quote/actions/workflows/ci.yml)
[![pull](https://img.shields.io/github/actions/workflow/status/nicholaswilde/trmnl-google-sheet-quote/trmnlp-pull.yml?label=pull&style=for-the-badge&branch=main&logo=github-actions)](https://github.com/nicholaswilde/trmnl-google-sheet-quote/actions/workflows/trmnlp-pull.yml)

A private plugin for [TRMNL](https://trmnl.com/) to display quotes from a Google Sheet.

![sheet-quote](https://raw.githubusercontent.com/nicholaswilde/trmnl-sheet-quote/refs/heads/main/src/img/screenshot.png)

## :rocket: Features

- Displays a daily quote synced from a Google Sheet.
- Automated daily quote rotation via GitHub Actions (running daily at 00:00 UTC).
- Quote history tracking to prevent repeating quotes within 30 days.
- Pure Liquid template rendering without client-side JavaScript execution dependencies.
- Option to hide the bottom title bar to maximize quote size.
- Configurable text alignment (Center, Left, Right).

## :gear: How It Works

1. **Daily Quotes**: By default, TRMNL polls `api/today.json` (`refresh_interval: 1440` minutes), updated daily at 00:00 UTC with non-repeating quotes from the public Google Sheet so your screen always refreshes each day.
2. **Custom Google Sheets**: When a custom `Spreadsheet ID or URL` is configured in plugin settings, TRMNL polls your sheet's CSV export and rotates quotes daily via Liquid date indexing (`now | date: "%j"`).
3. **Screen Rendering**: TRMNL renders the selected quote and author on your e-ink display using responsive Liquid templates without client-side JavaScript execution dependencies.

## :hammer_and_wrench: Installation

1. Add or import the private plugin into your TRMNL dashboard.
2. In the plugin settings, paste your **Spreadsheet ID or URL**.
3. (Optional) Set the **Quote Column Index** and **Author Column Index** if your sheet columns differ from column B (`1`) and column C (`2`).

## :gear: Configuration

Configuration is handled within the TRMNL application:

- **Spreadsheet ID or URL**: The ID or shareable link of your Google Sheet (defaults to the author's public quote sheet). Ensure the sheet is shared with "Anyone with the link can view". If your quotes are on a specific non-first tab, paste the full URL containing `&gid=...` or `#gid=...`.
- **Quote Column Index**: The zero-based column index of the quote text in your sheet (e.g. Column A is 0, Column B is 1, default: `1`).
- **Author Column Index**: The zero-based column index of the author text in your sheet (e.g. Column A is 0, Column C is 2, default: `2`).
- **Hide Title Bar**: Option to hide the bottom TRMNL logo and title bar (options: `No`, `Yes`).
- **Text Alignment**: Option to align quote and author text (options: `Center`, `Left`, `Right`).

## :arrows_counterclockwise: GitHub Synchronization

This repository supports automated synchronization with the TRMNL platform via the `trmnlp` CLI tool.

### Setup API Key

To push code changes to the TRMNL platform, you must configure a `TRMNL_API_KEY` secret in your GitHub repository:

1. Go to your repository settings on GitHub.
2. Select **Settings** > **Secrets and variables** > **Actions**.
3. Create a new repository secret:
   - **Name:** `TRMNL_API_KEY`
   - **Value:** Your TRMNL developer API key.

### Auto-Push on Release

Any commit pushed to this repository with a new tag (e.g. `v1.0.2`) will automatically trigger the GitHub Actions workflow to push the updated plugin files in the `src/` directory to the TRMNL platform.

## :question: Troubleshooting

If you see "No data found" or the plugin is stuck on "Loading quote…":

1.  **Check Spreadsheet ID:** Ensure the ID is correct and the sheet is shared with "Anyone with the link" (Viewer access).
2.  **Check Logs:** In the TRMNL dashboard, go to the **Logs** tab for this plugin. Look for "Sheet Quote: Starting execution" to verify the script is running.
3.  **Error Messages:** The plugin displays specific error messages on the screen if data is missing or malformed to help you debug.

## :construction: Development

To make changes, edit the files in the `src` directory. The `.liquid` files control the layout, and `settings.yml` controls the configuration options.

### Local Development & Preview

You can run a local preview server of the plugin to verify layout changes using the `trmnlp` CLI:

1. **Configure Local Variables:** Initialize the configuration file and update `.trmnlp.yml` in the root directory with your Google Sheet credentials:
   ```bash
   task init
   ```
2. **Start the Preview Server:** Run the following command:
   ```bash
   task serve
   ```
3. **Verify:** Open your browser to `http://localhost:4567/full` (or other layout paths) or verify by curling `/render/full.html`.

#### Required Gem Patch for Google Sheets Polling

Because the upstream `trmnl_preview` gem (v0.8.7) does not follow HTTP redirects or parse CSV content types out of the box, you must patch the gem's source code to display Google Sheet data correctly:

1. Locate the gem source file `lib/trmnlp/poller.rb` (run `gem which trmnl_preview` or `gem which trmnlp` to find its path).
2. Add `require 'csv'` to the top of the file:
   ```ruby
   require 'csv'
   ```
3. Update the `perform_request` method to follow HTTP redirects recursively:
   ```ruby
   def perform_request(url, verb)
     conn = Faraday.new(url:, headers: config.plugin.polling_headers)
     response = verb == 'POST' ? conn.post { |req| req.body = config.plugin.polling_body } : conn.get
     if [301, 302, 303, 307, 308].include?(response.status) && response.headers['location']
       perform_request(response.headers['location'], verb)
     else
       response
     end
   end
   ```
4. Update the `parse_body` method to support parsing `text/csv` payloads into the expected `data` array:
   ```ruby
   def parse_body(body, content_type_header)
     content_type = content_type_header&.split(';')&.first&.strip
     case content_type
     when 'application/json', %r{^application/.+\+json} then wrap_array(JSON.parse(body))
     when 'text/xml', 'application/xml', %r{^application/.+\+xml} then wrap_array(Hash.from_xml(body))
     when 'text/html', 'text/plain' then sniff_json(body) || { 'data' => body }
     when 'text/csv' then { 'data' => CSV.parse(body) }
     else log_unknown_type(content_type_header)
     end
   end
   ```

### Testing & TDD Workflow

This project adheres to **Test-Driven Development (TDD)**. Always write failing tests in `tests/` before implementing bug fixes or features:

```bash
task test        # Run full unit and regression test suite
task test:watch  # Continuously run tests on file changes
npm test         # Run tests via npm shortcut
```

### Linting & Formatting

This project uses Shopify's **Theme Check** to lint the Liquid template files and **Prettier** to auto-format files.

- **VS Code**: Install the official **Shopify Liquid** extension to view linting warnings and syntax validation.
- **CLI Verification**: Use the automated Taskfile tasks:
  ```bash
  task format  # Runs Prettier formatter on Liquid and YAML files
  task lint    # Runs Shopify Theme Check linter
  ```

## :balance_scale: License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## :pencil:​ Author

​This project was started in 2025 by [Nicholas Wilde][2].

[2]: https://github.com/nicholaswilde/
