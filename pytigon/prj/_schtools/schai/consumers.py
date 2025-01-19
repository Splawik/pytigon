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

from pytigon_lib.schtools.env import get_environ

ENV = get_environ()

OLLAMA_URL = ENV("OLLAMA_URL", default="127.0.0.1")
OLLAMA_MODEL = ENV("OLLAMA_MODEL", default="")

OPENAI_URL = ENV("OPENAI_URL", default="")
OPENAI_MODEL = ENV("OPENAI_MODEL", default="")
OPENAI_API_KEY = ENV("OPENAI_API_KEY", default="")

if OLLAMA_MODEL:
    try:
        import ollama
    except:
        print("For AI demo you shoud install ollama")

if OPENAI_MODEL:
    try:
        import openai
    except:
        print("For AI demo you shoud install openai")


class OllamaConnector(AsyncJsonWebsocketConsumer):
    client = None

    async def connect(self):
        await self.accept()

    async def receive_json(self, content):
        if "id" in content:
            id = content["id"]
            content_str = content["content"]
            message = {"role": "user", "content": content_str}
            self.client = ollama.AsyncClient(host=OLLAMA_URL)
            model_name = OLLAMA_MODEL
            async for part in await self.client.chat(
                model=model_name, messages=[message], stream=True
            ):
                await self.send_json({"content": part["message"]["content"]})
            self.client = None
            await self.send_json(
                {"content": "\n----------------------------------------------\n"}
            )

    async def disconnect(self, close_code):
        if self.client:
            await self.client.close()


class OpenAiConnector(AsyncJsonWebsocketConsumer):
    client = None

    async def connect(self):
        await self.accept()

    async def receive_json(self, content):
        if "id" in content:
            id = content["id"]
            content_str = content["content"]
            message = {"role": "user", "content": content_str}

            client = openai.AsyncOpenAI(
                base_url=OPENAI_URL,
                api_key=OPENAI_API_KEY,
            )
            stream = await client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    message,
                ],
                stream=True,
            )
            async for chunk in stream:
                print(chunk.choices[0].delta.content or "", end="")
                await self.send_json({"content": chunk.choices[0].delta.content or ""})
            self.client = None
            await self.send_json(
                {"content": "\n----------------------------------------------\n"}
            )

    async def disconnect(self, close_code):
        if self.client:
            await self.client.close()
