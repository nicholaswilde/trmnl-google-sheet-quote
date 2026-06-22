# :framed_picture: TRMNL Google Sheet Quote :bar_chart:

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

This project does not have any dependencies to install or a development server to run. The plugin is designed to be used within the TRMNL application.

To make changes, edit the files in the `src` directory. The `.liquid` files control the layout, and `settings.yml` controls the configuration options.

## :balance_scale: License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## :pencil:​ Author

​This project was started in 2025 by [Nicholas Wilde][2].

[2]: <https://github.com/nicholaswilde/>
