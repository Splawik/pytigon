import os
import sys
import datetime
import json
import asyncio

from channels.consumer import AsyncConsumer, SyncConsumer

from channels.generic.websocket import (
    WebsocketConsumer,
    AsyncWebsocketConsumer,
    JsonWebsocketConsumer,
    AsyncJsonWebsocketConsumer,
)

from channels.generic.http import AsyncHttpConsumer


class clock(AsyncJsonWebsocketConsumer):
    COUNT = 1

    async def connect(self):
        await self.accept()

    async def receive_json(self, content):
        print("RECEIVED: ", content)
        await self.send_json({"status": "pong", "data": "hello world"})

        for i in range(0, 3):
            await asyncio.sleep(1)
            await self.send_json({"status": "clock", "data": self.COUNT})
            self.COUNT += 1

    async def disconnect(self, close_code):
        print("Websocket closed", close_code)
