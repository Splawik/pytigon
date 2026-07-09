# Overview

## What is Pytigon?

Pytigon is a Python application framework that combines **wxPython** desktop GUI
capabilities with a **Django** web backend. The `pytigon` package provides the
CLI entry point, command architecture, and runtime infrastructure.

## Architecture

```
pytigon/
├── pytigon_run.py        # Main CLI dispatcher (~89 lines)
├── pytigon_request.py    # Embedded Django HTTP client
├── pytigon_task.py       # Twisted-based task scheduler
├── django_min_init.py    # Lightweight Django initialization
├── manage.py             # Django manage.py bridge
├── ptig.py               # CLI entry point (ptig command)
├── commands/             # Command dispatching architecture
│   ├── dispatcher.py     # CommandDispatcher class
│   ├── registry.py       # CommandRegistry class
│   ├── handlers/         # Command handler implementations
│   │   ├── base.py       # Base CommandHandler class
│   │   ├── default.py    # Default (catch-all) handler
│   │   ├── init.py       # init_<app> handler
│   │   ├── manage.py     # manage_<app> handler
│   │   ├── pip.py        # pip_<app> handler
│   │   ├── python.py     # python_<app> handler
│   │   ├── run.py        # run_<app> handler
│   │   ├── runserver.py  # runserver_<app> handler
│   │   └── tools.py      # Tool commands (zig, nim, nimble)
│   ├── errors/           # Error handling
│   │   ├── exceptions.py # Custom exception classes
│   │   └── handler.py    # ErrorHandler class
│   ├── utils/            # Path/subprocess utilities
│   │   ├── paths.py      # Path resolution utilities
│   │   └── subprocess.py # Safe subprocess execution
│   └── config/           # Configuration files
└── ext_lib/              # Bundled external libraries
    ├── autocomplete.py   # Autocomplete engine
    ├── naivehtmlparser.py # Simple HTML parser
    ├── pygettext.py      # Gettext message extraction
    └── wxasync.py        # wxPython async helpers
```

## CLI Command Patterns

Pytigon uses prefixed CLI commands to route operations:

| Pattern | Example | Handler |
|---------|---------|---------|
| `manage_<app>` | `ptig manage_mydb migrate` | ManageCommandHandler |
| `runserver_<app>` | `ptig runserver_myapp --port 8080` | RunServerCommandHandler |
| `run_<app>.<script>` | `ptig run_myapp.daily_report` | RunCommandHandler |
| `python_<app>` | `ptig python_myapp script.py` | PythonCommandHandler |
| `pip_<app>` | `ptig pip_myapp install requests` | PipCommandHandler |
| `init_<app>` | `ptig init_myapp` | InitCommandHandler |
| `--dev` | `ptig --dev manage_dev test` | (developer mode flag) |

## Dependencies

- **Core:** Python 3.12+
- **Django:** Django 6.x+ (for embedded server)
- **Web server:** Daphne (ASGI) or Waitress (WSGI)
- **Task scheduling:** Twisted
- **Desktop GUI:** wxPython (optional, for GUI mode)
- **Android:** Kivy (optional)
