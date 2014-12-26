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

from base64 import b32encode


class VfsFileInfo(object):

    def __init__(
        self,
        path,
        name,
        size=None,
        atime=None,
        mtime=None,
        ctime=None,
        islink=None,
        uid=None,
        param=None,
        ):
        self.path = path
        self.name = name
        self.size = size
        self.atime = atime
        self.mtime = mtime
        self.ctime = ctime
        self.islink = islink
        self.uid = uid
        self.param = param
        self.id = b32encode((self.path + name).encode('utf-8'))


class VfsDirectoryInfo(object):

    def __init__(
        self,
        path,
        name,
        atime=None,
        mtime=None,
        ctime=None,
        islink=None,
        uid=None,
        param=None,
        ):
        self.path = path
        self.name = name
        self.atime = atime
        self.mtime = mtime
        self.ctime = ctime
        self.islink = islink
        self.uid = uid
        self.param = param
        self.id = b32encode((self.path + name).encode('utf-8')).decode('utf-8')


class VfsFile(object):

    def close(self):
        pass

    def read(self, size=None):
        pass

    def readline(self, size=None):
        pass

    def readlines(self):
        pass

    def write(self, str):
        pass

    def writelines(self, sequence):
        pass


class VfsDirectory(object):

    def __init__(self, parent, path):
        self.path = path
        self.parent = parent
        if parent:
            self.gparent = parent.gparent
        else:
            self.gparent = self
        self.dirs = None
        self.files = None
        self.cache = None

    def type(self):
        return ''

    def cd(self, folder):
        return None

    def cd_parent(self):
        return self.parent

    def open_file(self, name):
        return None

    def get_files(self):
        return None

    def get_dirs(self):
        return None

    def exist(self, name):
        return False

    def mk_dir(self, name):
        return False

    def rm_dir(self, name):
        return False

    def remove(self, name):
        return False

    def rename(self, oldname, newname):
        return False

    def copy_to_lfs(self, local_path):
        pass

    def copy_from_lfs(self, local_path):
        pass


class VfsPlugin(object):

    def is_virtual_dir(self, pos):
        return False

    def cd(
        self,
        parent,
        basepath,
        pos,
        ):
        return None

    def empty_file_in_lfs(self, local_path, file_name):
        return None


