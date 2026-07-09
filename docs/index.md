# Pytigon Application

**Version:** 0.260706 · **License:** LGPL 3.0 · **Author:** Sławomir Chołaj

---

## Overview

Pytigon is a Python application framework combining **wxPython** desktop GUI
capabilities with a **Django** web backend. This package provides the CLI entry
point, command architecture, Django initialization, HTTP client helpers, and
task scheduling infrastructure.

## Module Map

| Module | Purpose |
|--------|---------|
| [`pytigon_run`](api/pytigon_run.md) | Main CLI runner – `manage_*`, `runserver_*`, `run_*`, `python_*` commands |
| [`pytigon_request`](api/pytigon_request.md) | Embedded Django HTTP client initialization and helpers |
| [`pytigon_task`](api/pytigon_task.md) | Scheduled task execution with Twisted-based scheduler |
| [`django_min_init`](api/django_min_init.md) | Lightweight Django setup for scripts/embedded use |
| [`manage`](api/manage.md) | Django `manage.py` entry point within pytigon paths |
| [`ptig`](api/ptig.md) | Ptig package installer – archive extraction and deployment |
| [`commands`](api/commands.md) | Refactored command dispatching architecture |
| [`ext_lib`](api/ext_lib.md) | Bundled external libraries (autocomplete, HTML parser, i18n, wx async) |

## Quick Start

```python
# Programmatic usage
from pytigon.django_min_init import init
init("schscripts")

# Embedded HTTP client
from pytigon.pytigon_request import init, request
init("myapp", username="admin", password="secret")
resp = request("/api/data/")

# CLI entry
from pytigon.pytigon_run import run
run()
```

## Key Design Patterns

- **Command Dispatcher** – priority-ordered handler chain for CLI routing
- **Embedded Django** – lightweight Django initialization for GUI/script modes
- **Task Scheduler** – Twisted-based background task execution with XML-RPC
- **Ptig Archives** – compressed project snapshots for deployment
