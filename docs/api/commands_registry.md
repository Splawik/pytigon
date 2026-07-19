# commands.registry – CommandRegistry

Registry that maps command names to handler instances, supporting
priority-ordered handler lookup. Handlers are registered at import time;
custom handlers can be appended via `register(handler, priority=...)`.

::: pytigon.commands.registry
    options:
      show_submodules: false
      members: true
