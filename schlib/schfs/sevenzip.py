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

import os
from .vfsplugin import VfsPlugin
from .extern_arch import ArchDirectory


class SevenZipConsole(object):

    ext_read_and_write = ('7z', 'gzip', 'bzip2')
    ext_read_only = (
        'arj',
        'cab',
        'chm',
        'cpio',
        'deb',
        'dmg',
        'hfs',
        'iso',
        'lzh',
        'lzma',
        'msi',
        'nsis',
        'rar',
        'rpm',
        'udf',
        'wim',
        'xar',
        'z',
        )

    def type(self):
        return '7-zip'

    def is_virtual_dir(self, pos):
        ext = pos.lower().split('.')[-1]
        if ext in self.ext_read_and_write or ext in self.ext_read_only:
            return True
        else:
            return False

    def list(self, path, out):
        cmd = "7z l '" + path + "'"
        f = os.popen(cmd)
        if f:
            x = f.readlines()
            start = False
            for pos in x:
                if not start:
                    if pos[:18] == '------------------':
                        start = True
                else:
                    if pos[:18] == '------------------':
                        start = False
                    else:
                        pos = pos.replace('\n', '')
                        if pos[20] == 'D':
                            out.append(('D', pos[53:], pos[:19], pos[25:38]))
                        else:
                            out.append(('F', pos[53:], pos[:19], pos[25:38]))

    def read_from_arch(
        self,
        zip_name,
        zip_file_name,
        out_file_name,
        ):
        return '7z e -so ' + zip_name + ' ' + zip_file_name + ' > '\
             + out_file_name

    def write_to_arch(
        self,
        zip_name,
        in_file_name,
        zip_file_name,
        ):
        return '7z a -si' + zip_file_name + ' ' + zip_name + ' < '\
             + in_file_name


class VfsPluginSevenZip(VfsPlugin):

    def __init__(self):
        self.archconsole = SevenZipConsole()

    def is_virtual_dir(self, pos):
        return self.archconsole.is_virtual_dir(pos)

    def empty_file_in_lfs(self, local_path, file_name):
        return False

    def cd(
        self,
        parent,
        basepath,
        pos,
        ):
        return ArchDirectory(self.archconsole, parent, basepath + pos + '/')


