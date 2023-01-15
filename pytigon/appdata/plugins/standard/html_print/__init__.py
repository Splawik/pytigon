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

# Pytigon - wxpython and django application framework

# author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
# copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
# license: "LGPL 3.0"
# version: "0.1a"


import wx


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    from pytigon_gui.guictrl.ctrl import SchBaseCtrl
    import pytigon_gui.guictrl.ctrl
    from .printframework import HtmlPreviewCanvas, get_printout

    class Htmlprint(HtmlPreviewCanvas, SchBaseCtrl):
        def __init__(self, parent, *args, **kwds):
            SchBaseCtrl.__init__(self, parent, kwds)
            HtmlPreviewCanvas.__init__(self, parent, **kwds)

    pytigon_gui.guictrl.ctrl.HTMLPRINT = Htmlprint
    wx.GetApp().get_printout = get_printout
