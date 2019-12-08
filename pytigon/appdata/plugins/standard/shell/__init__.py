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


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    import wx.py as py
    import wx
    from pytigon_gui.guictrl.ctrl import SchBaseCtrl
    import pytigon_gui.guictrl.ctrl

    class Shell(py.shell.Shell, SchBaseCtrl):
        def __init__(self, parent, **kwds):
            SchBaseCtrl.__init__(self, parent, kwds)
            if 'name' in kwds:
                del kwds['name']
            kwds['locals'] = {'self': self, 'app': wx.GetApp(),'topwin': wx.GetApp().GetTopWindow(), 'wx': wx }
            py.shell.Shell.__init__(self, parent, **kwds)


    class CrustShell(py.crust.Crust, SchBaseCtrl):
        def __init__(self, parent, **kwds):
            SchBaseCtrl.__init__(self, parent, kwds)
            if 'name' in kwds:
                del kwds['name']
            kwds['locals'] = {'self': self, 'app': wx.GetApp(),'topwin': wx.GetApp().GetTopWindow(), 'wx': wx }
            py.crust.Crust.__init__(self, parent, **kwds)


    class SliceShell(py.sliceshell.SlicesShell, SchBaseCtrl):
        def __init__(self, parent, **kwds):
            SchBaseCtrl.__init__(self, parent, kwds)
            if 'name' in kwds:
                del kwds['name']
            kwds['locals'] = {'self': self, 'app': wx.GetApp(),'topwin': wx.GetApp().GetTopWindow(), 'wx': wx }
            kwds['showPySlicesTutorial'] = False
            py.sliceshell.SlicesShell.__init__(self, parent, **kwds)

    pytigon_gui.guictrl.ctrl.SHELL = Shell
    pytigon_gui.guictrl.ctrl.CRUST_SHELL = CrustShell
    pytigon_gui.guictrl.ctrl.SLICE_SHELL = SliceShell


