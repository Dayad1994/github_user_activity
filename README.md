# 🚀 GitHub User Activity CLI

> A fast and minimal command-line tool to fetch and display a user's recent activity from the GitHub Events API.  
> 📌 Inspired by [a project idea from roadmap.sh](https://roadmap.sh/projects/github-user-activity).

---

## ✨ Features

- 🔍 Retrieves recent public activity of any GitHub user  
- 🖥️ Simple terminal output  
- ⚡ Lightweight and quick to install  
- 💾 JSON-based local cache for fetched data  

---

## 📁 Project Structure

```
./
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── src/gua/
│   ├── __init__.py
│   ├── fetcher.py        # Handles GitHub API requests
│   ├── handlers.py       # Event formatting helpers
│   ├── main.py           # CLI entry point
│   ├── module.py         # Event parsing and grouping
│   ├── typing.py         # Type definitions
│   └── view.py           # Terminal output logic
└── tests/
    ├── test_fetcher.py
    └── test_module.py
```

---

## 📦 Installation

> **Requires Python 3.13 or newer**

### 1. Install `pipx`  
_pipx_ lets you install and run Python CLI tools in isolated environments:

```bash
python3 -m pip install pipx
```

### 2. Install the project:

```bash
pipx install git+https://github.com/dayanik/github_user_activity.git
```

### 3. Create a working directory (recommended):

To avoid clutter, run the tool from a separate folder — it creates a local JSON database file:

```bash
mkdir github_user_activity
cd github_user_activity
```

---

## 🛠️ Usage

Run the CLI tool from anywhere using:

```bash
gua <github_username>
```

Example:

```bash
gua dayanik
```

---

## 🧪 Development

In the project directory, create a virtual environment and install the project in editable mode:

```bash
uv venv
```

> `uv` is a fast Python package manager compatible with `pip` and `venv`.

---

## 📋 Requirements

- 🐍 Python 3.13+
- 🔗 requests >= 2.32.4

---

## ✅ Testing

Run tests using:

```bash
python -m pytest
```

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.

---

## 👤 Author

- [Dayan Iskhakov](https://github.com/dayanik)
