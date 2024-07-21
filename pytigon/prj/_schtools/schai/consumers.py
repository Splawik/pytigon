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

try:
    import ollama
except:
    print("For AI demo you shoud install ollama")
from pytigon_lib.schtools.env import get_environ

ENV = get_environ()


class OllamaConnector(AsyncJsonWebsocketConsumer):
    client = None

    async def connect(self):
        await self.accept()

    async def receive_json(self, content):
        print("A0:", content)
        if "id" in content:
            id = content["id"]
            content_str = content["content"]
            message = {"role": "user", "content": content_str}
            self.client = ollama.AsyncClient(host="127.0.0.1")
            model_name = ENV("OLLAMA_MODEL", default="llama3")
            async for part in await self.client.chat(
                model=model_name, messages=[message], stream=True
            ):
                await self.send_json({"content": part["message"]["content"]})
            self.client = None
            await self.send_json(
                {"content": "\n----------------------------------------------\n"}
            )

    async def disconnect(self, close_code):
        print("dissconnect")
        if self.client:
            print("A2")
            await self.client.close()
            print("A3")
