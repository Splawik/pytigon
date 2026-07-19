# commands – Command Architecture

Refactored command handling architecture for the pytigon CLI.
Provides a priority-ordered handler chain with centralized error handling.

Top-level exports:

- `CommandDispatcher` — iterates registered handlers, dispatches `argv` to
  the first handler whose `can_handle(argv)` returns `True`.
- `CommandRegistry` — default handler registry, populated at import time
  with all built-in handlers.

::: pytigon.commands
    options:
      show_submodules: false
      members: true
