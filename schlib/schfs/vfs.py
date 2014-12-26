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

from django.utils.translation import ugettext_lazy as _

from .lfs import Directory
import shutil
import sys
import os
from .vfsplugin import VfsDirectoryInfo
from schlib.schfs.vfstools import Cmp
from .trash import DeleteToTrash
import string


class VfsManager(object):

    def __init__(self):
        self.plugins = []
        self.trash = DeleteToTrash()

    def _lfs_copy_file(self, source, desc):
        try:
            shutil.copy(source, desc)
        except:
            return (False, sys.exc_info()[0])
        return (True, 'OK')

    def _lfs_move_file(self, source, desc):
        try:
            shutil.move(source, desc)
        except:
            return (False, sys.exc_info()[0])
        return (True, 'OK')

    def _lfs_del_file(self, source, desc):
        try:
            self.trash.delete(source)
        except:
            return (False, sys.exc_info()[0])
        return (True, 'OK')

    def _lfs_copy_dir(self, source, desc):
        try:
            shutil.copytree(source, desc)
        except:
            return (False, sys.exc_info()[0])
        return (True, 'OK')

    def _lfs_move_dir(self, source, desc):
        try:
            shutil.move(source, desc)
        except:
            return (False, sys.exc_info()[0])
        return (True, 'OK')

    def _lfs_del_dir(self, source, desc):
        try:
            if source[-1] == '/':
                self.trash.delete(source[:-1])
            else:
                self.trash.delete(source)
        except:
            return (False, sys.exc_info()[0])
        return (True, 'OK')

    def _copy(
        self,
        cmd,
        parent,
        source_path,
        dest_path,
        source_files=None,
        source_masks=None,
        source_key=None,
        desc_file=None,
        ):
        sdir = self.get_dir(source_path)
        ddir = self.get_dir(dest_path)
        if sdir and ddir:
            if sdir.type() == 'lfs' and ddir.type() == 'lfs':
                if source_files == None and source_masks == None and source_key == None:
                    if desc_file == None:
                        desc = sdir.path.split('/')[-1]
                    else:
                        desc = desc_file
                    cmd['fun_dir'](sdir.path, ddir.path + desc)
                else:
                    x = {   'progress': 0,
                            'description': cmd['start_description'],
                            'template': 'schcommander/copyprogress.html',
                            'exit': 0,
                        }
                    if parent:
                        parent.WriteInfo(x)
                        parent.WriteData(x, True)
                    c = Cmp(source_masks, source_key, convert_to_re=True)
                    dir = sdir.get_dirs()
                    files = sdir.get_files()
                    count = len(dir) + len(files)
                    i = 0
                    for directory in sdir.get_dirs():
                        x = {'progress': (i * 100) / count,
                             'description': cmd['info_dir_description']}
                        if parent:
                            parent.WriteInfo(x)
                        if c.filter(directory.name) or source_files and directory.name in source_files:
                            (ret, info_str) = cmd['fun_dir'](source_path + '/' + directory.name + '/', dest_path + '/'
                                     + directory.name + '/')
                            if ret:
                                x = {
                                    'progress': (i * 100) / count,
                                    'description': cmd['data_dir_description']\
                                         % (directory.name, dest_path + '/'),
                                    'template': cmd['template'],
                                    'exit': 0,
                                    }
                            else:
                                x = {
                                    'progress': (i * 100) / count,
                                    'description': cmd['data_dir_error']\
                                         % (directory.name, info_str),
                                    'template': cmd['template'],
                                    'exit': 0,
                                    }
                            if parent:
                                parent.WriteData(x, True)
                        if parent.exit:
                            return 0
                        i += 1
                    for file in sdir.get_files():
                        x = {'progress': (i * 100) / count,
                             'description': cmd['info_file_description']}
                        if parent:
                            parent.WriteInfo(x)
                        if c.filter(file.name) or source_files and file.name in source_files:
                            (ret, info_str) = cmd['fun_file'](source_path + '/'
                                     + file.name, dest_path + '/')
                            if ret:
                                x = {
                                    'progress': (i * 100) / count,
                                    'description': cmd['data_file_description']\
                                         % (file.name, dest_path + '/'),
                                    'template': cmd['template'],
                                    'exit': 0,
                                    }
                            else:
                                x = {
                                    'progress': (i * 100) / count,
                                    'description': cmd['data_file_error']\
                                         % (file.name, info_str),
                                    'template': cmd['template'],
                                    'exit': 0,
                                    }
                            if parent:
                                parent.WriteData(x, True)
                        if parent.exit:
                            return 0
                        i += 1
                    x = {
                        'progress': 100,
                        'description': cmd['end_description'],
                        'template': cmd['template'],
                        'exit': True,
                        }
                    if parent:
                        parent.WriteInfo(x)
                        parent.WriteData(x, True)
            elif sdir.type() == 'lfs':
                ddir.copy_from_lfs(source_path, source_files)
            elif ddir.type() == 'lfs':
                sdir.copy_to_lfs(dest_path, desc_file)
            else:
                pass

    def get_dir(self, path):
        return get_dir(path, self)

    def is_virtual_dir(self, pos):
        for plugin in self.plugins:
            if plugin.is_virtual_dir(pos):
                return True
        return False

    def cd(
        self,
        parent,
        basepath,
        pos,
        ):
        for plugin in self.plugins:
            if plugin.is_virtual_dir(pos):
                return plugin.cd(parent, basepath, pos)

    def copy(
        self,
        parent,
        source_path,
        dest_path,
        source_files=None,
        source_masks=None,
        source_key=None,
        desc_file=None,
        ):
        cmd = {
            'fun_file': self._lfs_copy_file,
            'fun_dir': self._lfs_copy_dir,
            'template': 'schcommander/copyprogress.html',

            'start_description': _('Start copying'),
            'info_file_description': _('Copying files'),
            'info_dir_description': _('Copying folders'),
            'data_file_description': _('Copying file: %s to folder: %s'),
            'data_file_error': _('Error in copying file: %s - %s'),
            'data_dir_description': _('Copying folder: %s to folder: %s'),
            'data_dir_error': _('Error in copying folder: %s - %s'),
            'end_description': _('The end of the copy'),
            }
        return self._copy(
            cmd,
            parent,
            source_path,
            dest_path,
            source_files,
            source_masks,
            source_key,
            desc_file,
            )

    def move(
        self,
        parent,
        source_path,
        dest_path,
        source_files=None,
        source_masks=None,
        source_key=None,
        desc_file=None,
        ):
        cmd = {
            'fun_file': self._lfs_move_file,
            'fun_dir': self._lfs_move_dir,
            'template': 'schcommander/copyprogress.html',

            'start_description': _('Start moving'),
            'info_file_description': _('Moving files'),
            'info_dir_description': _('Moving folders'),
            'data_file_description': _('Moving file: %s to folder: %s'),
            'data_file_error': _('Error in moving file: %s - %s'),
            'data_dir_description': _('Moving folder: %s to folder: %s'),
            'data_dir_error': _('Error in moving folder: %s - %s'),
            'end_description': _('The end of transmission'),
            }
        return self._copy(
            cmd,
            parent,
            source_path,
            dest_path,
            source_files,
            source_masks,
            source_key,
            desc_file,
            )

    def delete(
        self,
        parent,
        source_path,
        dest_path,
        source_files=None,
        source_masks=None,
        source_key=None,
        desc_file=None,
        ):
        cmd = {
            'fun_file': self._lfs_del_file,
            'fun_dir': self._lfs_del_dir,
            'template': 'schcommander/copyprogress.html',

            'start_description': _('Start erasing'),
            'info_file_description': _('Erasing files'),
            'info_dir_description': _('Erasing folders'),
            'data_file_description': _('Erasing file: %s to folder: %s'),
            'data_file_error': _('Error in erasing file: %s - %s'),
            'data_dir_description': _('Erasing folder: %s to folder: %s'),
            'data_dir_error': _('Error in erasing folder: %s - %s'),
            'end_description': _('The end of removal'),
            }
        return self._copy(
            cmd,
            parent,
            source_path,
            dest_path,
            source_files,
            source_masks,
            source_key,
            desc_file,
            )

    def empty_file_in_lfs(self, lfs_path, file_name):
        for plugin in self.plugins:
            if plugin.is_virtual_dir(lfs_path + '/' + file_name):
                return plugin.empty_file_in_lfs(lfs_path, file_name)
        return False

    def install_plugin(self, plugin):
        self.plugins.append(plugin)


class MainDir(Directory):

    def __init__(self, vsfmanager):
        self.vsfmanager = vsfmanager
        Directory.__init__(self, '', '')

    def get_files(self):
        return []

    def get_dirs(self):
        if sys.platform.startswith('win'):
            drives = []
            for c in string.lowercase:
                if os.path.isdir(c + ':'):
                    drives.append(VfsDirectoryInfo('', c + ':/'))
            return drives
        else:
            return [VfsDirectoryInfo('', '/')]

    def cd(self, folder):
        if ':' in folder:
            return Directory(self, folder + '/')
        else:
            return Directory(self, folder)

    def cd_parent(self):
        return None


def get_dir(path, vfsmanager):
    d = MainDir(vfsmanager)
    if path == '' or path == None:
        return d
    tabpath = path.replace('\\', '/').split('/')
    if tabpath[0] == '':
        d = d.cd('/')
        tabpath = tabpath[1:]
    for pos in tabpath:
        if pos != '':
            d = d.cd(pos)
    return d


def open_file(file_name, vfsmanager):
    id = file_name.rfind('/')
    if id >= 0:
        directory = file_name[:id + 1]
        name = file_name[id + 1:]
        d = get_dir(directory, vfsmanager)
        f = d.open_file(name)
        return f
    else:
        return None


if __name__ == '__main__':
    from .zip import VfsPluginZip
    from base64 import b32encode, b32decode
    from .vfstools import ReplaceDot
    man = Vfsmanager()
    man.install_plugin(VfsPluginZip())
    x = get_dir('c:/home/scholaj/', man)
    dirs = x.get_dirs()
    print(dirs)
    for pos in dirs:
        print(pos.name, pos.path)
    files = x.get_files()
    for pos in files:
        print(pos.name, pos.path)
    print(ReplaceDot(b32decode(dirs[0].id)))
