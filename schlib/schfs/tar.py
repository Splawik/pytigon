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


class TarConsole(object):

    ext_read_and_write = ('gz', 'tgz', 'tar')
    ext_read_only = ()

    def type(self):
        return 'tar'

    def is_virtual_dir(self, pos):
        ext = pos.lower().split('.')[-1]
        if ext in self.ext_read_and_write or ext in self.ext_read_only:
            return True
        else:
            return False

    def list(self, path, out):
        cmd = "tar -tvf '" + path + "'"
        f = os.popen(cmd)
        if f:
            x = f.readlines()
            for pos in x:
                pos = pos.replace('\n', '')
                l = pos.split()
                if l[5][-1] in ('/', '\\'):
                    out.append(('D', (l[5])[:-1], l[3] + ' ' + l[4], l[2]))
                else:
                    out.append(('F', l[5], l[3] + ' ' + l[4], l[2]))

    def read_from_arch(
        self,
        zip_name,
        zip_file_name,
        out_file_name,
        ):
        return 'tar -xvOf ' + zip_name + ' ' + zip_file_name + ' > '\
             + out_file_name

    def write_to_arch(
        self,
        zip_name,
        in_file_name,
        zip_file_name,
        ):
        return 'tar -uvf ' + zip_name + ' --add-file=' + in_file_name


class VfsPluginTar(VfsPlugin):

    def __init__(self):
        self.archconsole = TarConsole()

    def is_virtual_dir(self, pos):
        return self.archconsole.is_virtual_dir(pos)

    def cd(
        self,
        parent,
        basepath,
        pos,
        ):
        return ArchDirectory(self.archconsole, parent, basepath + pos + '/')


