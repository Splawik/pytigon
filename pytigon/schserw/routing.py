import importlib

from django.urls import path, re_path
from django.core.asgi import get_asgi_application
from django.conf import settings

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

urls_tab = []


if hasattr(settings, "CHANNELS_URL_TAB"):
    for row in settings.CHANNELS_URL_TAB:
        u = row[0]
        tmp = row[1].split(".")
        m = importlib.import_module(".".join(tmp[:-1]))
        o = getattr(m, tmp[-1])
        if "(?P" in u:
            urls_tab.append(re_path(u, o.as_asgi()))
        else:
            urls_tab.append(path(u, o.as_asgi()))


class LifespanApp:
    def __init__(self, scope):
        self.scope = scope

    async def __call__(self, receive, send):
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
