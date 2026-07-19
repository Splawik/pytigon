# ext_lib – Bundled External Libraries

Third-party and utility libraries vendored with pytigon. Each module is
self-contained and imported only when needed:

| Module | Purpose |
|--------|---------|
| `autocomplete` | wxPython autocomplete listbox widget |
| `naivehtmlparser` | Fallback HTML parser used when `lxml` is unavailable |
| `pygettext` | Gettext message extraction (vendored from CPython tools) |
| `wxasync` | Bridge between wxPython's event loop and `asyncio` |

::: pytigon.ext_lib
    options:
      show_submodules: true
      members: true
