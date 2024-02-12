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


class TaskEventsConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.exit = False
        await self.accept()
        self.receiver = None
        self.finish = False
        self.commands = []

    async def receive_json(self, content):
        if "ping" in content:
            await self.send_json({"status": "pong"})
        if "id" in content:
            id = content["id"]
            self.receiver = CommunicationByCacheReceiver(id, self)
            while not self.finish:
                if self.receiver:
                    self.commands = []
                    self.receiver.process()
                    for command in self.commands:
                        await self.send_json(command)
                await asyncio.sleep(1)
            await self.close()

    async def disconnect(self, close_code):
        pass

    def handle_start(self):
        self.commands.append({"status": "start"})

    def handle_event(self, value):
        self.commands.append({"status": "event", "data": value})

    def handle_end(self):
        self.commands.append({"status": "stop"})
        self.finish = True
