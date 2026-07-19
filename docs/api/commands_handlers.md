# commands.handlers – Command Handlers

Implementations of command handlers for each CLI command pattern:
`manage`, `run`, `runserver`, `python`, `pip`, `init`, `tools` (@-prefixed),
and a `default` catch-all.

Each handler subclasses `CommandHandler` and implements:

- `can_handle(argv) -> bool` — claim the command
- `execute(argv, **kwargs) -> int` — run it, returning an exit code

Common helpers (path setup, subprocess execution, error wrapping) come from
`commands.utils` and `commands.errors`.

::: pytigon.commands.handlers
    options:
      show_submodules: true
      members: true
