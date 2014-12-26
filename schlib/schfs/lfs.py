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
import sys
from os.path import getsize, getatime, getmtime, getctime, islink, exists
from stat import ST_UID
import time
from .vfsplugin import VfsDirectory, VfsFile, VfsDirectoryInfo, VfsFileInfo


def _to_time(fun, t):
    try:
        t1 = fun(t)
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t1))
    except:
        return ''


class LfsFile(VfsFile):

    def __init__(self, file_name):
        self.file_name = file_name
        self.file = None

    def _get_file(self, forwrite=False):
        if not self.file:
            if forwrite:
                self.file = open(self.file_name, 'wb')
            else:
                self.file = open(self.file_name, 'rb')
        return self.file

    def close(self):
        self._get_file().close()

    def seek(self, nr):
        return self._get_file().seek(nr)

    def read(self, size=None):
        if size:
            return self._get_file().read(size)
        else:
            return self._get_file().read()

    def readline(self, size=None):
        if size:
            return self._get_file().readline(size)
        else:
            return self._get_file().readline()

    def readlines(self):
        return self._get_file().readlines()

    def write(self, str):
        return self._get_file(forwrite=True).write(str)

    def writelines(self, sequence):
        return self._get_file(forwrite=True).writelines(sequence)


class Directory(VfsDirectory):

    def __init__(self, parent, path):
        VfsDirectory.__init__(self, parent, path)

    def _get_all(self):
        try:
            if sys.platform.startswith('win'):
                ret = [x.decode('cp1250') for x in
                       os.listdir(self.path.encode('cp1250'))]
            else:
                ret = [x for x in os.listdir(self.path)]
        except:
            ret = []
        return ret

    def type(self):
        return 'lfs'

    def get_dirs(self):
        if not self.dirs:
            if self.parent:
                self.dirs = [VfsDirectoryInfo(self.path, '..')]
            else:
                self.dirs = []
            for pos in self._get_all():
                name = os.path.join(self.path, pos)
                if not os.path.isfile(name):
                    self.dirs.append(VfsDirectoryInfo(self.path, pos,
                                     _to_time(getatime, name),
                                     _to_time(getmtime, name),
                                     _to_time(getctime, name)))
                else:
                    if self.gparent.vsfmanager.is_virtual_dir(pos):
                        self.dirs.append(VfsDirectoryInfo(self.path, pos,
                                _to_time(getatime, name), _to_time(getmtime,
                                name), _to_time(getctime, name)))
        return self.dirs

    def get_files(self):
        if not self.files:
            try:
                self.files = []
                for pos in self._get_all():
                    name = os.path.join(self.path, pos)
                    if os.path.isfile(name):
                        if not self.gparent.vsfmanager.is_virtual_dir(pos):
                            stat = os.stat(name)
                            self.files.append(VfsFileInfo(
                                self.path,
                                pos,
                                getsize(name),
                                _to_time(getatime, name),
                                _to_time(getmtime, name),
                                _to_time(getctime, name),
                                islink(name),
                                stat[ST_UID],
                                ))
            except:
                import traceback
                print(pos.__class__.__name__)
                print(pos)
                traceback.print_exc()
        return self.files

    def cd(self, folder):
        if os.path.isfile(os.path.join(self.path, folder)):
            return self.gparent.vsfmanager.cd(self, self.path, folder)
        else:
            return Directory(self, self.path + folder + '/')

    def remove(self, name):
        os.remove(self.path + name)
        return False

    def exists(self, name):
        return exists(self.path + name)

    def rename(self, oldname, newname):
        if not self.exists(newname):
            return os.rename(self.path + oldname, self.path + newname)
        else:
            return False

    def mk_dir(self, name):
        if self.gparent.vsfmanager.is_virtual_dir(self.path + '/' + name):
            return self.gparent.vsfmanager.empty_file_in_lfs(self.path, name)
        else:
            os.mkdir(self.path + '/' + name)
            return True

    def open_file(self, name):
        return LfsFile(self.path + name)


