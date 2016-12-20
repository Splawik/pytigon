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

CMD_INFO = 1
CMD_PAGE = 2
CMD_COUNT = 3
CMD_SYNC = 4
CMD_AUTO = 5
CMD_RECASSTR = 6
CMD_EXEC = 7


class Table:
    """Base class for server table interface"""
    def __init__(self):
        self.auto_cols = []
        self.col_length = [0]
        self.col_names = ['ID']
        self.col_types = ['int']
        self.default_rec = [0]

    def _info(self):
        return schjson.dumps({
            'auto_cols': self.auto_cols,
            'col_length': self.col_length,
            'col_names': self.col_names,
            'col_types': self.col_types,
            'default_rec': self.default_rec,
            })

    def _page(self,nr,sort=None,value=None):
        return schjson.dumps({'page': self.page(nr, sort, value)})

    def _rec_as_str(self, nr):
        return schjson.dumps({'recasstr': self.rec_as_str(nr)})

    def _count(self, value=None):
        return schjson.dumps({'count': self.count(value)})

    def _sync(self,update,insert,delete):
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

    def _auto(self,col_name,col_names,rec):
        return schjson.dumps({'rec': self.auto(col_name, col_names, rec)})

    def _exec(self, value=None):
        ret = self.exec_command(value)
        if ret.__class__ == dict:
            return schjson.dumps(ret)
        else:
            return ret

    def page(self,nr,sort=None,value=None):
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

    def auto(self,col_name,col_names,rec):
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
        if cmd == CMD_INFO:
            return self._info()
        if cmd == CMD_PAGE:
            if 'value' in cmd_dict:
                value = cmd_dict['value']
            else:
                value = None
            if 'sort' in cmd_dict:
                return self._page(int(cmd_dict['nr']), cmd_dict['sort'], value=value)
            else:
                return self._page(int(cmd_dict['nr']), value=value)
        if cmd == CMD_COUNT:
            if 'value' in cmd_dict:
                value = cmd_dict['value']
            else:
                value = None
            return self._count(value)
        if cmd == CMD_SYNC:
            return self._sync(schjson.loads(cmd_dict['update']),
                              schjson.loads(cmd_dict['insert']),
                              schjson.loads(cmd_dict['delete']))
        if cmd == CMD_AUTO:
            return self._auto(cmd_dict['col_name'], cmd_dict['col_names'], cmd_dict['rec'])
        if cmd == CMD_RECASSTR:
            return self._rec_as_str(int(cmd_dict['nr']))
        if cmd == CMD_EXEC:
            if 'value' in cmd_dict:
                value = cmd_dict['value']
            else:
                value = None
            return self._exec(value)
        return None


def str_cmp(x, y, ts):
    (id, s) = ts[0]
    if x[id] > y[id]:
        return s
    if x[id] < y[id]:
        return -1 * s
    if len(ts) > 1:
        return str_cmp(x, y, ts[1:])
    else:
        return 0


class TablePy(Table):

    def __init__(self,table,col_names,col_typ,col_length,default_rec):
        self.tab = table
        self.auto_cols = []
        self.col_length = col_length
        self.col_names = ['ID'] + col_names
        self.col_types = ['int'] + col_typ
        self.default_rec = [0] + default_rec

    def page(self,nr,sort=None,value=None):
        tab = []
        i = 0
        tab2 = self.tab[nr * 256:(nr + 1) * 256]
        for rec in tab2:
            tab.append([nr * 256 + i] + rec)
            i += 1
        if sort != None:
            s = sort.split(',')
            ts = []
            for pos in s:
                if pos != '':
                    id = 0
                    ss = 0
                    if pos[0] == '-':
                        id = self.col_names.index(pos[1:])
                        ss = -1
                    else:
                        id = self.col_names.index(pos)
                        ss = 1
                    ts.append((id, ss))
            tab.sort(cmp=lambda x, y: str_cmp(x, y, ts))
        return tab

    def count(self, value=None):
        return len(self.tab)

    def insert_rec(self, rec):
        self.tab.append(rec[1:])

    def update_rec(self, rec):
        self.tab[rec[0]] = rec[1:]

    def delete_rec(self, nr):
        self.tab.pop(nr)

    def auto(self,col_name,col_names,rec):
        pass


