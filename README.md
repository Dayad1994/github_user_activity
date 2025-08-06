# GitHub User Activity CLI

A fast and minimal command-line tool to fetch and display a user's recent activity from the GitHub Events API.

## Features

- Retrieves recent public activity of any GitHub user
- Simple terminal output
- Lightweight and quick to install
- JSON-based local cache for fetched data

## Project Structure

```
./
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── src/gua/
|   ├── __init__.py
|   ├── fetcher.py        # Handles GitHub API requests
|   ├── handlers.py       # Event formatting helpers
|   ├── main.py           # CLI entry point
|   ├── module.py         # Event parsing and grouping
|   ├── typing.py         # Type definitions
|   └── view.py           # Terminal output logic
└── tests/
    ├── test_fetcher.py
    └── test_module.py
```

## Installation

Requires Python 3.13 or newer to be installed.

1. Install **pipx**:

   _pipx_ is a tool to install and run Python CLI apps in isolated environments. It lets you globally install Python-based command-line tools without affecting system or project environments.

```bash
   python3 -m pip install pipx
```

2. Install project:

```bash
    pipx install git+https://github.com/dayanik/github_user_activity.git
```

3. Create a directory for the project and navigate into it:

The application creates a JSON-based database file upon launch. To avoid cluttering your working directory, it's recommended to run it from a separate folder.

```bash
    mkdir github_user_activity
    cd github_user_activity
```

## Usage

If installed via `pipx`, you can run the app from anywhere using:

```bash
tasker <github_username>
```

Example:

```bash
gua dayanik
```

## Development

In the project directory, create a virtual environment and install the project in editable mode. I recommend using the uv package manager.

```bash
    uv venv
```

**uv** is a fast Python package manager compatible with pip and venv.

## Requirements

- Python 3.13 or higher
- requests 2.32.4 or higher

## Testing

Run tests with:

```bash
python -m pytest
```

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Authors

- [Dayan Iskhakov](https://github.com/dayanik)