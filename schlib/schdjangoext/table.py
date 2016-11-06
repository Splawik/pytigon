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

from schlib.schtools import schjson
cmd_info = 1
cmd_page = 2
cmd_count = 3
cmd_sync = 4
cmd_auto = 5
cmd_recasstr = 6
cmd_exec = 7


class Table:

    def __init__(self):
        self.AutoCols = []
        self.ColLength = [0]
        self.ColNames = ['ID']
        self.ColTypes = ['int']
        self.DefaultRec = [0]

    def _info(self):
        return schjson.dumps({
            'AutoCols': self.AutoCols,
            'ColLength': self.ColLength,
            'ColNames': self.ColNames,
            'ColTypes': self.ColTypes,
            'DefaultRec': self.DefaultRec,
            })

    def _page(
        self,
        nr,
        sort=None,
        value=None,
        ):
        return schjson.dumps({'page': self.page(nr, sort, value)})

    def _rec_as_str(self, nr):
        return schjson.dumps({'recasstr': self.rec_as_str(nr)})

    def _count(self, value=None):
        return schjson.dumps({'count': self.count(value)})

    def _sync(
        self,
        update,
        insert,
        delete,
        ):
        if len(update) > 0:
            for rec in update:
                self.update_rec(rec)
        if len(delete) > 0:
            for nr in delete:
                self.delete_rec(nr)
        if len(insert) > 0:
            for rec in insert:
                self.insert_rec(rec)
        return 'OK'

    def _auto(
        self,
        col_name,
        col_names,
        rec,
        ):
        return schjson.dumps({'rec': self.Auto(col_name, col_names, rec)})

    def _exec(self, value=None):
        ret = self.exec_command(value)
        if ret.__class__ == dict:
            return schjson.dumps(ret)
        else:
            return ret

    def page(
        self,
        nr,
        sort=None,
        value=None,
        ):
        pass

    def count(self, value):
        pass

    def rec_as_str(self, nr):
        pass

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
        pass

    def command(self, cmd_dict):
        if 'cmd' in cmd_dict:
            cmd = cmd_dict['cmd']
        else:
            cmd = cmd_page
            cmd_dict = {}
            cmd_dict['nr'] = 0
        if cmd == cmd_info:
            return self._info()
        if cmd == cmd_page:
            if 'value' in cmd_dict:
                value = cmd_dict['value']
            else:
                value = None
            if 'sort' in cmd_dict:
                return self._page(int(cmd_dict['nr']), cmd_dict['sort'], value=value)
            else:
                return self._page(int(cmd_dict['nr']), value=value)
        if cmd == cmd_count:
            if 'value' in cmd_dict:
                value = cmd_dict['value']
            else:
                value = None
            return self._count(value)
        if cmd == cmd_sync:
            return self._sync(schjson.loads(cmd_dict['update']),
                              schjson.loads(cmd_dict['insert']),
                              schjson.loads(cmd_dict['delete']))
        if cmd == cmd_auto:
            return self._auto(cmd_dict['col_name'], cmd_dict['col_names'],
                              cmd_dict['rec'])
        if cmd == cmd_recasstr:
            return self._rec_as_str(int(cmd_dict['nr']))
        if cmd == cmd_exec:
            if 'value' in cmd_dict:
                value = cmd_dict['value']
            else:
                value = None
            return self._exec(value)
        return None


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


class TablePy(Table):

    def __init__(
        self,
        table,
        col_names,
        col_typ,
        col_length,
        default_rec,
        ):
        self.Tab = table
        self.AutoCols = []
        self.ColLength = col_length
        self.ColNames = ['ID'] + col_names
        self.ColTypes = ['int'] + col_typ
        self.DefaultRec = [0] + default_rec

    def page(
        self,
        nr,
        sort=None,
        value=None,
        ):
        tab = []
        i = 0
        tab2 = self.Tab[nr * 256:(nr + 1) * 256]
        for rec in tab2:
            tab.append([nr * 256 + i] + rec)
            i += 1
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

    def count(self, value=None):
        return len(self.Tab)

    def insert_rec(self, rec):
        self.Tab.append(rec[1:])

    def update_rec(self, rec):
        self.Tab[rec[0]] = rec[1:]

    def delete_rec(self, nr):
        self.Tab.pop(nr)

    def auto(
        self,
        col_name,
        col_names,
        rec,
        ):
        pass


