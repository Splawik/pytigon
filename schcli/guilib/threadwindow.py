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
import wx.html
from schlib.schtools import schjson


schEVT_THREAD_INFO = wx.NewEventType()
EVT_THREAD_INFO = wx.PyEventBinder(schEVT_THREAD_INFO, 1)


class ThreadEvent(wx.PyCommandEvent):

    def __init__(self, evt_type, id):
        wx.PyCommandEvent.__init__(self, evt_type, id)
        self.info = None

    def set_info(self, val):
        self.info = val

    def get_info(self):
        return self.info


class SchThreadWindow(wx.Panel):

    def __init__(self,manager,thread_name,*args,**kwds):

        wx.Panel.__init__(self, *args, **kwds)
        self.thread_name = thread_name
        self.manager = manager
        self.closed = False
        self.SetBackgroundColour(wx.NamedColour('#eec'))
        self.gauge = wx.Gauge(self, range=100, size=(100, 1))
        self.gauge.SetValue(0)
        self.html = wx.html.HtmlWindow(self, size=(50, 50),
                                       style=wx.html.HW_SCROLLBAR_NEVER)
        self.html.SetBorders(0)
        self.html.SetPage("<body bgcolor='#eec'></body>")
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_TO_PARENT, wx.ART_TOOLBAR,
                                       (16, 16))
        bmp = bmp.ConvertToImage().Rescale(16, 8).ConvertToBitmap()
        bmp2 = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_TOOLBAR, (16, 16))
        bmp2 = bmp2.ConvertToImage().Rescale(16, 8).ConvertToBitmap()
        button1 = wx.BitmapButton(self, -1, bmp)
        button2 = wx.BitmapButton(self, -1, bmp2)
        self.Bind(wx.EVT_BUTTON, self.on_expand, button1)
        self.Bind(wx.EVT_BUTTON, self.on_kill, button2)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.html, 1, wx.EXPAND)
        box.Add(self.gauge, 0, wx.EXPAND)
        box.Add(button1, 0, wx.EXPAND)
        box.Add(button2, 0, wx.EXPAND)
        self.SetSizer(box)
        box.Fit(self)

    def is_closed(self):
        return self.closed

    def timer(self):
        http = wx.GetApp().http
        http.get(self, 'http://local.net/schsys/thread_short_info/'
                  + self.thread_name)
        info_json = http.str()
        info = schjson.loads(info_json)
        http.clear_ptr()

        if type(info)==str and info == '$$$':
            self.closed = True
            evt = ThreadEvent(schEVT_THREAD_INFO, -1)
            evt.set_info(self.thread_name)
            wx.GetApp().GetTopWindow().GetEventHandler().ProcessEvent(evt)
        else:
            if info:
                if 'progress' in info:
                    progress = info['progress']
                    self.gauge.SetValue(int(progress))
                if 'description' in info:
                    description = info['description']
                    self.html.SetPage("<body bgcolor='#eec'>" + description + '</body>')

    def on_expand(self, event):
        address = 'http://local.net/schsys/thread_long_info/' + self.thread_name
        wx.GetApp().GetTopWindow().new_main_page(address, 'aplikacja')

    def on_kill(self, event):
        http = wx.GetApp().http
        http.get(self, 'http://local.net/schsys/thread_kill/'
                  + self.thread_name)
        http.clear_ptr()


class SchThreadManager(object):

    def __init__(self, app, statusbar):
        self.app = app
        self.statusbar = statusbar
        self.sizeChanged = True
        self.windows = []
        statusbar.Bind(wx.EVT_SIZE, self.on_size)
        statusbar.Bind(wx.EVT_IDLE, self.on_idle)

    def append(self, thread_address):
        self.windows.append(SchThreadWindow(self, thread_address,
                            self.statusbar))

    def reposition(self):
        x = len(self.windows)
        if x > 0:
            rect = self.statusbar.GetFieldRect(1)
            w = 0
            for win in self.windows:
                win.SetPosition((rect.x + w + 2, rect.y + 2))
                win.SetSize((rect.width / x - 4, rect.height - 3))
                w += rect.width / x

    def on_size(self, evt):
        self.reposition()
        self.sizeChanged = True

    def on_idle(self, evt):
        if self.sizeChanged:
            self.reposition()

    def timer(self):
        if len(self.windows) > 0:
            for win in self.windows:
                if win.is_closed():
                    win.Destroy()
                    self.windows.remove(win)
                else:
                    win.timer()


