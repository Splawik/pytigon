#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

# Pytigon - wxpython and django application framework

# author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
# copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
# license: "LGPL 3.0"
# version: "0.1a"

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
