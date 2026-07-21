"""Public API for the Pytigon MCP layer.

Everything here is gated on ``settings.MCP_SERVER``:

* when enabled, the real registry (backed by the ``mcp`` library) is exposed;
* when disabled, ``tool`` is a no-op decorator and ``MCPToolset`` is a plain
  base class, so application code may import them unconditionally without
  requiring the ``mcp`` package.
"""

from django.conf import settings

_MCP_ENABLED = bool(getattr(settings, "MCP_SERVER", False)) if settings.configured else False

if _MCP_ENABLED:  # pragma: no cover - exercised only in MCP-enabled setups
    from .registry import (  # noqa: F401
        MCPToolset,
        get_current_user,
        get_mcp_server,
        init,
        tool,
    )
else:

    def tool(name=None, description=None, **kwargs):
        """No-op ``@tool`` decorator used when ``MCP_SERVER`` is disabled."""

        if name is not None and callable(name) and not kwargs:
            # Used as a bare decorator without parentheses.
            return name

        def decorator(fn):
            return fn

        return decorator

    class MCPToolset:
        """No-op toolset base used when ``MCP_SERVER`` is disabled."""

        pass

    def get_mcp_server():  # pragma: no cover
        raise RuntimeError("MCP_SERVER is not enabled")

    def get_current_user():  # pragma: no cover
        return None

    def init():  # pragma: no cover
        pass
