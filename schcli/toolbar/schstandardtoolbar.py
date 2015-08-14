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
# import wx.lib.agw.aui as aui import wx.lib.agw.aui.aui_utilities

import wx.lib.agw
import wx.lib.agw.aui as aui
import wx.lib.agw.aui.aui_utilities

from schcli.toolbar.basetoolbar import ToolbarInterface, TYPE_TOOLBAR, \
    TYPE_BUTTONBAR, TYPE_PANELBAR
from schcli.guictrl.schbasectrl import SchBaseCtrl

from schcli.guilib.schevent import *


_ = wx.GetTranslation

class SchAuiToolBarArt(aui.AuiDefaultToolBarArt):

    def __init__(self):
        aui.AuiDefaultToolBarArt.__init__(self)
        self._base_colour = \
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND)  # 3DFACE

    def draw_background(
        self,
        dc,
        wnd,
        _rect,
        horizontal=True,
        ):
        rect = wx.Rect(*_rect)
        start_colour = self._base_colour
        end_colour = self._base_colour
        reflex_colour = aui.StepColour(self._base_colour, 95)
        dc.GradientFillLinear(rect, start_colour, end_colour, (horizontal
                               and [wx.SOUTH] or [wx.EAST])[0])
        left = rect.GetLeft()
        right = rect.GetRight()
        top = rect.GetTop()
        bottom = rect.GetBottom()
        dc.SetPen(wx.Pen(reflex_colour))
        if horizontal:
            dc.DrawLine(left, bottom, right + 1, bottom)
        else:
            dc.DrawLine(right, top, right, bottom + 1)


class EmpytControl(object):

    def __init__(self):
        self.value = None

    def SetValue(self, value):
        self.value = value

    def GetValue(self):
        return self.value


class EmptyBar(object):

    def __init__(self):
        pass

    def refr(self):
        pass


class ToolBarInterface(ToolbarInterface):


    class Page(object):


        class Panel(object):

            def __init__(
                self,
                page,
                title,
                type=TYPE_TOOLBAR,
                ):
                self.page = page

            def append(
                self,
                id,
                title,
                bitmap=None,
                ):
                if bitmap:
                    self.page.page.AddSimpleTool(id, title, bitmap, title)

            def add_tool(
                self,
                id,
                title,
                bitmaps,
                ):
                self.append(id, title, bitmaps[0])

            def add_hybrid_tool(
                self,
                id,
                title,
                bitmaps,
                ):
                self.Append(id, title, bitmaps[0])

            def add_button(
                self,
                id,
                title,
                bitmaps,
                ):
                self.append(id, title, bitmaps[0])

            def add_panel(
                self,
                id,
                title,
                bitmaps,
                ):
                self.append(id, title, bitmaps[0])

            def add_separator(self):
                pass


        def __init__(self, bar, title):
            self.bar = bar
            self.page = aui.AuiToolBar(self.bar.parent._panel, -1,
                                       wx.DefaultPosition, wx.DefaultSize,
                                       agwStyle=aui.AUI_TB_DEFAULT_STYLE|aui.AUI_TB_HORZ_LAYOUT)
            #|aui.AUI_TB_OVERFLOW)
                                    #|aui.AUI_TB_TEXT|aui.AUI_TB_OVERFLOW)
                                       # |aui.AUI_TB_PLAIN_BACKGROUNDaui.AUI_TB_OVERFLOW|)
            self.page.SetToolBitmapSize(wx.Size(24, 24))
            #self.page.SetArtProvider(SchAuiToolBarArt())
            nr = len(self.bar.toolbars) + 1
            self.bar.parent._mgr.AddPane(self.page, self.bar.parent.panel('tb'
                     + str(nr), 'Toolbar '
                     + str(nr)).ToolbarPane().Top().LeftDockable(False).RightDockable(False).Row(1))


        def create_panel(self, title, type=TYPE_TOOLBAR):
            return self.Panel(self, title, type)


    def __init__(self, parent, gui_style):
        self.parent = parent
        self.event_object = parent
        self.pages = {}
        self.main_page = None
        self.tab = []
        self.toolbars = {}
        ToolbarInterface.__init__(self, parent, gui_style)
        self.toolbars = []

    def create_page(self, title):
        page = self.Page(self, title)
        self.tab.append(page)
        if not self.main_page:
            self.main_page = page
        return page

    def bind(
        self,
        fun,
        id=wx.ID_ANY,
        e = None,
        ):
        if e:
            self.parent.Bind(e, fun, id=id)
        else:
            self.parent.Bind(wx.EVT_MENU, fun, id=id)

    def realize_bar(self):
        for bar in self.tab:
            bar.page.Realize()
            bar.page.SetSize(bar.page.GetBestSize())
            #bar.page.Refresh(False)
            #print(bar.page)

            bar.page.Bind(wx.EVT_UPDATE_UI, self.on_update_ui)
            bar.page.Bind(wx.EVT_MENU, self.on_command)


    def on_command(self, event):
        if not self.parent.ProcessEvent(event):
            win = wx.Window.FindFocus()
            if win and issubclass(type(win), SchBaseCtrl):
                win.ProcessEvent(event)

    def on_update_ui(self, event):
        id = event.GetId()
        if id and ((id >= ID_START and id < ID_END) or (id >= wx.ID_LOWEST and id < wx.ID_HIGHEST )):
            if not self.parent.ProcessWindowEvent(event):
                win = wx.Window.FindFocus()
                if win and issubclass(type(win), SchBaseCtrl):
                    if not win.ProcessEvent(event):
                        event.Enable(False)
                else:
                    event.Enable(False)

    def get_toolbars(self):
        return self.toolbars

    def connect_object_to_panel(self, panel, object):
        pass

    def add_panel(self, panel, controls):
        for c in controls:
            c.SetMinSize((350, c.GetSize()[1]))
            self.bar_tmp.AddControl(c)
        self.frame._mgr.AddPane(self.bar_tmp, self.frame.Panel('tb99',
                                'Toolbar 99'
                                ).ToolbarPane().Top().LeftDockable(False).RightDockable(False).Row(2))
        self.bar_tmp.Realize()


    def bind_dropdown(self, fun, id):
        self.parent.Bind(aui.EVT_AUITOOLBAR_TOOL_DROPDOWN, fun, id=id)

    def un_bind(self, id, e=None):
        if e:
            self.parent.Unbind(e, id=id)
        else:
            self.parent.Unbind(wx.EVT_MENU, id=id)

    def status_tool_disabled(self):
        return 1

    def status_tool_enabled(self):
        return 0

    def add_spacer(self, bar):
        bar.AddSpacer(1)

    def popup_menu(self, event, menu):
        if event.IsDropDownClicked():
            tb = event.GetEventObject()
            tb.SetToolSticky(event.GetId(), True)
            rect = tb.GetToolRect(event.GetId())
            pt = tb.ClientToScreen(rect.GetBottomLeft())
            menu.Popup(wx.Point(pt.x, pt.y), self.bar)
            tb.SetToolSticky(event.GetId(), False)
        else:
            event.Skip()


