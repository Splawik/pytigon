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
#copyright: "Copyright (C) ????/2013 Slawomir Cholaj"
#license: "LGPL 3.0"
#version: "0.1a"

import os
import django

def cmd(arg, from_main=False):
    if from_main:
        argv = arg
    else:
        if type(arg) == str:
            argv=['manage.py', arg]
        else:
            argv=['manage.py',] + arg
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_app")
    from django.core.management import execute_from_command_line
    execute_from_command_line(argv)


def syncdb():
    cmd('syncdb')


def help():
    cmd('help')

