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
from wx.grid import GridCellAttr, GridTableMessage, GRIDTABLE_NOTIFY_ROWS_DELETED, GRIDTABLE_NOTIFY_ROWS_APPENDED


class SchGridTableBase(wx.grid.GridTableBase):

    def __init__(self):
        wx.grid.GridTableBase.__init__(self)
        self.can_append = 0
        self.append_count = 0
        self.read_only = True
        self.rec_to_update = dict()
        self.rec_to_instert = dict()
        self.rec_to_delete = []
        self.rec_selected = []
        self.tabsort = []
        self.filter_id = None
        self.key = None
        self.sel_mask = []

        self.sel_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK)
        self.attr_insert = GridCellAttr()
        self.attr_insert.SetBackgroundColour('PALE GREEN')
        self.attr_update = GridCellAttr()
        self.attr_update.SetBackgroundColour('WHEAT')
        self.attr_del = GridCellAttr()
        self.attr_del.SetBackgroundColour('RED')
        self.attr_del.SetFont(wx.Font(8, wx.ROMAN, wx.ITALIC, wx.NORMAL, True))
        self.attr_sel = GridCellAttr()
        self.attr_sel.SetBackgroundColour(self.sel_colour)
        self.attr_sel.SetFont(wx.Font(8, wx.ROMAN, wx.ITALIC, wx.NORMAL, True))
        self.attr_normal = GridCellAttr()

        self.data = []
        self.data_org = None
        self.last_row_count = 0
        self.auto_size = 'simple'
        self.no_actions = False

        self.init_data_base()

    def init_data_base(self):
        self.append_count = 0
        self.read_only = True
        self.rec_to_update = dict()
        self.rec_to_instert = dict()
        self.rec_to_delete = []
        self.rec_selected = []
        self.data = []
        self.data_org = None
        self.last_row_count = 0

    def replace_tab(self, new_tab):
        self.refr_count(0)
        self.init_data_base()
        self.data = new_tab

    def refr_count(self, count, store_pos=0):
        if count == self.last_row_count:
            return
        old_count = self.last_row_count
        self.last_row_count = count
        self.GetView().refr_count(old_count, count, store_pos)

    def _get_number_rows(self):
        return len(self.data) + self.can_append + self.append_count

    def get_rec(self, row):
        try:
            return self.data[row]
        except IndexError:
            return []

    def get_sort_nr(self, col):
        c = col + 1
        if c in self.tabsort:
            return self.tabsort.index(c) + 1
        else:
            if -1 * c in self.tabsort:
                return -1 * self.tabsort.index(-1 * c) - 1
            else:
                return 0

    def sort(self, column, append):
        col = column + 1
        if append:
            if col in self.tabsort:
                self.tabsort.remove(col)
                self.tabsort.append(-1 * col)
            else:
                if -1 * col in self.tabsort:
                    self.tabsort.remove(-1 * col)
                else:
                    self.tabsort.append(col)
        else:
            if col in self.tabsort:
                self.tabsort = [-1 * col]
            else:
                if -1 * col in self.tabsort:
                    self.tabsort = []
                else:
                    self.tabsort = [col]

    def _is_sel(self, row):
        if row in self.rec_selected:
            return True
        return False

    def sel_row(self, row):
        if row < self.GetNumberRows():
            if row in self.rec_selected:
                self.rec_selected.remove(row)
            else:
                self.rec_selected.append(row)
            self.GetView().ForceRefresh()
            return True
        else:
            return False

    def make_exec_cmd(self, cmd, option=0):
        if option == 0:
            data = [cmd]
        elif option == 1:
            selrows = self.get_sel_rows()
            key = self.get_sel_key()
            data = [cmd, (key, ) + selrows]
        else:
            data = [cmd]
        return data

    def run_cmd(self, cmd, options):
        pass

    def get_sel_key(self):
        row = self.GetView().GetGridCursorRow()
        rec = self.get_rec(row)
        return rec[0]

    def get_sel_rows(self):
        ret = []
        for pos in self.rec_selected:
            ret.append(self.get_rec(pos)[0])
        return (ret, self.sel_mask, self.key)

    def set_read_only(self, read_only):
        self.read_only = read_only
        if self.read_only:
            self.can_append = 0
        else:
            self.can_append = 1

    def set_no_actions(self, val):
        self.no_actions = val

    def is_read_only(self, row, col):
        return self.read_only

    def filter_cmp(self, pos, key):
        if self.filter_id is not None:
            if str(pos[self.filter_id]).startswith(key):
                return True
            else:
                return False
        else:
            return False

    def filter_by(self, col):
        self.filter_id = col

    def filter(self, key):
        if self.key and self.key == key:
            return
        old_count = self.GetNumberRows()
        if key and len(key) > 0:
            if not self.data_org:
                self.data_org = self.data
            self.data = []
            for pos in self.data_org:
                if self.filter_cmp(pos, key):
                    self.data.append(pos)
        else:
            if self.data_org:
                self.data = self.data_org
                self.data_org = None
        self.key = key
        self.refr_count(old_count, self.GetNumberRows(), 0)
        self.GetView().ForceRefresh()

    def append_sel_mask(self, mask):
        self.sel_mask.append(mask)
        self.GetView().ForceRefresh()

    def clear_sel_masks(self):
        self.sel_mask = []

    def clear_state(self):
        self.append_count = 0
        self.rec_to_update = dict()
        self.rec_to_instert = dict()
        self.rec_to_delete = []
        self.rec_selected = []
        self.tabsort = []
        self.filter_id = None
        self.key = None
        self.sel_mask = []

    def get_table_and_state(self):
        tableandstate = []
        tableandstate.append((
            self.append_count,
            self.rec_to_update,
            self.rec_to_instert,
            self.rec_to_delete,
            self.rec_selected,
            self.tabsort,
            self.filter_id,
            self.key,
            self.sel_mask,
            self.last_row_count,
            ))
        return tableandstate

    def duplicate_table_and_state(self):
        tableandstate = self.get_table_and_state()
        self.append_count = 0
        self.rec_to_update = dict()
        self.rec_to_instert = dict()
        self.rec_to_delete = []
        self.rec_selected = []
        self.tabsort = []
        self.filter_id = None
        self.key = None
        self.sel_mask = []
        return tableandstate

    def set_table_and_state(self, tableandstate):
        oldtableandstate = self.get_table_and_state()
        rec = tableandstate[0]
        self.append_count = rec[0]
        self.rec_to_update = rec[1]
        self.rec_to_instert = rec[2]
        self.rec_to_delete = rec[3]
        self.rec_selected = rec[4]
        self.tabsort = rec[5]
        self.filter_id = rec[6]
        self.key = rec[7]
        self.sel_mask = rec[8]
        self.last_row_count = rec[9]
        return oldtableandstate

    def get_actions(self, row, col=None):
        ret = {}
        attrs = self.get_action_list(row, col)
        for attr in attrs:
            if 'name' in attr:
                name = attr['name']
                if 'href' in attr:
                    href = attr['href']
                    if 'title' in attr:
                        title = attr['title']
                    else:
                        title = ''
                    ret[name] = ('openurl', href, title, attr)
        if len(ret) > 0:
            return ret
        return None

    def enable(self, en):
        pass

    def GetNumberRows(self):
        count = self._get_number_rows()
        return count

    def GetNumberCols(self):
        if len(self.data) > 0:
            return len(self.data[0]) - 1
        else:
            return 0

    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True

    def GetValue(self, row, col):
        try:
            return self.get_rec(row)[col]
        except IndexError:
            return ''

    def GetColLabelValue(self, col):
        return 'COL_' + str(col)

    def GetTypeName(self, row, col):
        return self.GetValue(row, col).__class__.__name__

    def CanGetValueAs(self, row, col, type_name):
        if self.GetTypeName(row, col) == type_name:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, type_name):
        return self.CanGetValueAs(row, col, type_name)

    def GetAttr(self,row,col,kind):
        if row < (self.GetNumberRows() - self.can_append) - self.append_count:
            if row in self.rec_to_update:
                attr = self.attr_update
                attr.IncRef()
                return attr
            elif row in self.rec_to_delete:
                attr = self.attr_del
                attr.IncRef()
                return attr
            elif self._is_sel(row):
                attr = self.attr_sel
                attr.IncRef()
            else:
                attr = self.attr_normal
                attr.IncRef()
            return attr
        else:
            attr = self.attr_insert
            attr.IncRef()
            return attr

    def refresh(self, storePos):
        pass

    def copy(self):
        return None

    def paste(self, data):
        return None
