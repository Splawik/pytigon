"""ASGI routing configuration for Pytigon.

Uses Django Channels to handle both HTTP and WebSocket protocols.
WebSocket routes are loaded dynamically from settings.CHANNELS_URL_TAB.

Consumer classes belong to the generated application projects (export
artefacts that must not be edited), so authorisation is enforced here: every
route is wrapped by :func:`guard_websocket`, which requires an authenticated
user and a staff user for the endpoints listed in
``settings.WEBSOCKET_STAFF_ONLY`` (interactive shell, ``manage.py``, server
control, task and AI connectors). Cross-origin connections are rejected by
``AllowedHostsOriginValidator``.
"""

import importlib
import logging

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf import settings
from django.core.asgi import get_asgi_application
from django.urls import path, re_path

from pytigon.schserw.schsys.default_admin import startup_check as _default_admin_startup_check

logger = logging.getLogger(__name__)

# WebSocket close codes (4000-4999 is the private range).
_WS_UNAUTHENTICATED = 4401
_WS_FORBIDDEN = 4403


def _websocket_is_staff_only(url_pattern: str) -> bool:
    """Return whether *url_pattern* belongs to a staff-only endpoint."""
    markers = getattr(settings, "WEBSOCKET_STAFF_ONLY", ())
    return any(marker and marker in url_pattern for marker in markers)


def _websocket_is_public(url_pattern: str) -> bool:
    """Return whether *url_pattern* is explicitly allowed to stay anonymous."""
    markers = getattr(settings, "WEBSOCKET_PUBLIC_PATHS", ())
    return any(marker and marker in url_pattern for marker in markers)


async def _reject_websocket(send, code: int) -> None:
    """Close a WebSocket that has not been accepted yet."""
    await send({"type": "websocket.close", "code": code})


def guard_websocket(url_pattern: str, inner_app):
    """Wrap a consumer application with an authorisation check.

    The consumer classes live in the generated application projects, which are
    export artefacts and must not be edited, so the check is applied here while
    the routes are built. ``scope["user"]`` is already populated by
    :class:`channels.auth.AuthMiddlewareStack`, which wraps the router.

    Args:
        url_pattern: The URL pattern the consumer is mounted on.
        inner_app: The consumer ASGI application to delegate to.

    Returns:
        An ASGI application that rejects unauthorised connections with a
        WebSocket close instead of reaching the consumer.
    """
    staff_only = _websocket_is_staff_only(url_pattern)
    public = _websocket_is_public(url_pattern)

    async def application(scope, receive, send):
        user = scope.get("user")
        authenticated = bool(user is not None and getattr(user, "is_authenticated", False))
        is_staff = authenticated and bool(getattr(user, "is_staff", False))

        if staff_only:
            # Administrative endpoints (shell, manage.py, server control) stay
            # staff-only even on a PUBLIC site.
            if not is_staff:
                await _reject_websocket(
                    send, _WS_FORBIDDEN if authenticated else _WS_UNAUTHENTICATED
                )
                return
        elif public:
            pass
        elif (
            getattr(settings, "WEBSOCKET_REQUIRE_AUTH", True)
            and not getattr(settings, "PUBLIC", False)
            and not authenticated
        ):
            await _reject_websocket(send, _WS_UNAUTHENTICATED)
            return

        return await inner_app(scope, receive, send)

    return application


def _build_websocket_routes() -> list:
    """Build WebSocket URL routes from settings.CHANNELS_URL_TAB.

    Loads consumer classes dynamically from dotted paths specified
    in the settings configuration.

    Returns:
        list: A fresh list of URL patterns. Building into a module-level list
            made a second call duplicate every route.
    """
    routes = []
    if not hasattr(settings, "CHANNELS_URL_TAB"):
        return routes

    for row in settings.CHANNELS_URL_TAB:
        consumer_path = None
        try:
            url_pattern = row[0]
            consumer_path = row[1]
            module_path, class_name = consumer_path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            consumer_class = getattr(module, class_name)
            guarded = guard_websocket(url_pattern, consumer_class.as_asgi())

            if "(?P" in url_pattern:
                routes.append(re_path(url_pattern, guarded))
            else:
                routes.append(path(url_pattern, guarded))
        except (ImportError, AttributeError, ValueError) as e:
            logger.error(
                "Failed to load WebSocket consumer '%s': %s",
                consumer_path if consumer_path is not None else str(row),
                e,
            )
    return routes


urls_tab = _build_websocket_routes()


class LifespanApp:
    """ASGI application that handles the lifespan protocol.

    Responds to lifespan.startup and lifespan.shutdown events
    as required by the ASGI specification.
    """

    def __init__(self, scope):
        """Initialize with the ASGI scope.

        Args:
            scope: The ASGI connection scope.
        """
        self.scope = scope

    async def __call__(self, receive, send):
        """Process lifespan events.

        Args:
            receive: ASGI receive callable.
            send: ASGI send callable.
        """
        if self.scope["type"] != "lifespan":
            return
        while True:
            message = await receive()
            message_type = message["type"]
            if message_type == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message_type == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return
            else:
                # Without this branch an unknown message type spins the loop
                # forever, pegging a CPU core.
                logger.warning("Unexpected ASGI lifespan message: %s", message_type)
                return


django_asgi_app = get_asgi_application()

# Production guard: warn loudly at process start, or refuse to boot in strict
# mode, when the bootstrap administrator password is still active. This runs
# after django.setup() (triggered by get_asgi_application), so the auth tables
# are reachable. It is a no-op for the embedded desktop client and development.
_default_admin_startup_check(raise_if_blocked=True)

# When MCP_SERVER is enabled, route the MCP Streamable HTTP endpoint
# (/mcp) to a native ASGI app and leave everything else to Django. This keeps
# the MCP request path on the event loop (no sync<->async bridging).
if settings.MCP_SERVER:
    from pytigon.schserw.mcp.http import MCPHttpRouter, mcp_path

    django_asgi_app = MCPHttpRouter(django_asgi_app, mcp_path())

# AuthMiddlewareStack populates scope["user"] from the session cookie, so the
# per-consumer guard below can check it. AllowedHostsOriginValidator then blocks
# cross-site WebSocket hijacking attempts made from a browser.
websocket_app = AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(urls_tab)))

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": websocket_app,
        "lifespan": LifespanApp,
    }
)
