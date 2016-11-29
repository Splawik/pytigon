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

from schcli.guilib.event import *
from schcli.toolbar.basetoolbar import ToolbarInterface
from schcli.guictrl.basectrl import SchBaseCtrl

class MenuInterface(ToolbarInterface):

    class Page(object):
        
        class Panel(object):

            def __init__(self, page, title):
                self.page = page
                if False and title == page.title:
                    self.panel = self.page.page
                else:
                    self.panel = wx.Menu()
                    try:
                        self.page.page.AppendMenu(wx.ID_ANY, title, self.panel)
                    except:
                        self.page.page.Append(self.panel, title)

            def add_separator(self):
                pass

            def append(
                self,
                id,
                title,
                bitmap=None,
                ):
                if bitmap:
                    item = wx.MenuItem(self.panel, id=id, text=title)
                    if type(bitmap) == tuple:
                        item.SetBitmap(bitmap[0])
                    self.panel.AppendItem(item)
                else:
                    self.panel.Append(id, title)

            def add_tool(self, id, title, bitmap=None):
                return self.append(id, title, bitmap)

            def add_button(self, id, title, bitmap=None):
                return self.append(id, title, bitmap)

        def __init__(self, bar, title):
            self.bar = bar
            self.title = title
            #sprawdzić
            if title != 'file':
                self.page = self.bar.bar
            else:
                self.page = wx.Menu()
                self.bar.bar.Append(self.page, title)


        def create_panel(self, title, type=None):
            return self.Panel(self, title)


    def __init__(self, bar, gui_style):
        self.bar = bar
        self.gui_style = gui_style
        self.parent=wx.GetApp().GetTopWindow()
        self.toolbars = {}
        self.pages = {}
        self.main_page = None
        ToolbarInterface.__init__(self, self.parent, gui_style)
        self.event_object = self.parent

        self.parent.Bind(wx.EVT_UPDATE_UI, self.on_update_ui)
        self.parent.Bind(wx.EVT_MENU, self.on_command)
        self.block_events = False

    def on_update_ui(self, event):        
        if self.block_events:
            return 
        id = event.GetId()
        if id and ((id >= ID_START and id < ID_END) or (id >= wx.ID_LOWEST and id < wx.ID_HIGHEST )):
            self.block_events = True
            event.Enable(False)
            win = wx.Window.FindFocus()
            if win and win != self.event_object and issubclass(type(win), SchBaseCtrl):
                win.ProcessEvent(event)
            self.block_events = False

    def on_command(self, event):
        win = wx.Window.FindFocus()
        if win and win != self.event_object and issubclass(type(win), SchBaseCtrl):
            win.ProcessEvent(event)
        else:
            event.Skip()

    def get_toolbars(self):
        return self.toolbars

    def create_page(self, title):
        if title in self.pages:
            page = self.pages[title]
        else:
            page = self.Page(self, title)
            self.pages[title] = page
        if not self.main_page:
            self.main_page=page
        return page

    def bind(
        self,
        fun,
        id=wx.ID_ANY,
        e = None
        ):
        if e:
            self.parent.Bind(e, fun, id=id)
        else:
            self.parent.Bind(wx.EVT_MENU, fun, id=id)

    def un_bind(
        self,
        id,
        e=None
        ):
        if e:
            self.parent.Unbind(e, id=id)
        else:
            self.parent.Unbind(wx.EVT_MENU, id=id)

    def update_bar(self, obj):
        obj.SetMenuBar(self.bar)


