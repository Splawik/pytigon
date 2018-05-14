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
    print("X1", app_pack, root_path, data_path, app_pack_path, paths)
    if not os.path.exists(app_pack_path):
        p2 = os.path.join(root_path, 'app_pack')
        print("X2",p2)
        if os.path.exists(p2):
            print("X3", p2, app_pack_path)
            shutil.copytree(p2, app_pack_path)
        else:
            zip_file = os.path.join(root_path, "app_pack.zip")
            print("X4", zip_file)
            if os.path.exists(zip_file):
                print("X5", app_pack_path)
                os.makedirs(app_pack_path)
                extractall(zipfile.ZipFile(zip_file), app_pack_path)

    print("X6", data_path)
    if not os.path.exists(data_path):
        zip_file2 = os.path.join(os.path.join(root_path, "install"), ".pytigon.zip")
        print("X7", zip_file2)
        if os.path.exists(zip_file2):
            print("X8", data_path)
            os.makedirs(data_path)
            print("X9", zip_file2, data_path)
            extractall(zipfile.ZipFile(zip_file2), data_path)

    print("X10", zip_file2, data_path)
    _paths = ['', 'cache', 'plugins_cache', '_schall',  'schdevtools', app_pack]
    for p in _paths:
        _mkdir(data_path, p)
    if paths:
        for p in paths:
            _mkdir(p)
