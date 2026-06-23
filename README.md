# :framed_picture: TRMNL Google Sheet Quote :bar_chart:

[![task](https://img.shields.io/badge/Task-Enabled-brightgreen?style=for-the-badge&logo=task&logoColor=white)](https://taskfile.dev/#/)
[![ci](https://img.shields.io/github/actions/workflow/status/nicholaswilde/trmnl-google-sheet-quote/ci.yml?label=ci&style=for-the-badge&branch=main&logo=github-actions)](https://github.com/nicholaswilde/trmnl-google-sheet-quote/actions/workflows/ci.yml)
[![pull](https://img.shields.io/github/actions/workflow/status/nicholaswilde/trmnl-google-sheet-quote/trmnlp-pull.yml?label=pull&style=for-the-badge&branch=main&logo=github-actions)](https://github.com/nicholaswilde/trmnl-google-sheet-quote/actions/workflows/trmnlp-pull.yml)

A private plugin for [TRMNL](https://trmnl.com/) to display quotes from a Google Sheet.

![sheet-quote](https://raw.githubusercontent.com/nicholaswilde/trmnl-sheet-quote/refs/heads/main/src/img/screenshot.png)

## :rocket: Features

-   Displays a random quote from a Google Sheet.
-   Customizable polling interval to fetch new quotes (default: 1 hour).
-   Configurable columns for quote and author.
-   Robust error handling with on-screen feedback.

## :hammer_and_wrench: Installation

1.  Clone this repository to your local machine.
2.  Copy the `src` directory to your TRMNL plugins directory.
3.  Rename the `src` directory to `sheet-quote`.

## :gear: Configuration

Configuration is handled within the TRMNL application. After installing the plugin, you will find the following settings:

-   **Spreadsheet ID**: The ID of your Google Sheet.
-   **Quote Column Index**: The column number (starting from 0) for the quotes in your sheet.
-   **Author Column Index**: The column number (starting from 0) for the authors in your sheet.

For more detailed instructions, please see the [TRMNL documentation](https://help.usetrmnl.com/en/articles/11400219-using-google-sheets-with-private-plugins).

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

### Linting
This project uses Shopify's **Theme Check** to lint the Liquid template files and verify best practices.
*   **VS Code**: Install the official **Shopify Liquid** extension to view linting warnings and syntax validation directly in your editor.
*   **CLI**: If you have Shopify CLI installed, run:
    ```bash
    shopify theme check
    ```

## :balance_scale: License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## :pencil:​ Author

​This project was started in 2025 by [Nicholas Wilde][2].

[2]: <https://github.com/nicholaswilde/>
