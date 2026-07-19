# commands.utils – Utilities

Path and subprocess utilities supporting the command architecture.

- `paths.py` — `setup_paths(app=None)`, `init_prj_path(...)`, executable
  lookup with security checks. Raises `PathError` on invalid or missing
  paths.
- `subprocess.py` — safe `run_subprocess(command)` wrapper that captures
  stdout/stderr and returns an exit code.

::: pytigon.commands.utils
    options:
      show_submodules: true
      members: true
