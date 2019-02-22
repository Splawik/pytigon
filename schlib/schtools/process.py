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

#Pytigon - wxpython and django application framework

#author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

import sys
import os
import asyncio
import imp
from subprocess import Popen, PIPE
from threading import Thread
import importlib

from schlib.schtools.tools import get_executable

class FrozenModules():
    def __init__(self):
        self.to_restore = {}
        self.all = []
        to_delete = []

        for pos in sys.modules:
            self.all.append(pos)
            if pos.startswith('django') or pos.startswith('schlib') or pos.startswith('schserw') or pos.startswith('settings'):
                self.to_restore[pos] = sys.modules[pos]
                to_delete.append(pos)

        for pos in to_delete:
            del sys.modules[pos]

    def restore(self):
        to_delete = []
        for module in sys.modules:
            if not module in self.all:
                to_delete.append(module)

        for module in to_delete:
            del sys.modules[module]

        for pos in self.to_restore:
            sys.modules[pos] = self.to_restore[pos]

def run(cmd):
    """run extern command

    args:
        cmd - array of parameters

    returns:
        array:
            return code,
            return stdout data
            return stderr data
    example:
        run(["ls" "-la",])
    """
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if output:
        if type(output) != str:
            s = output.decode('utf-8')
        else:
            s = output
        output_tab = [ pos.replace('\r','') for pos in s.split('\n') ]
    else:
        output_tab = None

    if err:
        if type(err) != str:
            s = err.decode('utf-8')
        else:
            s = err
        err_tab = [pos.replace('\r', '') for pos in s.split('\n')]
    else:
        err_tab = None
    return (exit_code, output_tab, err_tab)


def py_run(cmd):
    """run python script

    args:
        cmd - array of parameters

    returns:
        array:
            return code,
            return stdout data
            return stderr data
    example:
        py_run(["manage.py", "help"])
    """
    return run([get_executable(), ]+cmd)

def _manage(path, cmd):
    frozen_modules = FrozenModules()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    os.chdir(path)
    #tmp = []
    #to_reload = {}
    #for m in sys.modules:
    #    tmp.append(m)
    #for pos in tmp:
    #    if pos.startswith('django') or pos.startswith('schserw') or pos.startswith('settings'):
    #        to_reload[pos] = sys.modules[pos]
    #        del sys.modules[pos]
    #
    m = __import__("schlib.schdjangoext.django_manage")
    sys.path.insert(0, path)
    m.schdjangoext.django_manage.cmd(cmd, from_main=False)
    sys.path.pop(0)
    #to_delete = []
    #for module in sys.modules:
    #    if not module in tmp:
    #        to_delete.append(module)

    #for module in to_delete:
    #    del sys.modules[module]

    #for pos in to_reload:
    #    sys.modules[pos] = to_reload[pos]

    frozen_modules.restore()

def py_manage(cmd, thread_version = False):
    if len(cmd) > 0:
        if thread_version:
            thread = Thread(target=_manage, args=(os.getcwd(), cmd,))
            thread.start()
            thread.join()
            return 0, [], []
        else:
            return py_run(['manage.py',] + cmd)




