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

from base64 import b32encode, b32decode
import binascii
from schlib.schtools import schjson
from schlib.schtools.tools import bencode, bdecode
import sys
from schlib.schdjangoext.table import Table
from schlib.schfs.vfstools import replace_dot
from django.http import HttpResponse
from django.core.cache import cache
from django.core.files.storage import default_storage

from fs.opener import fsopendir

import fs.path
from schlib.schtools.data import is_null
from schlib.schtasks.task import get_process_manager
import datetime
import re


def automount(path):
    lpath = path.lower()
    if lpath.endswith('.zip') or '.zip/' in lpath:
        id = lpath.find('.zip')
        pp = path[:id+4]

        syspath = default_storage.fs.getsyspath(pp, allow_none=True)
        if syspath:
            zip_name = 'zip://'+default_storage.fs.getsyspath(pp)
            default_storage.fs.mountdir(pp[1:], fsopendir(zip_name))
    return path


def str_cmp(x, y, ts):
    (id, znak) = ts[0]
    if x[id] > y[id]:
        return znak
    if x[id] < y[id]:
        return -1 * znak
    if len(ts) > 1:
        return str_cmp(x, y, ts[1:])
    else:
        return 0


class VfsTable(Table):

    def __init__(self, folder):
        self.var_count = -1
        self.folder = replace_dot(folder).replace('%20', ' ')
        self.AutoCols = []
        self.ColLength = [10, 10, 10]
        self.ColNames = ['ID', 'Name', 'Size', 'Created']
        self.ColTypes = ['int', 'str', 'int', 'datetime']
        self.DefaultRec = ['', 0, None]
        self.task_href = None

    def set_task_href(self, href):
        self.task_href = href

    def _size_to_color(self, size):
        colors = ((1024, '#fff'), (1048576, '#fdd'), (1073741824, '#f99,#FFF'),
                  (1099511627776, '#000,#FFF'))
        for pos in colors:
            if size < pos[0]:
                return pos[1]
        return colors[-1][1]

    def _time_to_color(self, time):
        if time:
            size = (datetime.datetime.today() - time).days
            colors = ((1, '#FFF,#F00'), (7, '#efe'), (31, '#dfd'), (365, '#cfc'), (365, '#000,#FFF'))
            for pos in colors:
                if size < pos[0]:
                    return pos[1]
            return colors[-1][1]
        else:
            return '#FFF,#F00'

    def _get_table(self, value=None):
        try:
            f = default_storage.fs.listdir(automount(self.folder))
        except:
            return []

        elements = []
        files = []
        if value:
            cmp = re.compile(value, re.IGNORECASE)
        else:
            cmp = None

        if self.folder!='/':
            f = ['..',] + f
        for p in f:
            pos = fs.path.join(self.folder, p)
            if default_storage.fs.isdir(pos) or p.lower().endswith('.zip'):
                if cmp and cmp.match(p) or not cmp:
                    id = b32encode(pos.encode('utf-8')).decode('utf-8')
                    info = default_storage.fs.getinfo(pos)
                    if not 'created_time' in info:
                        info['created_time'] = ''
                    elements.append([
                        id,
                        (p, ',#fdd'),
                        '',
                        (info['created_time'], ',,#f00,s'),
                        info,
                        {'edit': ('tableurl', '../../%s//' % id, 'Change folder')},
                    ])
            else:
                files.append((p, pos))
        for pp in files:
            p=pp[0]
            pos=pp[1]
            if cmp and cmp.match(p) or not cmp:
                id = b32encode(pos.encode('utf-8')).decode('utf-8')
                info = default_storage.fs.getinfo(pos)
                size = info['size']
                ctime = info['created_time']
                elements.append([
                    id,
                    p,
                    (size, '>,' + self._size_to_color(size)),
                    (ctime, ',' + self._time_to_color(ctime)),
                    info,
                    {'edit': ('command', '../../%s//' % id, 'Open file')},
                    ])
        return elements

    def page(
        self,
        nr,
        sort=None,
        value=None,
        ):
        key = 'FOLDER_' + b32encode(self.folder.encode('utf-8')).decode('utf-8') + '_TAB'

        #tabvalue = cache.get(key + '::' + is_null(value, ''))
        tabvalue = None

        if tabvalue:
            tab = tabvalue
        else:
            tab = self._get_table(value)[nr * 256:(nr + 1) * 256]
            cache.set(key + '::' + is_null(value, ''), tab, 300)

        self.var_count = len(tab)
        if sort != None:
            s = sort.split(',')
            ts = []
            for pos in s:
                if pos != '':
                    id = 0
                    znak = 0
                    if pos[0] == '-':
                        id = self.ColNames.index(pos[1:])
                        znak = -1
                    else:
                        id = self.ColNames.index(pos)
                        znak = 1
                    ts.append((id, znak))
            tab.sort(cmp=lambda x, y: str_cmp(x, y, ts))
        return tab

    def count(self, value):
        key = 'FOLDER_' + b32encode(self.folder.encode('utf-8')).decode('utf-8') + '_COUNT'
        countvalue = cache.get(key + '::' + is_null(value, ''))

        if countvalue:
            return countvalue
        else:
            countvalue = len(self._get_table(value))
            cache.set(key + '::' + is_null(value, ''), countvalue, 300)
            return countvalue

        return len(self._get_table(value))

    def insert_rec(self, rec):
        pass

    def update_rec(self, rec):
        pass

    def delete_rec(self, nr):
        pass

    def auto(
        self,
        col_name,
        col_names,
        rec,
        ):
        pass

    def exec_command(self, value):
        """format pliku exec:
        COPY(source_folder, dest_folder, files, mask);
        DEL(source_folder, files);
        MKDIR(source_folder, folder_name);
        MOVE(source_folder, dest_folder, files, mask):
        RENAME(source_path, new_name);
        NEWFILE(source_path, new_name);
        """

        print(value)

        thread_commands = ('COPY', 'MOVE', 'DELETE')
        if value[0] in thread_commands:
            parm = {}
            parm["cmd"] = value[0]
            parm["files"] = b32decode(value[1][0])
            parm["dest"] = b32decode(value[2][1])
            task_manager = get_process_manager(self.task_href if self.task_href else '127.0.0.1:8080')
            _id = task_manager.put('system', parm["cmd"], "@schlib.schfs:filesystemcmd", user_parm = parm)
            c = { 'process': _id }
        elif value[0] == 'MKDIR':
            path = bdecode(value[2][0])
            name = bdecode(value[2][1])
            default_storage.fs.makedir(path+"/"+name)
            c = {}
        elif value[0] == 'NEWFILE':
            path = bdecode(value[2][0])
            name = bdecode(value[2][1])
            default_storage.fs.createfile(path+"/"+name)
            c = {}
        elif value[0] == 'RENAME':
            source = bdecode(value[1][0])
            path = bdecode(value[2][0])
            name = bdecode(value[2][1])
            default_storage.fs.rename(source, path+"/"+name)
            c = {}
        else:
            c = { }
        return c


def vfstable_view(request, folder, value=None):
    if request.POST:
        p = request.POST.copy()
        d = {}
        for (key, val) in list(p.items()):
            if key != 'csrfmiddlewaretoken':
                d[str(key)] = schjson.loads(val)
    else:
        d = {}
    if value and value != '' and value != '_':
        d['value'] = b32decode(value.encode('utf-8')).decode('utf-8')
    if folder and folder != '' and folder != '_':
        folder2 = b32decode(folder.encode('utf-8')).decode('utf-8')
    else:
        folder2 = '/'
    folder2 = replace_dot(folder2)
    tabview = VfsTable(folder2)
    retstr = tabview.command(d)
    return HttpResponse(retstr)


def vfsopen(request, file):
    try:
        try:
            file2 = b32decode(file).decode('utf-8')
        except:
            file2 = b32decode(file.encode('utf-8')).decode('utf-8')


        plik = default_storage.fs.open(automount(file2),'rb')
        buf = plik.read()
        plik.close()
    except:
        buf = ''
    return HttpResponse(buf)


def vfsopen_page(request, file, page):
    try:
        file2 = b32decode(file).decode('utf-8')
        page2 = int(page)
        plik = default_storage.fs.open(automount(file2),'rb')
        try:
            plik.seek(page2 * 4096)
            buf = binascii.hexlify(plik.read(4096))
            plik.close()
        except:
            buf = ''
    except:
        buf = ''
    return HttpResponse(buf)


def vfssave(request, file):
    buf = 'ERROR'
    plik = None
    if request.POST:
        try:
            data = request.POST['data']
            file2 = b32decode(file).decode('utf-8')
            plik = default_storage.fs.open(automount(file2),"w")
            plik.write(data)
            plik.close()
            buf = 'OK'
        except:
            buf = 'ERROR: ' + str(sys.exc_info()[0])
            if plik:
                plik.close()
    return HttpResponse(buf)
