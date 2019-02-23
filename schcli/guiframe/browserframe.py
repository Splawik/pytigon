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

from schlib.schhttptools.httpclient import COOKIES

import schcli.guictrl.ctrl

from schcli.guiframe.baseframe import SchBaseFrame

class SchBrowserFrame(SchBaseFrame):
    """
        This is main window of pytigon application
    """

    def __init__(self, parent, gui_style="tree(toolbar,statusbar)", id= -1, title="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE |
                 wx.CLIP_CHILDREN | wx.WANTS_CHARS, name="MainWindow"):


        self.gui_style = gui_style
        self.destroy_fun_tab = []
        self.idle_objects = []
        self.after_init = False
        self.desktop = None
        self._mgr = None
        self.toolbar_interface = None
        self.aTable = None
        self.ctrl = None

        SchBaseFrame.__init__(self, parent, id, gui_style, title, pos, size, style | wx.WANTS_CHARS, name)
        wx.GetApp().SetTopWindow(self)

        self.init_plugins()
        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_SHOW, self.on_show)
        self.Show()
        wx.CallAfter(self.SetSize, (1024,768))

    def on_show(self, event):
        if event.Show and not self.ctrl:
            app = wx.GetApp()
            self.ctrl = schcli.guictrl.ctrl.HTML2(self, name='schbrowser', size=self.GetClientSize())
            #self.ctrl.load_url(app.base_address+"/", cookies = COOKIES)
            self.ctrl.load_url(app.base_path+"/", cookies = COOKIES)

    def on_size(self, event):
        if event:
            if self.ctrl:
                self.ctrl.SetSize(event.GetSize())
            event.Skip()
        else:
            if self.ctrl:
                self.ctrl.SetSize(self.GetSize())

    def get_menu_bar(self):
        return None

    def on_idle(self, event):
        for obj in self.idle_objects:
            obj.on_idle()

        if not self.after_init:
            self.after_init = True
            app = wx.GetApp()
            if len(app.start_pages) > 0:
                def start_pages():
                    for page in app.start_pages:
                        url_page = page.split(';')
                        if len(url_page) == 2:
                            self._on_html(_(url_page[0]) + ',' + app.base_address
                                            + url_page[1])
                wx.CallAfter(start_pages)

        event.Skip()

    def set_acc_key_tab(self, win, tab):
        pass

