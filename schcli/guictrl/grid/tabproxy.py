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

#author: "Sławomir Chołaj (slawomir.cholaj@gmail.com)"
#copyright: "Copyright (C) ????/2012 Sławomir Chołaj"
#license: "LGPL 3.0"
#version: "0.1a"

import sys

import wx

from schlib.schtools import schjson

_ = wx.GetTranslation


CMD_INFO = 1
CMD_PAGE = 2
CMD_COUNT = 3
CMD_SYNC = 4
CMD_AUTO = 5
CMD_RECASSTR = 6
CMD_EXEC = 7


def process_post_parm(obj):
    ret = {}
    for (key, value) in list(obj.items()):
        ret[key] = schjson.dumps(value)
    return ret


class DataProxy:

    def __init__(self, http, tabaddress):
        self.max_count = 1000000
        self.var_count = -1
        self.tabaddress = tabaddress
        self.tabaddress0 = self.tabaddress
        self.parm = ""
        self.parent = None
        self.http = http
        self.col_types2 = []
        self.parm = dict()
        self.is_valid = True

        self.http.post(self.parent, self.tabaddress, process_post_parm({'cmd': CMD_INFO, }))
        ret = schjson.loads(self.http.str())
        self.http.clear_ptr()

        self.col_names = ret["col_names"]
        self.col_types = ret["col_types"]
        self.default_rec = ret["default_rec"]
        self.col_size = ret["col_length"]

        for i in range(0, len(self.col_size)):
            if (self.col_size)[i] > 32:
                (self.col_size)[i] = 32

        self.auto_cols = ret["auto_cols"]

        for col in self.col_types:
            self.col_types2.append(col.split(":")[0])

        self.tab_conw = {"long": self.conw_long, "string": self.conw_none, "double": self.conw_float,
            "bool": self.conw_bool, "choice": self.conw_none, "x": self.conw_none}

    def set_parent(self, parent):
        self.parent = parent

    def set_address(self, address):
        self.tabaddress = self.tabaddress0 + address

    def get_address(self):
        return self.tabaddress

    def set_address_parm(self, parm):
        if self.parm == parm:
            return False
        else:
            self.parm = parm
            return True

    def get_address_parm(self):
        return self.parm

    def conw_long(self, l):
        if l:
            return int(l)
        else:
            return None

    def conw_none(self, n):
        if n != None:
            return n
        else:
            return ""

    def conw_float(self, f):
        if f:
            return float(f)
        else:
            return None

    def conw_bool(self, b):
        if b:
            return bool(b)
        else:
            return None

    def _reformat_rec(self, rec):
        ret = []
        i = 0
        for col in rec:
            ret.append((self.tab_conw)[(self.col_types2)[i]](col))
            i = i + 1
        return ret

    def set_parm(self, key, value):
        (self.parm)[key] = value

    def get_page(self, nrPage):
        c = {'cmd': CMD_PAGE, 'nr': nrPage}
        if self.parm:
            for (key, value) in list(self.parm.items()):
                c[key] = value
        self.http.post(self.parent, self.tabaddress, process_post_parm(c))

        page = schjson.loads(self.http.str())
        try:
            retpage = page["page"]
        except:
            retpage = None
            from schlib.schhttptools.httperror import http_error
            http_error(wx.GetApp().GetTopWindow(), self.http.str())
        self.http.clear_ptr()
        return retpage


    def get_max_count(self):
        return self.max_count

    def get_count(self):
        parm = {'cmd': CMD_COUNT}
        if 'value' in self.parm:
            parm['value']=self.parm['value']
        self.http.post(self.parent, self.tabaddress, process_post_parm(parm))
        s = self.http.str()
        ret = schjson.loads(s)
        self.http.clear_ptr()
        self.max_count = int(ret["count"])
        return self.max_count

    def sync_data(self, listaRecUpdate, listaRecInsert, listaRecDelete):
        update = schjson.dumps(listaRecUpdate)
        insert = schjson.dumps(listaRecInsert)
        delete = schjson.dumps(listaRecDelete)
        c = {'cmd': CMD_SYNC, 'update': update, 'insert': insert, 'delete': delete}
        self.http.post(self.parent, self.tabaddress, process_post_parm(c))
        self.http.clear_ptr()

    def auto_update(self, col_name, col_names, rec):
        """Return transformed row after current row is changed"""

        col_name2 = schjson.dumps(col_name)
        col_names2 = schjson.dumps(col_names)
        rec2 = schjson.dumps(rec)

        c = {'cmd': CMD_AUTO, 'col_name': col_name2, 'col_names': col_names2, "rec": rec2}

        self.http.post(self.parent, self.tabaddress, process_post_parm(c))
        ret = schjson.loads(self.http.str())
        self.http.clear_ptr()
        if ret == None:
            return rec
        else:
            return ret["rec"]

    def clone(self):
        c = DataProxy(self.http, self.tabaddress)
        c.set_address_parm(self.get_address_parm())
        return c

    def exec(self, parm):
        c = {'cmd': CMD_EXEC, 'value': parm}
        self.http.post(self.parent, self.tabaddress, process_post_parm(c))
        ret = schjson.loads(self.http.str())
        self.http.clear_ptr()
        return ret

    def get_default_rec(self):
        return self.default_rec

    def GetRecAsStr(self, nrRec):
        self.http.post(self.parent, self.tabaddress, process_post_parm({'cmd': CMD_RECASSTR, 'nr': nrRec}))
        ret = schjson.loads(self.http.str())

        self.http.clear_ptr()

        return ret["recasstr"]

    def GetColNames(self):
        return self.col_names

    def GetAutoCols(self):
        return self.auto_cols

    def GetColTypes(self):
        return self.col_types

    def GetColSize(self):
        return self.col_size

    def GetColIcons(self):
        return None
