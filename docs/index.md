# Pytigon Application

**Version:** 0.260714 · **License:** LGPL 3.0 · **Author:** Sławomir Chołaj

---

## Overview

Pytigon is a Python application framework that combines a **Django** web
backend with an optional **wxPython** desktop GUI. The `pytigon` package is
the application tier: it provides the `ptig` CLI, a command-dispatching
architecture, an embedded Django runtime, an HTTP client for in-process
requests, and a Twisted-based task scheduler.

Pytigon is distributed as three cooperating packages:

| Package | Role |
|---------|------|
| [`pytigon`](api/pytigon.md) | Application framework: CLI, command dispatcher, embedded Django server, task scheduler |
| `pytigon_lib` | Core library: iHTML templating, document rendering (PDF/DOCX/XLSX), table abstraction, HTTP client, scheduling primitives |
| `pytigon_gui` | wxPython desktop client (optional): HTML widget, grid controls, toolbars, native forms |

A typical install pulls in all three. The GUI is optional — pytigon can run
headless as a CLI, embedded server, or background task runner.

## Module Map

| Module | Purpose |
|--------|---------|
| [`pytigon_run`](api/pytigon_run.md) | Main CLI runner — `manage_*`, `runserver_*`, `run_*`, `python_*` commands |
| [`pytigon_request`](api/pytigon_request.md) | Embedded Django HTTP client initialization and helpers |
| [`pytigon_task`](api/pytigon_task.md) | Scheduled task execution with Twisted-based scheduler |
| [`django_min_init`](api/django_min_init.md) | Lightweight Django setup for scripts/embedded use |
| [`manage`](api/manage.md) | Django `manage.py` entry point within pytigon paths |
| [`ptig`](api/ptig.md) | `ptig` console entry — project init and command launch |
| [`commands`](api/commands.md) | Refactored command dispatching architecture |
| [`ext_lib`](api/ext_lib.md) | Bundled external libraries (autocomplete, naive HTML parser, gettext, wx async) |

## Quick Start

```python
# Minimal Django setup (no DB, no middleware) for scripts
from pytigon.django_min_init import init
init("schscripts")

# Embedded HTTP client — talk to pytigon's in-process Django server
from pytigon.pytigon_request import init, request
init("myapp", username="admin", password="secret")
resp = request("/api/data/")

# CLI entry (equivalent to running `ptig` from the shell)
from pytigon.pytigon_run import run
run()
```

## CLI Command Patterns

Pytigon routes CLI commands by prefix:

| Pattern | Example | Handler |
|---------|---------|---------|
| `manage_<app>` | `ptig manage_mydb migrate` | ManageCommandHandler |
| `runserver_<app>` | `ptig runserver_myapp --port 8080` | RunServerCommandHandler |
| `run_<app>.<script>` | `ptig run_myapp.daily_report` | RunCommandHandler |
| `python_<app>` | `ptig python_myapp script.py` | PythonCommandHandler |
| `pip_<app>` | `ptig pip_myapp install requests` | PipCommandHandler |
| `init_<app>` | `ptig init_myapp` | InitCommandHandler |
| `@<tool>` | `ptig @zig build` | ToolsCommandHandler |

The `--dev` flag switches project path resolution to the local checkout,
and `--script-mode` enables script-friendly defaults.

## Key Design Patterns

- **Command Dispatcher** — priority-ordered handler chain; each handler
  decides whether it can handle `argv`, and the first match wins.
- **Embedded Django** — a lightweight `django_min_init.init()` boots Django
  without `manage.py`, suitable for GUI and script contexts.
- **In-process HTTP** — `pytigon_request` drives an embedded Django server
  on `127.0.0.2` and exposes a small `init()` / `request()` API.
- **Task Scheduler** — `SChScheduler` runs coroutines on a Twisted reactor
  with an optional XML-RPC control port.
- **Ptig Archives** — compressed project snapshots (`.ptig`) for deployment
  via the `Ptig` installer.
