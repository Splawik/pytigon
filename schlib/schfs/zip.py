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

from .vfsplugin import VfsPlugin, VfsDirectory, VfsFile, VfsDirectoryInfo, \
    VfsFileInfo
from .lfs import LfsFile
import os
import tempfile
import zipfile
import time


class ZipFile(LfsFile):

    def __init__(self, file_name, zip_file_name):
        LfsFile.__init__(self, file_name)
        self.temp_file_name = None
        self.zip_file_name = zip_file_name
        self.for_write = False
        self.zip_handle = None

    def _get_file(self, forwrite=False):
        if not self.file:
            self.for_write = forwrite
            if forwrite:
                file = tempfile.mkstemp()
                self.temp_file_name = file[1]
                self.file = os.fdopen(file[0], 'w')
            else:
                self.zip_handle = zipfile.ZipFile(self.file_name[:-1])
                self.file = self.zip_handle.open(self.zip_file_name)
        return self.file

    def _write_to_zip(
        self,
        zip_name,
        in_file_name,
        zip_file_name,
        ):
        zip_handle = zipfile.ZipFile(zip_name, 'a')
        zip_handle.write(in_file_name, zip_file_name)
        zip_handle.close()

    def close(self):
        if self.file:
            self.file.close()
        if self.for_write:
            self._write_to_zip(self.file_name[:-1], self.temp_file_name,
                               self.zip_file_name)
        else:
            if self.zip_handle:
                self.zip_handle.close()


class ZipDirectory(VfsDirectory):

    def __init__(
        self,
        parent,
        path,
        poziom=1,
        pathinarchiwe='',
        ):
        VfsDirectory.__init__(self, parent, path)
        self.poziom = poziom
        self.pathinarchiwe = pathinarchiwe

    def _get_all(self):
        if not self.cache:
            self.cache = []
            f = zipfile.ZipFile(self.path[:-1])
            self.cache = f.infolist()
        return self.cache

    def _transform_poziom(self, name):
        x = name.split('/')
        if len(x) != self.poziom:
            return None
        else:
            if name.startswith(self.pathinarchiwe):
                return x[-1]

    def type(self):
        return 'zip'

    def get_dirs(self):
        if not self.dirs:
            if self.parent:
                self.dirs = [VfsDirectoryInfo(self.path + self.pathinarchiwe,
                             '..')]
            else:
                self.dirs = []
            for pos in self._get_all():
                if pos.filename[-1] == '/':
                    p = self._transform_poziom(pos.filename[:-1])
                    if p:
                        self.dirs.append(VfsDirectoryInfo(self.path
                                 + self.pathinarchiwe, p))
        return self.dirs

    def get_files(self):
        if not self.files:
            self.files = []
            for pos in self._get_all():
                if not pos.filename[-1] == '/':
                    p = self._transform_poziom(pos.filename)
                    if p:
                        self.files.append(VfsFileInfo(self.path
                                 + self.pathinarchiwe, p))
        return self.files

    def cd(self, folder):
        return ZipDirectory(self, self.path, self.poziom + 1, self.pathinarchiwe
                             + folder + '/')

    def copy_to_lfs(self, local_path):
        pass

    def copy_from_lfs(self, local_path):
        pass

    def open_file(self, name):
        return ZipFile(self.path, self.pathinarchiwe + name)


class VfsPluginZip(VfsPlugin):

    def is_virtual_dir(self, pos):
        if pos[-4:].lower() in ('.zip', '.jar'):
            return True
        else:
            return False

    def cd(
        self,
        parent,
        basepath,
        pos,
        ):
        return ZipDirectory(parent, basepath + pos + '/')

    def empty_file_in_lfs(self, local_path, file_name):
        zip_handle = zipfile.ZipFile(local_path + '/' + file_name, 'w')
        now = time.localtime(time.time())[:6]
        info = zipfile.ZipInfo('$$$')
        info.date_time = now
        info.compress_type = zipfile.ZIP_DEFLATED
        zip_handle.writestr(info, '')
        zip_handle.close()
        return True


