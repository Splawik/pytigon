"""Streamable HTTP transport for the MCP server, mounted as a raw ASGI app.

This is the official MCP-over-HTTP transport (the one standard clients such as
Claude Desktop use). It is exposed as a plain ASGI application driven directly by
the ASGI server (uvicorn/daphne), so the request path stays on the event loop
with no ``async_to_sync``/``sync_to_async`` bridging — the combination that
caused the original ``django-mcp-server`` hang under ASGI.

Only this module knows about the HTTP transport; tools live in the registry
layer and can be extended without touching it.

Optional authentication: when ``settings.MCP_SERVER_PRV`` is set, the MCP
endpoint is protected with the *same* OAuth2 + JWT mechanisms already configured
for REST in ``settings`` (``REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']``
for OAuth2 and ``graphql_jwt.backends.JSONWebTokenBackend`` for JWT, both
populated by the project's REST/GRAPHQL settings). No new auth scheme is added.
When ``MCP_SERVER_PRV`` is unset the endpoint stays open (current behaviour).
"""

import logging
import posixpath

from asgiref.sync import sync_to_async
from django.conf import settings
from django.http import QueryDict
from django.utils.module_loading import import_string
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager

from .registry import current_user, get_mcp_server

logger = logging.getLogger(__name__)


def mcp_path() -> str:
    """Return the configured MCP HTTP endpoint path (e.g. ``/mcp``)."""
    root = (getattr(settings, "URL_ROOT_PREFIX", "/") or "/").strip("/")
    endpoint = (getattr(settings, "DJANGO_MCP_PATH", "mcp") or "mcp").strip("/")
    path = "/" + "/".join(p for p in (root, endpoint) if p)
    return posixpath.normpath(path)


# ---------------------------------------------------------------------------
# Authentication (only used when settings.MCP_SERVER_PRV is set)
# ---------------------------------------------------------------------------

_JWT_BACKEND_PATH = "graphql_jwt.backends.JSONWebTokenBackend"


class _AuthRequest:
    """Minimal HttpRequest-like shim for the REST auth backends.

    The OAuth2 and JWT authenticators only inspect request headers (the
    ``Authorization`` bearer/JWT token); the request body is not needed to
    validate a bearer token, so this shim avoids consuming the body that the
    MCP handler still has to read.
    """

    def __init__(self, scope):
        self.method = scope.get("method", "GET")
        self.path = scope.get("path", "")
        self.META = self._headers_to_meta(scope)
        self.POST = QueryDict()
        self.COOKIES = {}
        self._scope = scope

    @staticmethod
    def _headers_to_meta(scope):
        meta = {}
        for name, value in scope.get("headers", ()):  # (bytes, bytes)
            name = name.decode("latin-1")
            value = value.decode("latin-1")
            if name == "content-length":
                key = "CONTENT_LENGTH"
            elif name == "content-type":
                key = "CONTENT_TYPE"
            else:
                key = "HTTP_" + name.upper().replace("-", "_")
            meta[key] = value
        return meta

    def get_full_path(self):
        qs = self._scope.get("query_string", b"")
        if isinstance(qs, bytes):
            qs = qs.decode("latin-1")
        return self.path + (("?" + qs) if qs else "")

    def is_secure(self):
        return self._scope.get("scheme") == "https"


def _resolve_authenticators():
    """Build the list of authenticator classes from existing REST settings.

    Reuses, in order:
    * ``REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']`` (OAuth2), and
    * the JWT backend (``graphql_jwt.backends.JSONWebTokenBackend``) when it is
      registered in ``AUTHENTICATION_BACKENDS``.
    """
    paths = []
    rest_framework = getattr(settings, "REST_FRAMEWORK", None) or {}
    paths.extend(rest_framework.get("DEFAULT_AUTHENTICATION_CLASSES", []))
    if _JWT_BACKEND_PATH in getattr(settings, "AUTHENTICATION_BACKENDS", []):
        paths.append(_JWT_BACKEND_PATH)

    seen = set()
    classes = []
    for p in paths:
        if p in seen:
            continue
        seen.add(p)
        try:
            classes.append(import_string(p))
        except ImportError:
            logger.warning("MCP auth: cannot import '%s'", p)
    return classes


async def _authenticate(scope):
    """Return the authenticated user for the request, or ``None``.

    Tries each configured authenticator. Authenticators perform DB access
    (OAuth2 access-token lookup, JWT user lookup), so they run off the event
    loop via ``sync_to_async`` with connection cleanup.
    """
    authenticators = _resolve_authenticators()
    if not authenticators:
        logger.error(
            "MCP_SERVER_PRV is enabled but no authenticators are configured "
            "(enable REST/GRAPHQL). Denying the request."
        )
        return None

    shim = _AuthRequest(scope)

    def run():
        from django.db import close_old_connections

        try:
            for auth_cls in authenticators:
                try:
                    result = auth_cls().authenticate(shim)
                except Exception:
                    continue
                if result:
                    # DRF authenticators return (user, token); the graphql_jwt
                    # backend returns the user directly.
                    return result[0] if isinstance(result, (tuple, list)) else result
            return None
        finally:
            close_old_connections()

    return await sync_to_async(run)()


async def _unauthorized(send, message="Unauthorized"):
    await send(
        {
            "type": "http.response.start",
            "status": 401,
            "headers": [
                (b"www-authenticate", b'Bearer realm="mcp"'),
                (b"content-type", b"application/json"),
            ],
        }
    )
    import json

    await send(
        {
            "type": "http.response.body",
            "body": json.dumps(
                {
                    "jsonrpc": "2.0",
                    "error": {"code": -32001, "message": message},
                    "id": None,
                }
            ).encode("utf-8"),
        }
    )


async def mcp_streamable_http(scope, receive, send):
    """Handle a single MCP Streamable HTTP request on the event loop."""
    server = get_mcp_server()
    session_manager = StreamableHTTPSessionManager(
        app=server._mcp_server,
        event_store=None,
        json_response=bool(getattr(settings, "DJANGO_MCP_JSON_RESPONSE", True)),
        stateless=bool(getattr(settings, "DJANGO_MCP_STATELESS", True)),
        security_settings=None,
    )
    current_user.set(scope.get("user"))
    async with session_manager.run():
        await session_manager.handle_request(scope, receive, send)


async def mcp_streamable_http_protected(scope, receive, send):
    """Auth-gated wrapper: authenticates then delegates to the MCP handler."""
    if scope.get("type") != "http":
        await mcp_streamable_http(scope, receive, send)
        return

    user = await _authenticate(scope)
    if user is None or not getattr(user, "is_authenticated", False):
        await _unauthorized(send)
        return
    scope = dict(scope)
    scope["user"] = user
    await mcp_streamable_http(scope, receive, send)


class MCPHttpRouter:
    """ASGI HTTP router: ``/mcp`` -> MCP, everything else -> Django.

    Mounted inside the Channels ``ProtocolTypeRouter`` so routing is still
    channels-managed, while the MCP endpoint is served natively as ASGI.
    Authentication is applied to the MCP endpoint only when
    ``settings.MCP_SERVER_PRV`` is set.
    """

    def __init__(self, django_app, path):
        self.django_app = django_app
        self.path = path
        self.protected = bool(getattr(settings, "MCP_SERVER_PRV", False))
        self.mcp_app = mcp_streamable_http_protected if self.protected else mcp_streamable_http

    async def __call__(self, scope, receive, send):
        if scope.get("type") == "http" and self._matches(scope):
            await self.mcp_app(scope, receive, send)
        else:
            await self.django_app(scope, receive, send)

    def _matches(self, scope) -> bool:
        path = scope.get("path") or ""
        if path == self.path:
            return True
        # tolerate a trailing slash
        return path.rstrip("/") == self.path.rstrip("/") and self.path != "/"
