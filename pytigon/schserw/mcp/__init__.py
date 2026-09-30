"""Public API for the Pytigon MCP layer.

Everything here is gated on ``settings.MCP_SERVER``:

* when enabled, the real registry (backed by the ``mcp`` library) is exposed;
* when disabled, ``tool`` is a no-op decorator and ``MCPToolset`` is a plain
  base class, so application code may import them unconditionally without
  requiring the ``mcp`` package.

Import order matters. ``tool`` and ``MCPToolset`` are *objects* bound at import
time, so which of the two implementations callers get is frozen by then. This
module must therefore be imported after Django settings are configured - in
practice from ``AppConfig.ready()`` or from application code, never at the top
of ``settings.py``. If it is imported too early, the no-op variants are
installed and :func:`get_mcp_server` raises with an explanation rather than
silently behaving as if MCP were switched off.
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

    def _explain_why_disabled():
        """Build the message for a get_mcp_server() call with MCP off."""
        if not settings.configured:
            return (
                "pytigon.schserw.mcp was imported before Django settings were "
                "configured, so the no-op API was installed. Import it after "
                "django.setup()."
            )
        if getattr(settings, "MCP_SERVER", False):
            return (
                "settings.MCP_SERVER is enabled but pytigon.schserw.mcp was "
                "imported too early, so the no-op API was installed."
            )
        return "MCP_SERVER is not enabled."

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
        raise RuntimeError(f"Cannot build the MCP server: {_explain_why_disabled()}")

    def get_current_user():  # pragma: no cover
        return None

    def init():  # pragma: no cover
        pass
