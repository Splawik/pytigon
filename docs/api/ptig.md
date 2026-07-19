# ptig – Ptig Package Installer / Console Entry

Console entry point installed as the `ptig` command. Provides:

- `init(prj_name)` — initialise a new pytigon project (wraps
  `pytigon_run.run(["ptig", f"init_{prj_name}"])`)
- `main()` — invoked by the `ptig` console script; forwards `sys.argv` to
  `pytigon_run.run()`

The `Ptig` archive installer class itself lives in
`pytigon_lib.schtools.install` and handles `.ptig` extraction and deployment.

::: pytigon.ptig
    options:
      show_submodules: false
      members: true
