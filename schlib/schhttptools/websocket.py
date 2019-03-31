#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Pu`blic License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Pytigon - wxpython and django application framework

#author: "Sławomir Chołaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Sławomir Chołaj"
#license: "LGPL 3.0"
#version: "0.1a"

import asyncio
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
from schlib.schtools.schjson import json_dumps, json_loads

class PytigonClientProtocolBase():
    def onConnect(self, response):
        print("OnConnect")
        return self.app.on_websocket_connect(self, self.websocket_id, response)

    def onOpen(self):
        print("OnOpen")
        return self.app.on_websocket_open(self, self.websocket_id)

    def onClose(self, wasClean, code, reason):
        print("OnClose")
        pass

    def onMessage(self, msg, binary):
        return self.app.on_websocket_message(self, self.websocket_id, { "msg": msg })


def create_websocket_client(app, websocket_id, local=False, callback=False):
    if local:
        class PytigonClientProtocol(PytigonClientProtocolBase):
            def __init__(self, app):
                self.app = app
                self.websocket_id = websocket_id
                self.input_queue = asyncio.Queue()
                self.callbacks = []
                self.status = 1

            async def send_message(self, msg):
                await self.input_queue.put(json_dumps(msg))

        app.websockets[websocket_id] = PytigonClientProtocol(app)

    else:
        class PytigonClientProtocol(PytigonClientProtocolBase, WebSocketClientProtocol):
            def __init__(self):
                nonlocal app, websocket_id
                PytigonClientProtocolBase.__init__(self)
                WebSocketClientProtocol.__init__(self)
                self.app = app
                self.websocket_id = websocket_id
                app.websockets[websocket_id] = self
                self.status = 0

            def send_message(self, msg):
                super().sendMessage(json_dumps(msg).encode('utf-8'))

        ws_address = app.base_address.replace('http', 'ws').replace('https', 'wss')
        ws_address += websocket_id
        factory = WebSocketClientFactory(ws_address)
        factory.protocol = PytigonClientProtocol
        connectWS(factory)

    if callback:
        app.add_websoket_callback(websocket_id, callback)
