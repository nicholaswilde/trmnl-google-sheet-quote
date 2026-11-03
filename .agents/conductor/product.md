# Initial Concept
A private plugin for TRMNL to display quotes from a Google Sheet.

# Product Definition

## Target Audience
The primary users are individuals who own a TRMNL device and wish to personalize their display with meaningful content. These users typically maintain a curated collection of quotes, affirmations, or reminders in a Google Sheet and want a seamless way to rotate this content on their TRMNL screen.

## Core Goals
- **Inspiration & Motivation:** Provide a random daily or interval-based quote to inspire the user.
- **Ease of Use:** Offer a simple configuration process using standard Google Sheet IDs and column indices.
- **Customization:** Allow users to define which columns represent the quote and the author, ensuring flexibility with existing sheet structures.

## Key Features
- **Dynamic Fetching:** Automatically retrieves data from a specified Google Sheet.
- **Randomization:** Selects a random entry from the provided spreadsheet to keep the content fresh.
- **Multi-Layout Support:** Provides liquid templates for various TRMNL display sizes (Full, Half Horizontal, Half Vertical, Quadrant).
- **Flexible Configuration:** Settings for Spreadsheet ID, Quote Column Index, Author Column Index, Text Alignment (Center, Left, Right), and option to hide the bottom title bar to maximize presentation area.
- **Offline Fallback Caching:** Automatically displays a randomized quote from a local pre-defined cache if the Google Sheet CSV data is empty or fails to fetch, ensuring the display remains resilient and elegant.