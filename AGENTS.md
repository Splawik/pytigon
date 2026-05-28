# Pytigon Development Guide

## Project Overview

Pytigon is a Django-based application framework by Sławomir Chołaj (LGPLv3).
It bridges Python + Django + wxWidgets for desktop and web applications.

## Quick Commands

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests -v

# Run specific test
pytest tests/test_commands_dispatcher.py -v

# Run tests (via invoke)
invoke test

# Lint code
ruff check pytigon tests
invoke lint

# Format code
ruff format pytigon tests
invoke format

# Type check
mypy pytigon --ignore-missing-imports
invoke typecheck

# Build static assets (Python→JS, SASS→CSS)
python make.py
invoke build

# Build only JavaScript
invoke build-js

# Build only CSS
invoke build-css

# Build templates
invoke build-templates

# Clean build artifacts
invoke clean

# List all tasks
invoke -l

# Run Django management commands
python pytigon/manage.py <command>
```

## Architecture

- `pytigon/` - Main application package
  - `commands/` - CLI command dispatcher (Chain of Responsibility pattern)
  - `schserw/` - Django server core (settings, URLs, views, middleware)
  - `schserw/settings/` - Modular Django settings (base, features, infra)
  - `ext_lib/` - Bundled third-party extensions
  - `static/` - Compiled frontend assets
  - `templates/` - Compiled Django templates
- `tests/` - Pytest test suite
- `pytigon_gui/` - External wxPython GUI package (symlink)
- `pytigon_lib/` - External shared library (symlink)

## Settings

The Django settings are split into modules:
- `pytigon/schserw/settings/base.py` - Core settings (paths, database, i18n)
- `pytigon/schserw/settings/features.py` - Installed apps, middleware, feature flags
- `pytigon/schserw/settings/infra.py` - Logging, storage, channels, integrations

## Code Style

- Python 3.10+ compatible
- Line length: 100 characters
- Use ruff for linting and formatting
- Docstrings in Google-style format
- Import order: standard library → third-party → local

## Testing

- Framework: pytest with pytest-django
- Test config: `tests/conftest.py` (in-memory SQLite)
- Excluded: `pytigon/prj/`, `pytigon_gui/`, `pytigon_lib/`
- Run: `pytest tests -v`

## Configuration Files

- `pyproject.toml` - Build system, linting, formatting, test config
- `pytest.ini` - Legacy pytest config
- `.pre-commit-config.yaml` - Git hooks
- `.github/workflows/ci.yml` - CI pipeline
