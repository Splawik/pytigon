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

import wx
import wx.html
import wx.grid as gridlib
from .datasource import *
from .schgrid import *
import sys
from schlib.schtools import schjson


cmd_info = 1
cmd_page = 2
cmd_count = 3
cmd_sync = 4
cmd_auto = 5
cmd_recasstr = 6
cmd_exec = 7


class string(str):
    pass


class double(float):
    pass


class choice(str):
    pass


def ProcessPostParm(obj):
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

        self.Http = http

        self.Http.get(self.parent, self.tabaddress, ProcessPostParm({'cmd': cmd_info, }))

        ret = schjson.loads(self.Http.str())

        self.Http.clear_ptr()

        self.col_names = ret["ColNames"]
        self.col_types = ret["ColTypes"]
        self.default_rec = ret["DefaultRec"]

        self.col_size = ret["ColLength"]

        for i in range(0, len(self.col_size)):
            if (self.col_size)[i] > 32:
                (self.col_size)[i] = 32

        self.auto_cols = ret["AutoCols"]

        self.col_types2 = []
        for col in self.col_types:
            self.col_types2.append(col.split(":")[0])
        self.tab_conw = {"long": self.conw_long, "string": self.conw_none, "double": self.conw_float, "bool": self.conw_bool,
                        "choice": self.conw_none, "x": self.conw_none}
        self.parm = dict()
        self.is_valid = True

    def SetParent(self, parent):
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
        c = {'cmd': cmd_page, 'nr': nrPage}
        if self.parm:
            for (key, value) in list(self.parm.items()):
                c[key] = value
        self.Http.get(self.parent, self.tabaddress, ProcessPostParm(c))

        #try:
        if True:
            page = schjson.loads(self.Http.str())

            try:
                retpage = page["page"]
            except:
                retpage = None
                from schlib.schhttptools.htmltools import HtmlErrorDialog
                dlg = HtmlErrorDialog(wx.GetApp().GetTopWindow(), -1, "Sample Dialog", self.Http.str(), size=(800, 600),
                                      style=wx.DEFAULT_DIALOG_STYLE)
                dlg.CenterOnScreen()
                val = dlg.ShowModal()
                if val == wx.ID_CANCEL:
                    sys.exit()
        #except:
        #    retpage = None

        self.Http.clear_ptr()
        return retpage

    def GetRecAsStr(self, nrRec):
        self.Http.get(self.parent, self.tabaddress, ProcessPostParm({'cmd': cmd_recasstr, 'nr': nrRec}))
        ret = schjson.loads(self.Http.str())

        self.Http.clear_ptr()

        return ret["recasstr"]

    def GetColNames(self):
        return self.col_names

    def GetAutoCols(self):
        return self.auto_cols

    def GetDefaultRec(self):
        return self.default_rec

    def GetColTypes(self):
        return self.col_types

    def GetColSize(self):
        return self.col_size

    def GetColIcons(self):
        return None

    def get_max_count(self):
        return self.max_count

    def GetCount(self):
        parm = {'cmd': cmd_count}
        if 'value' in self.parm:
            parm['value']=self.parm['value']
        self.Http.get(self.parent, self.tabaddress, ProcessPostParm(parm))
        #print "Count:", self.Http.Str()
        s = self.Http.str()
        #print(s)
        ret = schjson.loads(s)
        #ret = schjson.loads(self.Http.Str())
        self.Http.clear_ptr()
        self.max_count = int(ret["count"])
        return self.max_count
        #return int(ret["count"])

    def sync_data(self, listaRecUpdate, listaRecInsert, listaRecDelete):
        update = schjson.dumps(listaRecUpdate)
        insert = schjson.dumps(listaRecInsert)
        delete = schjson.dumps(listaRecDelete)

        c = {'cmd': cmd_sync, 'update': update, 'insert': insert, 'delete': delete}
        self.Http.get(self.parent, self.tabaddress, ProcessPostParm(c))
        self.Http.clear_ptr()

    def GetAttr(self, row, col, kind):
        return None

    def auto_update(self, col_name, col_names, rec):
        """po zmianie pozycji w kolumnie o nazwie col_name funkcja przetwarza aktualny rekord
      w wyniku zwracaj\xc4\x85 rekord przetworzony"""

        col_name2 = schjson.dumps(col_name)
        col_names2 = schjson.dumps(col_names)
        rec2 = schjson.dumps(rec)

        c = {'cmd': cmd_auto, 'col_name': col_name2, 'col_names': col_names2, "rec": rec2}

        self.Http.get(self.parent, self.tabaddress, ProcessPostParm(c))
        ret = schjson.loads(self.Http.str())
        self.Http.clear_ptr()
        if ret == None:
            return rec
        else:
            return ret["rec"]

    def clone(self):
        c = DataProxy(self.Http, self.tabaddress)
        c.set_address_parm(self.get_address_parm())
        return c

    def exec(self, parm):
        c = {'cmd': cmd_exec, 'value': parm}
        self.Http.get(self.parent, self.tabaddress, ProcessPostParm(c))
        #self.Http.ClearPtr()
        #print "Exec ret:", self.Http.Str()
        ret = schjson.loads(self.Http.str())
        self.Http.clear_ptr()
        return ret
