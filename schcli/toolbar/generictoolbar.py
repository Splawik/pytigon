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

import wx.lib.agw
import wx.lib.agw.aui as aui
import wx.lib.agw.aui.aui_utilities

from schcli.guilib.events import *
from schcli.toolbar.basetoolbar import ToolbarBar, ToolbarPage, ToolbarPanel, ToolbarButton


_ = wx.GetTranslation


class SchAuiToolBarArt(aui.AuiDefaultToolBarArt):
    def __init__(self):
        aui.AuiDefaultToolBarArt.__init__(self)
        self._base_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND)

    def draw_background(self,dc, wnd, _rect, horizontal=True):
        rect = wx.Rect(*_rect)
        start_colour = self._base_colour
        end_colour = self._base_colour
        reflex_colour = aui.StepColour(self._base_colour, 95)
        dc.GradientFillLinear(rect, start_colour, end_colour, (horizontal and [wx.SOUTH] or [wx.EAST])[0])
        left = rect.GetLeft()
        right = rect.GetRight()
        top = rect.GetTop()
        bottom = rect.GetBottom()
        dc.SetPen(wx.Pen(reflex_colour))
        if horizontal:
            dc.DrawLine(left, bottom, right + 1, bottom)
        else:
            dc.DrawLine(right, top, right, bottom + 1)


class GenericToolbarButton(ToolbarButton):
    def __init__(self, parent_panel, id, title, bitmap, bitmap_disabled = None, kind=ToolbarButton.TYPE_SIMPLE):
        ToolbarButton.__init__(self, parent_panel, id, title, bitmap, bitmap_disabled, kind)


class GenericToolbarPanel(ToolbarPanel):
    def __init__(self, parent_page, title, kind=ToolbarPanel.TYPE_PANEL_TOOLBAR):

        ToolbarPanel.__init__(self, parent_page, title, kind)

        if len(parent_page.panels)>0:
            parent_page.AddStretchSpacer()

    def _append(self, b):
        item = None
        if self.kind in (ToolbarPanel.TYPE_PANEL_TOOLBAR, ToolbarPanel.TYPE_PANEL_BUTTONBAR):
            if b.kind == ToolbarButton.TYPE_SIMPLE:
                item = self.parent_page.AddSimpleTool(b.id, b.title, b.bitmap, b.title)
            elif b.kind == ToolbarButton.TYPE_DROPDOWN:
                item = self.parent_page.AddSimpleTool(b.id, b.title, b.bitmap, b.title)
            elif b.kind == ToolbarButton.TYPE_HYBRID:
                item = self.parent_page.AddSimpleTool(b.id, b.title, b.bitmap, b.title)
            elif b.kind == ToolbarButton.TYPE_TOOGLE:
                item = self.parent_page.AddToggleTool(b.id, b.title, b.bitmap)
            elif b.kind == ToolbarButton.TYPE_PANEL:
                pass
            elif b.kind == ToolbarButton.TYPE_SEPARATOR:
                self.parent_page.AddSeparator()
        else:
            pass


    def create_button(self, id, title, bitmap=None, bitmap_disabled=None, kind=ToolbarButton.TYPE_SIMPLE):
        b = GenericToolbarButton(self, id, title, bitmap, bitmap_disabled, kind)
        self._append(b)
        return b

    def add_separator(self):
        b = GenericToolbarButton(self, 0, '', None, None, kind=ToolbarButton.TYPE_SEPARATOR)
        self._append(b)
        return b


class GenericToolbarPage(ToolbarPage, aui.AuiToolBar):
    def __init__(self, parent_bar, title, kind=ToolbarPage.TYPE_PAGE_NORMAL):
        ToolbarPage.__init__(self, parent_bar, title, kind)
        agwStyle = aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_HORZ_LAYOUT
        aui.AuiToolBar.__init__(self, parent_bar.parent, -1, wx.DefaultPosition, wx.DefaultSize, agwStyle=agwStyle)

        self.SetToolBitmapSize(wx.Size(24, 24))
        if wx.Platform != '__WXMSW__':
            self.SetArtProvider(SchAuiToolBarArt())
        nr = len(parent_bar.pages) + 1

        pinfo = parent_bar.parent._create_pane_info('tb' + str(nr), 'Toolbar ' + str(nr)).ToolbarPane().\
            Top().LeftDockable(False).RightDockable(False).Row(1)
        parent_bar.parent._mgr.AddPane(self, pinfo)

    def create_panel(self, title, kind=ToolbarPanel.TYPE_PANEL_TOOLBAR):
        return GenericToolbarPanel(self, title, kind)


class GenericToolbarBar(ToolbarBar):
    def __init__(self, parent, gui_style):
        ToolbarBar.__init__(self, parent, gui_style)

    def create_page(self, title, kind=ToolbarPage.TYPE_PAGE_NORMAL):
        return GenericToolbarPage(self, title, kind)

    def create(self):
        for bar in self.pages:
            bar.Realize()
            bar.SetSize(bar.GetBestSize())

    def update(self):
        pass

    def bind_ui(self, fun, id=wx.ID_ANY):
        self.parent.Bind(wx.EVT_UPDATE_UI, fun, id=id)

    def bind(self, fun, id=wx.ID_ANY, e=None):
        if e:
            self.parent.Bind(e, fun, id=id)
        else:
            self.parent.Bind(wx.EVT_MENU, fun, id=id)

    def bind_dropdown(self, fun, id):
        self.parent.Bind(wx.EVT_MENU, fun, id=id)

    def un_bind(self, id, e=None):
        if e:
            self.Unbind(e, id=id)
        else:
            self.Unbind(wx.EVT_MENU, id=id)

