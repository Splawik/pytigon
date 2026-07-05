"""ASGI routing configuration for Pytigon.

Uses Django Channels to handle both HTTP and WebSocket protocols.
WebSocket routes are loaded dynamically from settings.CHANNELS_URL_TAB.
"""

import importlib
import logging

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf import settings
from django.core.asgi import get_asgi_application
from django.urls import path, re_path

logger = logging.getLogger(__name__)

urls_tab = []


def _build_websocket_routes():
    """Build WebSocket URL routes from settings.CHANNELS_URL_TAB.

    Loads consumer classes dynamically from dotted paths specified
    in the settings configuration.
    """
    if not hasattr(settings, "CHANNELS_URL_TAB"):
        return

    for row in settings.CHANNELS_URL_TAB:
        try:
            url_pattern = row[0]
            consumer_path = row[1]
            module_path, class_name = consumer_path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            consumer_class = getattr(module, class_name)

            if "(?P" in url_pattern:
                urls_tab.append(re_path(url_pattern, consumer_class.as_asgi()))
            else:
                urls_tab.append(path(url_pattern, consumer_class.as_asgi()))
        except (ImportError, AttributeError, ValueError) as e:
            logger.error(
                "Failed to load WebSocket consumer '%s': %s",
                consumer_path if "consumer_path" in dir() else str(row),
                e,
            )


_build_websocket_routes()


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
        if self.scope["type"] == "lifespan":
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    await send({"type": "lifespan.shutdown.complete"})
                    return


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(URLRouter(urls_tab)),
        "lifespan": LifespanApp,
    }
)
