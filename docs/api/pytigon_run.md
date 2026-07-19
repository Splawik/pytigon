# pytigon_run – CLI Runner and Command Dispatcher

Main entry point for Pytigon CLI commands. Dispatches `argv` to the
priority-ordered handler chain in `pytigon.commands`.

Handled command prefixes:

- `manage_<app>` — Django management commands
- `runserver_<app>` — WSGI/ASGI web server
- `run_<app>.<script>` — run a project script
- `python_<app>` — launch the Python interpreter in the app context
- `pip_<app>` — install packages into the app's `prjlib`
- `init_<app>` — initialise a new project
- `@<tool>` — invoke bundled tools (zig, nim, nimble)

Global flags processed at import time: `--dev` (local project paths) and
`--script-mode` (script-friendly defaults).

::: pytigon.pytigon_run
    options:
      show_submodules: false
      members: true
