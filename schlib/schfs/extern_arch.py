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

from .vfsplugin import VfsDirectory, VfsDirectoryInfo, VfsFileInfo
from .lfs import LfsFile
import os
import tempfile


class ArchFile(LfsFile):

    def __init__(
        self,
        archconsole,
        file_name,
        zip_file_name,
        ):
        LfsFile.__init__(self, file_name)
        self.archconsole = archconsole
        self.temp_file_name = None
        self.zip_file_name = zip_file_name
        self.for_write = False

    def _get_file(self, forwrite=False):
        if not self.file:
            self.for_write = forwrite
            file = tempfile.mkstemp()
            self.temp_file_name = file[1]
            if forwrite:
                self.file = os.fdopen(file[0], 'w')
            else:
                self.file = os.fdopen(file[0], 'w')
                self.file.close()
                self._read_from_zip(self.file_name[:-1], self.zip_file_name,
                                    self.temp_file_name)
                self.file = open(self.temp_file_name, 'r')
        return self.file

    def _read_from_zip(
        self,
        zip_name,
        zip_file_name,
        out_file_name,
        ):
        cmd = self.archconsole.read_from_arch(zip_name, zip_file_name,
                out_file_name)
        f = os.popen(cmd)
        if f:
            x = f.readlines()
            for pos in x:
                print(pos)

    def _write_to_zip(
        self,
        zip_name,
        in_file_name,
        zip_file_name,
        ):
        cmd = self.archconsole.write_to_arch(zip_name, in_file_name,
                zip_file_name)
        f = os.popen(cmd)
        if f:
            x = f.readlines()
            for pos in x:
                print(pos)

    def close(self):
        self._get_file().close()
        if self.for_write:
            self._write_to_zip(self.file_name[:-1], self.temp_file_name,
                               self.zip_file_name)


class ArchDirectory(VfsDirectory):

    def __init__(
        self,
        archconsole,
        parent,
        path,
        poziom=1,
        pathinarchiwe='',
        ):
        VfsDirectory.__init__(self, parent, path)
        self.archconsole = archconsole
        self.poziom = poziom
        self.pathinarchiwe = pathinarchiwe

    def _get_all(self):
        if not self.cache:
            self.cache = []
            self.archconsole.list(self.path[:-1], self.cache)
        return self.cache

    def _transform_poziom(self, name):
        x = name.split('/')
        if len(x) != self.poziom:
            return None
        else:
            if name.startswith(self.pathinarchiwe):
                return x[-1]

    def type(self):
        return self.archconsole.type()

    def get_dirs(self):
        if not self.dirs:
            if self.parent:
                self.dirs = [VfsDirectoryInfo(self.path + self.pathinarchiwe,
                             '..')]
            else:
                self.dirs = []
            for pos in self._get_all():
                if pos[0] == 'D':
                    p = self._transform_poziom(pos[1])
                    if p:
                        self.dirs.append(VfsDirectoryInfo(self.path
                                 + self.pathinarchiwe, p, pos[2], pos[2],
                                pos[2]))
        return self.dirs

    def get_files(self):
        if not self.files:
            self.files = []
            for pos in self._get_all():
                if pos[0] == 'F':
                    p = self._transform_poziom(pos[1])
                    if p:
                        self.files.append(VFSFileInfo(
                            self.path + self.pathinarchiwe,
                            p,
                            pos[3],
                            pos[2],
                            pos[2],
                            pos[2],
                            ))
        return self.files

    def cd(self, folder):
        return ArchDirectory(self.archconsole, self, self.path, self.poziom
                              + 1, self.pathinarchiwe + folder + '/')

    def copy_to_lfs(self, local_path):
        pass

    def copy_from_lfs(self, local_path):
        pass

    def open_file(self, name):
        return ArchFile(self.archconsole, self.path, self.pathinarchiwe + name)


