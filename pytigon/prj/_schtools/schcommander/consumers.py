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

import select
import time
from threading import Thread
import subprocess
import struct
import getpass

try:
    import pty
    import fcntl
    import termios
except:
    pass

from django.conf import settings

from pytigon_lib.schtools.tools import get_executable


def read_and_forward_pty_output(consumer):
    max_read_bytes = 1024 * 20
    while not consumer.exit:
        time.sleep(0.01)
        if consumer.fd:
            timeout_sec = 1
            (data_ready, _, _) = select.select(
                [
                    consumer.fd,
                ],
                [],
                [],
                timeout_sec,
            )
            if data_ready:
                output = os.read(consumer.fd, max_read_bytes)
                try:
                    output = output.decode(errors="replace")
                except:
                    print("---------------------------------------------")
                    print(output)
                    print("---------------------------------------------")
                    output = ""
                if output:
                    consumer.send(text_data=output)
    print("Shell closed")


class ShellConsumer(WebsocketConsumer):

    def set_winsize(self, fd, row, col, xpix=0, ypix=0):
        winsize = struct.pack("HHHH", row, col, xpix, ypix)
        fcntl.ioctl(self.fd, termios.TIOCSWINSZ, winsize)

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            x = json.loads(text_data)
            if "input" in x:
                if self.fd:
                    os.write(self.fd, x["input"].encode("utf-8"))
            if "resize" in x:
                size = x["resize"]
                if self.fd:
                    self.set_winsize(self.fd, size["rows"], size["cols"])
            if "ping" in x:
                self.send(text_data="pong")

    def connect(self):
        print("Connecting.......")
        self.exit = False
        self.fd = None
        self.child_pid = None
        self.accept()
        (child_pid, fd) = pty.fork()
        if child_pid == 0:
            env2 = os.environ.copy()
            env2["TERM"] = "xterm"
            if (
                settings.PLATFORM_TYPE == "webserver"
                and getpass.getuser() == "www-data"
            ):
                env2["HOME"] = "/home/www-data"
            subprocess.run([get_executable(), "-m", "xonsh"], env=env2)
        else:
            self.fd = fd
            self.child_pid = child_pid
            self.thread = Thread(target=read_and_forward_pty_output, args=(self,))
            self.thread.start()

    def disconnect(self, close_code):
        print("Disconnect.......")
        self.exit = True
        os.write(self.fd, b"exit\n")
