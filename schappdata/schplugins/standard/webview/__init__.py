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
import six
from .basebrowser import BaseWebBrowser

if wx.Platform == '__WXMSW__':
    #try:
    #if six.PY2:
    if False:
        from .cef import init_plugin_cef    
        def init_plugin(
            app,
            mainframe,
            desktop,
            mgr,
            menubar,
            toolbar,
            accel,
            ):
            return init_plugin_cef(
                app,
                mainframe,
                desktop,
                mgr,
                menubar,
                toolbar,
                accel,
                BaseWebBrowser,
                )
    #except:
    else:
        import wx.html2
        from .wxwebview import init_plugin_web_view


        def init_plugin(
            app,
            mainframe,
            desktop,
            mgr,
            menubar,
            toolbar,
            accel,
            ):
            return init_plugin_web_view(
                app,
                mainframe,
                desktop,
                mgr,
                menubar,
                toolbar,
                accel,
                BaseWebBrowser,
                )
else:
    if False:
        import wx.html2
        from .wxwebview import init_plugin_web_view

        def init_plugin(
            app,
            mainframe,
            desktop,
            mgr,
            menubar,
            toolbar,
            accel,
            ):
            return init_plugin_web_view(
                app,
                mainframe,
                desktop,
                mgr,
                menubar,
                toolbar,
                accel,
                BaseWebBrowser,
                )



    if True:
        from .cef import init_plugin_cef
        def init_plugin(
            app,
            mainframe,
            desktop,
            mgr,
            menubar,
            toolbar,
            accel,
            ):
            return init_plugin_cef(
                app,
                mainframe,
                desktop,
                mgr,
                menubar,
                toolbar,
                accel,
                BaseWebBrowser,
                )
