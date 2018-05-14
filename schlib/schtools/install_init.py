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
from schlib.schfs.vfstools import extractall
import zipfile
import shutil

def _mkdir(path, ext=None):
    if ext:
        p = os.path.join(path, ext)
    else:
        p = path

    if not os.path.exists(p):
        os.mkdir(p)

def init(app_pack, root_path, data_path, app_pack_path, paths=None):
    _root_path = os.path.normpath(root_path)
    _data_path = os.path.normpath(data_path)
    _app_pack_path = os.path.normpath(app_pack_path)

    test1 = False if os.path.exists(_app_pack_path) else True
    test2 = False if os.path.exists(_data_path) else True

    if test1:
        p2 = os.path.join(_root_path, 'app_pack')
        if os.path.exists(p2):
            shutil.copytree(p2, _app_pack_path)
        else:
            zip_file = os.path.join(_root_path, "app_pack.zip")
            if os.path.exists(zip_file):
                os.makedirs(_app_pack_path)
                extractall(zipfile.ZipFile(zip_file), _app_pack_path)
    if test2:
        zip_file2 = os.path.join(os.path.join(_root_path, "install"), ".pytigon.zip")
        if os.path.exists(zip_file2):
            os.makedirs(_data_path)
            extractall(zipfile.ZipFile(zip_file2), _data_path)

    _paths = ['', 'cache', 'plugins_cache', '_schall',  'schdevtools', app_pack]
    for p in _paths:
        _mkdir(_data_path, p)
    if paths:
        for p in paths:
            _mkdir(p)
