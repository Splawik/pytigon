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


class teleconference(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = True
        self.base_room_group_name = "default"

    async def init_consumer(self, conf):
        if "room" in conf:
            self.base_room_group_name = conf["room"]

        if "host" in conf and conf["host"]:
            self.host = True
            self.room_group_name = self.base_room_group_name + "_host"
            self.room_other_group_name = self.base_room_group_name
        else:
            self.host = False
            self.room_group_name = self.base_room_group_name
            self.room_other_group_name = self.base_room_group_name + "_host"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.send_json({"status": "initiated"})

    async def connect(self):
        await self.accept()
        await self.send_json({"status": "connected"})

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.room_other_group_name,
            {
                "type": "chat_destroy",
                "message": {
                    "destroy": True,
                },
            },
        )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print("DDDDDDDDDDDDDDDDDIIIIIIIIIIIISSSSSSSSSSCONNECT")

    async def receive_json(self, content):
        print("receive_json: ", content)
        if "init_consumer" in content:
            await self.init_consumer(content)
        elif "ping" in content:
            pass
        else:
            await self.channel_layer.group_send(
                self.room_other_group_name, {"type": "chat_message", "message": content}
            )

    async def chat_message(self, event):
        message = event["message"]
        await self.send_json(message)

    async def chat_destroy(self, event):
        print("DEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEESTROY")
        message = event["message"]
        await self.send_json(message)
