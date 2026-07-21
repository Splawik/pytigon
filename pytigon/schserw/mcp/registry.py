"""MCP server registry — the extensible layer (no Django Channels here).

This module owns the :class:`~mcp.server.FastMCP` server and the registration of
MCP tools. Adding a new MCP capability is done here (or in application code via
the public decorators) and never requires touching the Channels transport in
``pytigon.schserw.mcp.consumer``.

Two extension mechanisms are provided:

* ``@tool`` — register a standalone function as an MCP tool::

      from pytigon.schserw.mcp import tool

      @tool()
      async def echo(text: str) -> str:
          '''Echo the given text.'''
          return text

* ``MCPToolset`` — group related tools in a class. Every public method of a
  subclass becomes an MCP tool::

      from pytigon.schserw.mcp import MCPToolset

      class MathTools(MCPToolset):
          async def add(self, a: int, b: int) -> int:
              '''Add two numbers.'''
              return a + b

The public API (``tool``, ``MCPToolset``, ``get_mcp_server``) is re-exported from
``pytigon.schserw.mcp`` and is a no-op when ``settings.MCP_SERVER`` is disabled,
so application code can import it unconditionally.
"""

import contextvars
import inspect
import logging

from django.conf import settings
from mcp.server import FastMCP

logger = logging.getLogger(__name__)

_server: FastMCP | None = None
_initialized = False
_pending_tools: list[tuple] = []
_toolsets: dict[str, type] = {}

current_user: contextvars.ContextVar = contextvars.ContextVar("mcp_current_user")


def get_current_user():
    """Return the Django user associated with the active MCP connection.

    Tools may call this to access the authenticated user. Returns ``None`` when
    called outside of an MCP request (e.g. during tests).
    """
    try:
        return current_user.get()
    except LookupError:
        return None


def _server_kwargs() -> dict:
    return {
        "name": getattr(settings, "DJANGO_MCP_SERVER_NAME", "pytigon_mcp"),
        "instructions": getattr(settings, "DJANGO_MCP_INSTRUCTIONS", None) or None,
    }


def _create_server() -> FastMCP:
    return FastMCP(**_server_kwargs())


def _clean_kwargs(kwargs: dict) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None}


def _register_tool(fn, **kwargs) -> None:
    """Register a function as an MCP tool, now or once the server exists."""
    global _server
    if _server is not None and _initialized:
        _server.add_tool(fn, **_clean_kwargs(kwargs))
    else:
        _pending_tools.append((fn, kwargs))


def _register_toolset(cls: type) -> None:
    """Instantiate a toolset class and register its public methods as tools."""
    global _server
    if _server is None:
        return
    instance = cls()
    for name, method in inspect.getmembers(instance, predicate=inspect.ismethod):
        if name.startswith("_"):
            continue
        try:
            _server.add_tool(method)
        except Exception:
            logger.exception("Failed to register MCP tool %s.%s", cls.__name__, name)


def init() -> None:
    """Create the FastMCP server (if needed) and register all pending tools.

    Idempotent. Called eagerly from the app ``ready()`` hook and lazily from
    :func:`get_mcp_server`.
    """
    global _server, _initialized

    if _initialized:
        return

    if _server is None:
        _server = _create_server()

    for fn, kwargs in _pending_tools:
        try:
            _server.add_tool(fn, **_clean_kwargs(kwargs))
        except Exception:
            logger.exception("Failed to register MCP tool %s", getattr(fn, "__name__", fn))
    _pending_tools.clear()

    for cls in list(_toolsets.values()):
        _register_toolset(cls)

    _initialized = True


def get_mcp_server() -> FastMCP:
    """Return the shared :class:`FastMCP` instance, initializing it if needed."""
    if not _initialized:
        init()
    assert _server is not None
    return _server


def tool(name=None, description=None, **kwargs):
    """Decorator registering a function as an MCP tool.

    Usage: ``@tool()`` or ``@tool(name="x", description="...")``. Also supports
    the bare ``@tool`` form.

    No-op equivalent is exposed via ``pytigon.schserw.mcp`` when MCP is disabled.
    """
    if callable(name) and not isinstance(name, str) and not kwargs:
        fn = name
        _register_tool(fn)
        return fn

    def decorator(fn):
        _register_tool(fn, name=name, description=description, **kwargs)
        return fn

    return decorator


class _ToolsetMeta(type):
    """Metaclass that records ``MCPToolset`` subclasses for later registration."""

    def __init__(cls, what, bases, namespace):
        super().__init__(what, bases, namespace)
        if bases and any(isinstance(b, _ToolsetMeta) for b in bases):
            _toolsets[cls.__name__] = cls
            if _initialized:
                _register_toolset(cls)


class MCPToolset(metaclass=_ToolsetMeta):
    """Base class for grouping MCP tools.

    Every public method (name not starting with ``_``) of a subclass is
    published as an MCP tool. A subclass is instantiated once and its methods
    are registered as bound tools, so ``self`` is bound automatically and
    excluded from the tool's input schema.
    """

    pass
