# Raindrop.io CSV to Zettelkasten-based Markdown

A Python CLI tool to parse a CSV export from Raindrop.io and create a directory of individual markdown files - one per bookmark - using Zettelkasten-style filenames.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Template](#template-system)
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

## Template System

This tool supports user-editable markdown templates for generating bookmark notes. Templates are written using the [Jinja2](https://jinja.palletsprojects.com/) templating language and must follow these conventions:

### Template File Requirements
- Templates must be placed in the `templates/` directory and have the `.md.j2` extension (e.g., `bookmark_template.md.j2`).
- The template filename is used as its identifier and is referenced in the YAML frontmatter of each generated note.

### Template Syntax
- Use Jinja2 variable syntax for bookmark fields, e.g. `{{ title }}`, `{{ url }}`, `{{ tags }}`.
- Standard bookmark fields available:
  - `title`, `url`, `cover`, `tags`, `created`, `favorite`, `excerpt`, `note`, `highlights`
- You may define additional user sections by adding new variables (e.g., `{{ user_notes }}`) in the template. These will be preserved and editable in the CLI.
- To render highlights as a list, use a Jinja2 loop:
  ```jinja
  {% if highlights %}
  ### Highlights:
  {% for h in highlights %}
  > {{ h }}
  {% endfor %}
  {% endif %}
  ```
- You can use any valid Jinja2 syntax for formatting, conditionals, and loops.

### YAML Frontmatter
- Each generated note includes YAML frontmatter indicating the template used:
  ```yaml
  ---
  template: bookmark_template.md.j2
  ---
  ```
- The tool uses this field to ensure the correct template is used for editing and parsing.

### Example Template
```
## [{{ title }}]({{ url }})
{% if cover %}![cover image]({{ cover }}){% endif %}
**Tags:** {{ tags }}
**Created:** {{ created }}
{% if favorite %}⭐ **Favorite**{% endif %}
{% if excerpt %}
_Excerpt:_ {{ excerpt }}
{% endif %}
{% if note %}
_Note:_ {{ note }}
{% endif %}
{% if highlights %}
### Highlights:
{% for h in highlights %}
> {{ h }}
{% endfor %}
{% endif %}
```

### User-Defined Sections
- Any variable in the template that is not a standard bookmark field is treated as a user-defined section (e.g., `{{ user_notes }}`).
- The CLI will prompt for these sections when creating or editing notes, and will preserve their content on update.

### Template Best Practices
- Use clear section headers (e.g., `### Notes`) for user-defined sections.
- Avoid duplicate variable names.
- Test your template with a sample bookmark to ensure all fields render as expected.

See the `templates/` directory for working examples.


## TODOs
- [x] Improve CLI output
- [x] Add markdown template customization
- [ ] Improve bookmark editing
- [ ] Add Raindrop API use to automate CSV export

## License
This project is licensed under the MIT License.

