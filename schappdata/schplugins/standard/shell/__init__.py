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


def init_plugin(
    app,
    mainframe,
    desktop,
    mgr,
    menubar,
    toolbar,
    accel,
    ):
    import wx.py as py
    from schcli.guictrl.schctrl import SchBaseCtrl
    import schcli.guictrl.schctrl


    class Shell(py.shell.Shell, SchBaseCtrl):

        def __init__(self, *args, **kwds):
            SchBaseCtrl.__init__(self, args, kwds)
            if 'name' in kwds:
                del kwds['name']
            kwds['locals'] = {'self': self}
            py.shell.Shell.__init__(self, *args, **kwds)


    class CrustShell(py.crust.Crust, SchBaseCtrl):

        def __init__(self, *args, **kwds):
            SChBaseCtrl.__init__(self, args, kwds)
            if 'name' in kwds:
                del kwds['name']
            kwds['locals'] = {'self': self}
            py.crust.Crust.__init__(self, *args, **kwds)


    schcli.guictrl.schctrl.SHELL = Shell
    schcli.guictrl.schctrl.CRUST_SHELL = CrustShell

