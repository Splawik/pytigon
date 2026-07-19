# pytigon_task – Task Scheduler Entry Point

Runs scheduled tasks defined by pytigon application modules using the
Twisted-based `SChScheduler`. Supports direct view invocation (via the
embedded HTTP client) and background task execution.

Schedule helpers come from `pytigon_lib.schtasks.schschedule`:
`daily`, `hourly`, `monthly`, `in_minute_intervals`, `in_second_intervals`.
Tasks may be coroutines — the scheduler awaits them with `asyncio.wait`.

::: pytigon.pytigon_task
    options:
      show_submodules: false
      members: true
