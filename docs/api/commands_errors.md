# commands.errors – Error Handling

Custom exception classes and a centralized `ErrorHandler` for the command
architecture. Exceptions carry an exit `code` so that handlers can fail
fast while still producing a meaningful process exit status.

Exception hierarchy (all subclass `PytigonError`):

- `ConfigurationError` — missing/invalid configuration (code 40–49)
- `SecurityError` — disallowed operation (code 60–69)
- `CommandError` — generic command failure (code 70–79)
- `SubprocessError` — subprocess failed (code 80–89)
- `PathError` — path resolution failed (code 50–54)
- `ValidationError` — input validation failed (code 90–99)
- `ResourceError` — resource unavailable (code 100–109)

::: pytigon.commands.errors
    options:
      show_submodules: true
      members: true
