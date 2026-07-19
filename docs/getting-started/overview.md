# Overview

## What is Pytigon?

Pytigon is a Python application framework that combines a **Django** web
backend with an optional **wxPython** desktop GUI. The `pytigon` package
provides the CLI entry point, command architecture, embedded Django server,
HTTP client, and task scheduler.

The framework is split across three packages that cooperate at runtime:

| Package | Role |
|---------|------|
| `pytigon` | Application framework — CLI, command dispatcher, embedded server |
| `pytigon_lib` | Core library — iHTML, document rendering, table abstraction, HTTP client |
| `pytigon_gui` | wxPython desktop client (optional) |

## Architecture

```
pytigon/
├── pytigon_run.py        # Main CLI dispatcher
├── pytigon_request.py    # Embedded Django HTTP client
├── pytigon_task.py       # Twisted-based task scheduler
├── django_min_init.py    # Lightweight Django initialization
├── manage.py             # Django manage.py bridge
├── ptig.py               # ptig console entry point
├── __main__.py           # `python -m pytigon` entry
├── commands/             # Command dispatching architecture
│   ├── dispatcher.py     # CommandDispatcher class
│   ├── registry.py       # CommandRegistry class
│   ├── handlers/         # Command handler implementations
│   │   ├── base.py       # Base CommandHandler
│   │   ├── default.py    # Catch-all handler
│   │   ├── init.py       # init_<app> handler
│   │   ├── manage.py     # manage_<app> handler
│   │   ├── pip.py        # pip_<app> handler
│   │   ├── python.py     # python_<app> handler
│   │   ├── run.py        # run_<app> handler
│   │   ├── runserver.py  # runserver_<app> handler
│   │   └── tools.py      # @zig / @nim / @nimble tool commands
│   ├── errors/           # Custom exceptions + ErrorHandler
│   │   ├── exceptions.py
│   │   └── handler.py
│   ├── utils/            # Path + subprocess utilities
│   │   ├── paths.py
│   │   └── subprocess.py
│   └── config/           # Configuration files
├── schserw/              # Django server extensions (embedded app)
│   ├── urls.py           # Root URL conf
│   ├── routing.py        # Channels (WebSocket) routing
│   ├── settings/         # Layered Django settings (base/features/infra)
│   ├── schsys/           # System app: auth, context processors, template tags
│   │   ├── app_manager.py
│   │   ├── context_processors.py
│   │   ├── initdjango.py        # Runtime monkey-patches for Django
│   │   ├── schema.py            # GraphQL schema helpers
│   │   └── templatetags/        # exsyntax, exfiltry — UI template tags
│   ├── schmiddleware/    # JWT, post logging, vary, etc.
│   └── oauth2_ext/       # OAuth2 extensions
├── appdata/              # Plugins, install assets, source assets
│   ├── plugins/standard/ # Bundled plugins (editor, hexview, shell, webview…)
│   ├── install/          # install.ini template
│   ├── icss/             # Indented CSS sources
│   └── plugins_src/      # Plugin sources before build
├── static_src/           # Frontend sources
│   └── pytigon_js/       # Python→JS (pscript) frontend runtime
├── ext_lib/              # Bundled external libraries
│   ├── autocomplete.py   # wxPython autocomplete widget
│   ├── naivehtmlparser.py # Fallback HTML parser (no lxml)
│   ├── pygettext.py      # Gettext message extraction (vendored)
│   └── wxasync.py        # wxPython + asyncio bridge
├── templates/            # Built Django templates
├── templates_src/        # iHTML template sources (compiled to templates/)
└── static/               # Built static assets
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
| `@<tool>` | `ptig @zig build` | ToolsCommandHandler |
| `--dev` | `ptig --dev manage_dev test` | Developer-mode flag (local paths) |
| `--script-mode` | `ptig --script-mode python_myapp tool.py` | Script-friendly defaults |

## Runtime Modes

Pytigon adapts its runtime to the host environment:

| Mode | Trigger | Behaviour |
|------|---------|-----------|
| **GUI** | `runserver_<app>` without `--nogui` | Launches the wxPython desktop client |
| **Web server (WSGI)** | `runserver_<app> --wsgi` | Waitress serving Django on `127.0.0.2` |
| **Web server (ASGI)** | `runserver_<app>` (default) | Daphne serving Django + Channels |
| **Headless task runner** | `pytigon_task` entry | Twisted reactor + `SChScheduler` |
| **Embedded** | `pytigon_request.init(...)` | In-process Django on `127.0.0.2` |
| **Android** | Kivy launcher | WebView/Kivy host wrapping the web server |

## Dependencies

- **Core:** Python 3.12+
- **Web framework:** Django 6.x+
- **ASGI server:** Daphne (default); **WSGI:** Waitress (optional)
- **Task scheduling:** Twisted
- **Desktop GUI:** wxPython 4.x (optional — only for GUI mode)
- **Android:** Kivy (optional, for the mobile wrapper)
- **Frontend:** pscript (Python→JS), bundled JS runtime in `static/`
- **Templating:** lxml (preferred) with a fallback `naivehtmlparser`
- **Auth (optional):** django-allauth for OAuth/social login
- **Realtime (optional):** Django Channels for WebSocket consumers
