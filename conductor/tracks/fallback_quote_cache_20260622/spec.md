# Specification - Fallback Offline Quote Cache

## Overview
This track implements a fallback offline quote cache in the Liquid/Javascript templates of the TRMNL Google Sheet Quote plugin. If the Google Sheet CSV data cannot be fetched, is empty, or encounters errors, the plugin will seamlessly fall back to displaying a randomized quote from a local pre-defined cache, ensuring the screen is never blank or showing a generic error code.

## Functional Requirements
- **Fallback Quote Cache:** Hardcode a collection of at least 5 polite, inspirational fallback quotes and their authors.
- **Trigger Conditions:** Use the fallback cache when:
  - The fetched `data` payload is null or empty.
  - The rows are empty.
  - An exception is thrown during parsing or processing.
- **Graceful Error Recovery:** Instead of showing "No data found. Check Spreadsheet ID." or raw Javascript error details, display a fallback quote.
- **Consistency across Layouts:** The fallback mechanism must be implemented consistently in all four Liquid layouts:
  - `full.liquid`
  - `half_horizontal.liquid`
  - `half_vertical.liquid`
  - `quadrant.liquid`

## Non-Functional Requirements
- **Performance:** Fallback rendering should be instantaneous, without external requests.
- **Aesthetics:** The visual display of fallback quotes must match the standard layout and styling of fetched quotes.
- **Logging:** Log warnings to the console when fallback mode is active to assist with developer/user troubleshooting.

## Acceptance Criteria
- [ ] Liquid templates detect empty or invalid sheet data payloads.
- [ ] Fallback cache array is defined in all layout files.
- [ ] A random quote and author from the fallback cache are rendered if data is unavailable.
- [ ] No raw developer-facing error messages are visible on the screen.
- [ ] Local preview server renders fallback content correctly when no data is supplied.

## Out of Scope
- Fetching fallback quotes from an alternate web API.
- Storing user-defined fallback quotes in a local file.
