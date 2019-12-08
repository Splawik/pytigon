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


def replace_colors(win, html):
    c_caption = \
        wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION).GetAsString(wx.C2S_HTML_SYNTAX)
    c_text = \
        wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTIONTEXT).GetAsString(wx.C2S_HTML_SYNTAX)
    return html.replace('#E9E0E2', c_caption).replace('#090002', c_text)


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    from pytigon_gui.guiframe.form import install_pre_process_lib
    install_pre_process_lib(replace_colors)


