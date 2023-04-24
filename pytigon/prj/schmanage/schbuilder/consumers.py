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

import asyncio
import psutil
from os import environ
from django.conf import settings


class Clock(AsyncJsonWebsocketConsumer):

    COUNT = 1

    async def connect(self):
        await self.accept()

    async def receive_json(self, content):
        print("RECEIVED: ", content)
        await self.send_json({"txt": "hello world"})
        # await self.close(code=4123)

        for i in range(0, 10):
            await asyncio.sleep(1)
            await self.send_json({"clock": self.COUNT})
            self.COUNT += 1

    async def disconnect(self, close_code):
        print("Websocket closed", close_code)


class WebServer(AsyncJsonWebsocketConsumer):

    PROC = None

    async def connect(self):
        await self.accept()

    async def subprocess(self, prj):
        environ["PYTHONPATH"] = os.path.join(settings.ROOT_PATH, "..")

        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m",
            "pytigon.ptig",
            "manage_" + prj,
            "runserver",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        self.PROC = proc

        while True:
            data = await proc.stdout.readline()
            if data == b"":
                break
            await self.send_json({"txt": data.decode("utf-8")})

        await proc.wait()
        await self.send_json({"txt": ""})

    async def receive_json(self, content):
        command = content["command"]
        if command == "start":
            if self.PROC:
                parent = psutil.Process(self.PROC.pid)
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()
                await self.PROC.wait()
                self.PROC = None
            loop = asyncio.get_running_loop()
            tsk = loop.create_task(self.subprocess(content["id"]))

            def finish(t):
                print("Finished")

            tsk.add_done_callback(finish)
        elif command == "stop":
            if self.PROC:
                parent = psutil.Process(self.PROC.pid)
                for child in parent.children(recursive=True):
                    child.kill()
                # parent.kill()
                await self.PROC.wait()
                self.PROC = None
        else:
            pass

    async def disconnect(self, close_code):
        print("Websocket closed", close_code)


class DjangoManage(AsyncJsonWebsocketConsumer):

    PROCS = []

    async def connect(self):
        await self.accept()

    async def subprocess(self, prj, cmd):
        environ["PYTHONPATH"] = os.path.join(settings.ROOT_PATH, "..")

        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m",
            "pytigon.ptig",
            "manage_" + prj,
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )
        self.PROCS.append(proc)

        while True:
            data = await proc.stdout.readline()
            if data == b"":
                break
            await self.send_json({"txt": data.decode("utf-8")})

        await proc.wait()
        await self.send_json({"txt": ""})
        self.PROCS.remove(proc)

    async def receive_json(self, content):
        command = content["command"]
        if command == "start":
            cmd = content["cmd"].split(" ")
            loop = asyncio.get_running_loop()
            tsk = loop.create_task(self.subprocess(content["id"], cmd))

            def finish(t):
                print("Finished")

            tsk.add_done_callback(finish)
        elif command == "start":
            if self.PROCS:
                for proc in self.PROCS:
                    parent = psutil.Process(proc.pid)
                    for child in parent.children(recursive=True):
                        child.kill()
                    # parent.kill()
                    await proc.wait()
                self.PROCS = []
        else:
            pass

    async def disconnect(self, close_code):
        print("Websocket closed", close_code)
