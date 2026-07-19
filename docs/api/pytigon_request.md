# pytigon_request – Embedded Django HTTP Client

Initialization and simplified HTTP request functions for communicating with
pytigon's internal Django server (bound to `127.0.0.2`) from GUI and script
modes.

Two public functions:

- `init(prj, username=None, password=None, ...)` — boot the embedded server
  and optionally log in. A `.ptig` archive can be supplied via
  `ptig_installer` to deploy a project before init.
- `request(url, params=None)` — issue a GET (when `params` is `None`) or a
  POST against the embedded server. Raises `RuntimeError` if `init()` has
  not been called.

::: pytigon.pytigon_request
    options:
      show_submodules: false
      members: true
