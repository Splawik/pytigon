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
import sys
from schlib.schfs.vfstools import extractall
import zipfile
#import shutil
from distutils.dir_util import copy_tree
import configparser

def _mkdir(path, ext=None):
    if ext:
        p = os.path.join(path, ext)
    else:
        p = path

    if not os.path.exists(p):
        os.mkdir(p)

def upgrade_test(zip_path, out_path):
    if os.path.exists(zip_path):
        archive = zipfile.ZipFile(zip_path, 'r')
        cfg_txt = archive.read('install.ini').decode('utf-8')
        cfg = configparser.ConfigParser()
        cfg.read_string(cfg_txt)
        t1 = cfg['DEFAULT']['GEN_TIME']
        ini2 = os.path.join(out_path, "install.ini")
        if os.path.exists(ini2):
            cfg2 = configparser.ConfigParser()
            cfg2.read(ini2)
            t2 = cfg2['DEFAULT']['GEN_TIME']
            if t2 < t1:
                return True
    return False


def init(app_pack, root_path, data_path, app_pack_path, static_app_path, paths=None):
    _root_path = os.path.normpath(root_path)
    _data_path = os.path.normpath(data_path)
    _app_pack_path = os.path.normpath(app_pack_path)
    _static_app_path = os.path.normpath(static_app_path)

    test1 = 0 if os.path.exists(_app_pack_path) else 1
    test2 = 0 if os.path.exists(_data_path) else 1
    test3 = 0 if os.path.exists(_static_app_path) else 1

    if not test1:
        if upgrade_test(os.path.join(os.path.join(_root_path, "install"), "app_pack.zip"),_app_pack_path):
            test1 = 2
            print("Upgrade app_pack")

    if not test2:
        if upgrade_test(os.path.join(os.path.join(_root_path, "install"), ".pytigon.zip"), _data_path):
            test2 = 2
            print("Upgrade data")

    if test1:
        p2 = os.path.join(_root_path, 'app_pack')
        if os.path.exists(p2) and test1 == 1:
            copy_tree(p2, _app_pack_path, preserve_mode=0, preserve_times=0)
        else:
            zip_file = os.path.join(os.path.join(_root_path, "install"), "app_pack.zip")
            if os.path.exists(zip_file):
                if not os.path.exists(_app_pack_path):
                    os.makedirs(_app_pack_path)
                extractall(zipfile.ZipFile(zip_file), _app_pack_path)

    if test2:
        zip_file2 = os.path.join(os.path.join(_root_path, "install"), ".pytigon.zip")
        if os.path.exists(zip_file2):
            if not os.path.exists(_data_path):
                os.makedirs(_data_path)
            if test2==2:
                extractall(zipfile.ZipFile(zip_file2), _data_path, exclude=['.*\.db',])
            else:
                extractall(zipfile.ZipFile(zip_file2), _data_path)
            if not os.path.exists(os.path.join(_data_path,'media')):
                media_path = os.path.exists(os.path.join(_data_path,'media'))
                os.makedirs(media_path)
                os.makedirs(os.path.join(media_path,'filer_public'))
                os.makedirs(os.path.join(media_path,'filer_private'))
                os.makedirs(os.path.join(media_path,'filer_public_tumbnails'))
                os.makedirs(os.path.join(media_path,'filer_private_thumbnails'))

    if test2 == 2:
        pass

    if test3:
        p2 = os.path.join(os.path.join(_root_path, 'static'), 'app')
        if os.path.exists(p2):
            copy_tree(p2, _static_app_path, preserve_mode=0, preserve_times=0)

    _paths = ['', 'cache', 'plugins_cache', '_schall',  'schdevtools', app_pack]
    for p in _paths:
        _mkdir(_data_path, p)
    if paths:
        for p in paths:
            _mkdir(p)

    applib = os.path.join(os.path.join(_app_pack_path, app_pack), "applib")
    if os.path.exists(applib) and not applib in sys.path:
        sys.path.append(applib)
