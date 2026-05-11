# Overview

## What is Pytigon?

Pytigon is a Python application framework that combines **wxPython** desktop GUI
capabilities with a **Django** web backend. The `pytigon` package provides the
CLI entry point, command architecture, and runtime infrastructure.

## Architecture

```
pytigon/
├── pytigon_run.py        # Main CLI dispatcher (~650 lines)
├── pytigon_request.py    # Embedded Django HTTP client
├── pytigon_task.py       # Twisted-based task scheduler
├── django_min_init.py    # Lightweight Django initialization
├── manage.py             # Django manage.py bridge
├── ptig.py               # Ptig archive installer
├── commands/             # Command dispatching architecture
│   ├── dispatcher.py     # CommandDispatcher class
│   ├── registry.py       # CommandRegistry class
│   ├── handlers/         # Command handler implementations
│   ├── errors/           # Error handling (exceptions, handler)
│   └── utils/            # Path/subprocess utilities
└── ext_lib/              # Bundled external libraries
```

## CLI Command Patterns

Pytigon uses prefixed CLI commands to route operations:

| Pattern | Example | Handler |
|---------|---------|---------|
| `manage_<app>` | `pytigon manage_mydb migrate` | ManageCommandHandler |
| `runserver_<app>` | `pytigon runserver_myapp --port 8080` | RunServerCommandHandler |
| `run_<app>.<script>` | `pytigon run_myapp.daily_report` | RunCommandHandler |
| `python_<app>` | `pytigon python_myapp script.py` | PythonCommandHandler |
| `pip_<app>` | `pytigon pip_myapp install requests` | PipCommandHandler |
| `init_<app>` | `pytigon init_myapp` | InitCommandHandler |
| `--dev` | `pytigon --dev manage_dev test` | (developer mode flag) |

## Dependencies

- **Core:** Python 3.10+
- **Django:** Django 4.x+ (for embedded server)
- **Web server:** Daphne (ASGI) or Waitress (WSGI)
- **Task scheduling:** Twisted
- **Desktop GUI:** wxPython (optional, for GUI mode)
- **Android:** Kivy (optional)
