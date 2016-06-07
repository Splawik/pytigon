#! /usr/bin/python3
# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY  ; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2013 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

from threading import Thread
from multiprocessing import Process
import socket
import datetime
import sys
import threading

from django.conf import settings
from django.core.management.commands.runserver import Command as RunserverCommand
from django.utils import six
from django.utils.encoding import get_system_encoding

from channels import DEFAULT_CHANNEL_LAYER, channel_layers
from channels.handler import ViewConsumer
from channels.log import setup_logger
from channels.staticfiles import StaticFilesConsumer
from channels.worker import Worker


class WorkerThread(threading.Thread):
    def __init__(self, channel_layer):
        super(WorkerThread, self).__init__()
        self.channel_layer = channel_layer

    def run(self):
        worker = Worker(channel_layer=self.channel_layer, signal_handlers=False)
        worker.run()

def log_action(protocol, action, details):
    msg = "[%s] " % datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    # HTTP requests
    if protocol == "http" and action == "complete":
        msg += "HTTP %(method)s %(path)s %(status)s [%(time_taken).2f, %(client)s]\n" % details
        # Utilize terminal colors, if available
    elif protocol == "websocket" and action == "connected":
        msg += "WebSocket CONNECT %(path)s [%(client)s]\n" % details
    elif protocol == "websocket" and action == "disconnected":
        msg += "WebSocket DISCONNECT %(path)s [%(client)s]\n" % details

    sys.stderr.write(msg)


def _run(addr, port):
    channel_layer = channel_layers[DEFAULT_CHANNEL_LAYER]
    channel_layer.router.check_default(
        http_consumer=ViewConsumer(),
    )
    quit_command = 'CTRL-BREAK' if sys.platform == 'win32' else 'CONTROL-C'
    now = datetime.datetime.now().strftime('%B %d, %Y - %X')
    if six.PY2:
        now = now.decode(get_system_encoding())

    for _ in range(4):
        worker = WorkerThread(channel_layer)
        worker.daemon = True
        worker.start()

    # Launch server in 'main' thread. Signals are disabled as it's still
    # actually a subthread under the autoreloader.
    try:
        from daphne.server import Server
        server = Server(
            channel_layer=channel_layer,
            host=addr,
            port=int(port),
            signal_handlers=False,
            action_logger=log_action,
            http_timeout=60,
        )
        server.run()
    except KeyboardInterrupt:
        return


class ServProc():
    def __init__(self, proc):
        self.proc = proc

    def stop(self):
        self.proc.terminate()

def run_server(address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Start serwer: ', address, port)

    #thread = Thread(target = _run, args=(address, port) )
    #thread.start()

    proc = Process(target = _run, args=(address, port) )
    proc.start()

    while(True):
        try:
            s.connect((address, port))
            s.close()
            break
        except:
            pass
    print("Server started")
    #return thread

    return ServProc(proc)