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

import wx

from .gridtable_base import SchGridTableBase
from schlib.schhtml.htmlviewer import tdata_from_html
from schcli.guilib.tools import colour_to_html


class KeyForRec:
    def __init__(self, rec, tabsort):
        self.rec = rec
        self.tabsort = tabsort

    def __lt__(self, other):
        if self.rec[0].data.strip() == '-':
            return 1
        if other.rec[0].data.strip() == '-':
            return -1

        for pos in self.tabsort:
            if pos > 0:
                x = self.rec[pos - 1].data.lower() < other.rec[pos - 1].data.lower()
            else:
                x = self.rec[-1 * pos - 1].data.lower() > other.rec[-1 * pos - 1].data.lower()
            if x:
                return x
        return False


def make_key(tabsort):
    return lambda rec: KeyForRec(rec, tabsort)


class PageData(object):

    def __init__(self, parent, page_len, count, first_page):
        self.count = count
        self.page_len = page_len
        self.pages = {}
        self.pages[0] = first_page
        self.parent = parent

    def get_page(self, nr):
        href = self.parent.GetParent().get_parm_obj().address
        if '?' in href:
            addr = href + '&page=' + str(nr + 1)
        else:
            addr = href + '?page=' + str(nr + 1)
        html = self.parent.load_data_from_server(addr).decode('utf-8')
        tab = tdata_from_html(html, wx.GetApp().http)
        if tab:
            return tab[1:]
        else:
            return []

    def __getitem__(self, id):
        page = id // self.page_len
        id2 = id % self.page_len
        if page in self.pages:
            try:
                ret = self.pages[page][id2]
            except:
                ret = None
            return ret
        else:
            data = self.get_page(page)
            self.pages[page] = data
            return self.__getitem__(id)

    def sort(self, key):
        data = []
        for i in range(0, self.count):
            data.append(self.__getitem__(i))
        data.sort(key=key)
        self.pages = {}
        self.pages[0] = data
        self.page_len = self.count

    def __len__(self):
        return self.count


class SimpleDataTable(SchGridTableBase):

    def __init__(self, parent, tab):
        SchGridTableBase.__init__(self)
        self._parent=parent
        self.init_data(tab)
        self.last_row_count = len(self.data)

    def init_data(self, tab):
        self.colLabels = tab[0]
        self.dataTypes = []
        for col in self.colLabels:
            self.dataTypes.append('s')
        l = tab[0][0].data.split(':')
        self.count = len(tab) - 1
        self.per_page = 0
        if len(l) > 1:
            pages = l[1].split('/')
            if len(pages) > 1:
                self.per_page = int(pages[0])
                self.count = int(pages[1])
                self.colLabels[0].data = l[0]

        if self.per_page > 0:
            self.data = PageData(self._parent, int(self.per_page), self.count, tab[1:self.per_page + 1])
            self.simple_data = False
            if self.count > 128:
                self.auto_size = 'short'
        else:
            self.data = tab[1:]
            self.per_page = len(self.data)
            self.simple_data = True
        self.attrs = {}
        self.enabled = False

    def replace_tab(self, new_tab):
        SchGridTableBase.replace_tab(self, new_tab)
        self.init_data(new_tab)
        self.refr_count(len(new_tab)-1)

    def refresh_page_data(self, tab):
        old_data = self.data
        self.data = PageData(old_data.parent, int(self.per_page), int(len(tab) - 1), tab[1:self.per_page + 1])

    def enable(self, enabled):
        self.enabled = enabled
        if not self.simple_data:
            self.data.count = self.count

    def get_action_list(self, row, col=None):
        try:
            if col == None:
                col2 = self.GetNumberCols()
            else:
                col2 = col
            attrs = []
            td = self.data[row][col2]
            attrs.append(td.attr)
            childs = td.childs
            if childs:
                for sys_id in childs:
                    a = childs[sys_id].attrs
                    txt = ''
                    for atom in childs[sys_id].atom_list.atom_list:
                        txt += atom.data
                    a['data'] = txt
                    attrs.append(a)
            if col2!=0:
                attrs2 = self.get_action_list(row, 0)
                for pos in attrs2:
                    attrs.append(pos)
            return attrs
        except:
            return []

    def sort(self, column, append):
        SchGridTableBase.sort(self, column, append)
        if self.count < 4096:
            key = make_key(self.tabsort)
            self.data.sort(key=key)
        else:
            pass
        self.GetView().ForceRefresh()

    def get_ext_attr(self, row, col):
        try:
            tdattr = {}
            td = self.data[row][col]
            tdattr.update(td.attr)
            if td.childs:
                for sys_id in td.childs:
                    child = td.childs[sys_id]
                    tag = child.tag
                    if tag in tdattr:
                        tdattr[tag] += (child.attrs, )
                    else:
                        tdattr[tag] = (child.attrs, )
        except:
            print('GetExtAttr:', row, col)
            tdattr = None
        return tdattr

    def get_childs(self, row, col):
        try:
            td = self.data[row][col]
            return td.childs
        except:
            return None

    def filter_cmp(self, pos, key):
        if self.filter_id >= 0:
            if str(pos[self.filter_id].data).upper().startswith(key.upper()):
                return True
            else:
                return False
        else:
            return False

    def GetAttr(self,row,col,kind):
        if row >= self.GetNumberRows():
            attr = self.attr_normal
            attr.IncRef()
            return attr
        try:
            tdattr = self.data[row][col].attr
        except:
            print('<<<')
            print('rows:', self.GetNumberRows())
            print('cols:', self.GetNumberCols())
            print('len:', len(self.data[row]))
            print(self.data[row][col])
            print('Error', row, col)
            print('>>>')
        bgcolor = None
        color = None
        strong = None
        if 'bgcolor' in tdattr:
            bgcolor = tdattr['bgcolor']
            if bgcolor[0] != '#':
                bgcolor = None
        if 'color' in tdattr:
            color = tdattr['color']
            if color[0] != '#':
                color = None
        if 'strong' in tdattr:
            strong = 's'
        if self._is_sel(row):
            bgcolor = colour_to_html(self.sel_colour)
            strong = 's'
        key = ''
        key += bgcolor if bgcolor else '_'
        key += color if color else '_'
        key += strong if strong else '_'
        if key:
            if key in self.attrs:
                attr = self.attrs[key]
            else:
                attr = wx.grid.GridCellAttr()
                if bgcolor:
                    attr.SetBackgroundColour(bgcolor)
                if color:
                    attr.SetTextColour(color)
                if strong:
                    font = self.GetView().GetDefaultCellFont()
                    font.SetWeight(wx.FONTWEIGHT_BOLD)
                    attr.SetFont(font)
                self.attrs[key] = attr
        else:
            attr = self.attr_normal
        attr.IncRef()
        return attr

    def GetNumberCols(self):
        if len(self.colLabels) > 0:
            if self.no_actions:
                return len(self.colLabels)
            else:
                return len(self.colLabels)-1
        else:
            return 0

    def GetValue(self, row, col):
        try:
            ret = self.data[row][col].data
            return ret
        except IndexError:
            return ''

    def SetValue(self,row,col,value):
        try:
            self.data[row][col] = value
        except IndexError:
            self.data.append([''] * self.GetNumberCols())
            self.SetValue(row, col, value)
            msg = wx.grid.GridTableMessage(self,wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
            self.GetView().ProcessTableMessage(msg)

    def GetColLabelValue(self, col):
        return self.colLabels[col].data

    def GetTypeName(self, row, col):
        return self.dataTypes[col]

    def CanGetValueAs(self,row,col,type_name):
        col_type = self.dataTypes[col].split(':')[0]
        if type_name == col_type:
            return True
        else:
            return False

    def CanSetValueAs(self,row,col,type_name):
        return self.CanGetValueAs(row, col, type_name)
