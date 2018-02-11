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

import os

def _mkdir(path, ext=None):
    if ext:
        p = os.path.join(path, ext)
    else:
        p = path

    if not os.path.exists(p):
        os.mkdir(p)

def init(app_pack, data_path, paths=None):
    _paths = ['', 'cache', 'plugins_cache', '_schall',  'schdevtools', app_pack]
    for p in _paths:
        _mkdir(data_path, p)
    if paths:
        for p in paths:
            _mkdir(p)
