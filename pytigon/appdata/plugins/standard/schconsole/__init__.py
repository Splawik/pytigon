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


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    from pytigon_gui.guictrl.ctrl import SchBaseCtrl
    import pytigon_gui.guictrl.ctrl

    class Console(wx.Panel):
        def __init__(self, parent, **kwds):
            if 'name' in kwds:
                name = kwds['name']
                del kwds['name']
            else:
                name = 'CONSOLE'
            self.obj = SchBaseCtrl(self, parent, kwds)
            wx.Panel.__init__(self, parent, name=name)
            html = wx.html.HtmlWindow(self)
            html.SetPage('Hello world Hello world Hello world Hello world Hello world Hello world')
            text = wx.TextCtrl(self)
            box = wx.BoxSizer(wx.VERTICAL)
            box.Add(html, 1, wx.EXPAND)
            box.Add(text, 0, wx.EXPAND)
            self.SetSizer(box)
            box.Fit(self)

    pytigon_gui.guictrl.ctrl.CONSOLE = Console


