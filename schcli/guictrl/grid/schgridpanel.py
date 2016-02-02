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
import wx.lib.scrolledpanel as scrolled
from schcli.guilib.tools import bitmap_from_href
_ = wx.GetTranslation

class SchGridPanel(wx.Panel):

    def __init__(self, *args, **argv):
        self.grid = None
        self.icon_size = 2
        wx.Panel.__init__(self, *args, **argv)
        self.vertical = False
        self._bitmaps = {'edit': 'wx.ART_FILE_OPEN', 'edit_inline': 'wx.ART_FILE_OPEN', 'delete': 'wx.ART_DELETE', 'view_row': 'wx.ART_INFORMATION'}

    def set_bitmap(self, action, path):
        self._bitmaps[action] = path

    def set_bitmaps(self, action_dict):
        for key in action_dict:
            self.set_bitmap(key, action_dict[key])

    def set_vertical(self, enable=True):
        self.vertical = enable

    def _get_bmp(self, id_str):
        if id_str in self._bitmaps:
            value = self._bitmaps[id_str]
            return bitmap_from_href(value, self.icon_size)
        try:
            ret = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (32, 32))
        except:
            ret = wx.ArtProvider_GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (32, 32))
        return ret

    def _add_action(self, akcja):
        test = False
        if 'name' in akcja:
            name = akcja['name']
            label = akcja['data']
            if 'title' in akcja:
                title = akcja['title']
                if not label:
                    label = title
            else:
                title = ''
            if not name in ('insert', 'edit', 'delete', 'new', 'get_row', 'view_row') and not name in self.commands:

                if name in self._bitmaps:
                    b = self._get_bmp(name)
                else:
                    if 'src' in akcja:
                        b = bitmap_from_href(akcja['src'])
                    else:
                        b = bitmap_from_href("fa://fa-chevron-right?size=1")

                self.toolbar.AddLabelTool(
                    self.lp,
                    label,
                    b,
                    wx.NullBitmap,
                    wx.ITEM_NORMAL,
                    label,
                    title,
                    )
                self.commands.append(name)
                test = True
                self.lp+=1
        return test

    def create_toolbar(self, grid):
        self.GetParent().signal_from_child(self, 'set_bitmap_list')
        self.grid = grid
        if self.vertical:
            self.spanel = wx.ScrolledWindow(self, style=wx.VSCROLL)
        else:
            self.spanel = wx.ScrolledWindow(self, style=wx.HSCROLL)
        self.commands = []
        self.lp = 101
        (standard, akcje) = grid.get_action_list()
        if standard or akcje and len(akcje) > 0:
            if self.vertical:
                self.toolbar = wx.ToolBar(self.spanel, -1, wx.DefaultPosition,
                        wx.DefaultSize, wx.TB_VERTICAL)
            else:
                self.toolbar = wx.ToolBar(self.spanel, -1, wx.DefaultPosition,
                        wx.DefaultSize, 0)
            tsize = (22, 22)
            self.toolbar.SetToolBitmapSize(tsize)
            if standard:
                self.toolbar.AddLabelTool(
                    self.lp,
                    _('Edit'),
                    self._get_bmp('edit'),
                    wx.NullBitmap,
                    wx.ITEM_NORMAL,
                    _('Edit'),
                    _('Edit'),
                    )
                self.toolbar.AddLabelTool(
                    self.lp + 1,
                    _('Delete'),
                    self._get_bmp('delete'),
                    wx.NullBitmap,
                    wx.ITEM_NORMAL,
                    _('Delete'),
                    _('Delete'),
                    )
                self.toolbar.AddLabelTool(
                    self.lp + 2,
                    _('view_row'),
                    self._get_bmp('view_row'),
                    wx.NullBitmap,
                    wx.ITEM_NORMAL,
                    _('View row'),
                    _('View row'),
                    )
                self.toolbar.AddSeparator()
                self.commands.append('edit')
                self.commands.append('delete')
                self.commands.append('view_row')
                self.lp += 3
            if akcje:
                for akcja in akcje:
                    self._add_action(akcja)
            self.toolbar.Realize()
            self.toolbar.Bind(wx.EVT_TOOL, self.on_tool_click)

            self.toolbar.SetSize(self.toolbar.GetBestSize())
            if self.vertical:
                self.spanel.SetScrollRate(0, 20)
            else:
                self.spanel.SetScrollRate(20, 0)
            self.spanel.SetVirtualSize(self.toolbar.GetSize())
        grid.set_panel(self)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.on_size()

    def on_size(self, event=None):
        if event:
            panel_size = event.GetSize()
        else:
            panel_size = self.GetSize()
        toolbar_size = self.toolbar.GetSize()
        if self.vertical:
            if toolbar_size[1] >= panel_size[1]:
                dx = toolbar_size[0] + wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
            else:
                dx = toolbar_size[0]
            self.spanel.SetRect(wx.Rect(0, 0, dx, panel_size[1]))
            self.grid.SetRect(wx.Rect(dx + 2, 0, (panel_size[1] - dx) - 2,panel_size[1]))
        else:
            if toolbar_size[0] >= panel_size[0]:
                dy = toolbar_size[1] + wx.SystemSettings.GetMetric(wx.SYS_HSCROLL_Y)
            else:
                dy = toolbar_size[1]
            self.spanel.SetRect(wx.Rect(0, 0, panel_size[0], dy))
            self.grid.SetRect(wx.Rect(0, dy + 2, panel_size[0], (panel_size[1] - dy) - 2))
        if event:
            event.Skip()

    def on_tool_click(self, event):
        id = event.GetId()
        self.grid.action(self.commands[id - 101])


    def refresh(self, row):
        if self.grid.GetTable().GetNumberRows() > 0:
            akcje = self.grid.get_action_list(row)[1]
            akcje_dict = {}
            test = False
            if akcje:
                for akcja in akcje:
                    if not 'name' in akcja:
                        continue
                    akcje_dict[akcja['name']] = akcje
                    if self._add_action(akcja):
                        test = True
            if test:
                self.toolbar.Realize()
                self.toolbar.SetSize(self.toolbar.GetBestSize())
            i = 101
            for command in self.commands:
                if command in akcje_dict:
                    self.toolbar.EnableTool(i, True)
                else:
                    self.toolbar.EnableTool(i, False)
                i = i + 1


