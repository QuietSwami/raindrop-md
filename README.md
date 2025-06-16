# Raindrop.io CSV to Zettelkasten-based Markdown

A Python CLI tool to parse a CSV export from Raindrop.io and create a directory of individual markdown files - one per bookmark - using Zettelkasten-style filenames.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Future Enhancements](#future-enhancements)
- [License](#license)


## Features
- Parses Raindrop.io CSV exports
- Extracts bookmarks and highlights
- Creates a directory of markdown files (one per bookmark)
- Zettelkasten-style filenames: `{YYYYMMDDHHMM}_{title}.md`
- Interactive CLI to show, edit, remove, and search bookmarks in the directory
- Fuzzy search across all bookmarks
- Robust error handling and logging
- Comprehensive unit tests

## Requirements
- Python 3.8+

## Installation

1. Clone the repository:
   ```sh
   git clone <repository-url>
   ```

2. Navigate to the project directory
   ```sh
   cd <project-directory>
   ```

3. (Optional) Create and activate a virtual environment
   ```sh
   python -m venv venv
   source venv/bin/activate # On Windows, use `venv\Scripts\activate`
   ```

## Usage
1. Place your Raindrop.io CSV export anywhere on your system.
2. Run the script to create a directory of markdown files:
   ```sh
   python raindropMD.py create <your_csv_file.csv> <output_directory>
   ```
   Example:
   ```sh
   python raindropMD.py create ~/Downloads/raindrop.csv bookmarks/
   ```
3. Use the CLI to manage your bookmarks:
   - List all bookmarks:
     ```sh
     python raindropMD.py list <output_directory>
     ```
   - Edit a bookmark interactively:
     ```sh
     python raindropMD.py edit <output_directory>
     ```
   - Remove a bookmark interactively:
     ```sh
     python raindropMD.py remove <output_directory>
     ```
   - Fuzzy search bookmarks:
     ```sh
     python raindropMD.py search <output_directory> <query>
     ```

## TODOs
- [x] Improve CLI output
- [ ] Add markdown template customization
- [ ] Improve bookmark editing
- [ ] Add Raindrop API use to automate CSV export

## License
This project is licensed under the MIT License.

