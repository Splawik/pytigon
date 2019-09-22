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


from . import schtest
import wx

def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    print("tcc plugin - start testing")
    print(schtest.silnia(10))
    print(schtest.passed("test2"))
    schtest.message("end!")
    print("tcc plugin - end testing")

    functions = { 'silnia': schtest.silnia, 'passed': schtest.passed, 'message': schtest.message, }
    app.extern_data['schtest'] = functions

    print("tcc plugin - start testing2")
    context = wx.GetApp().extern_data['schtest']
    print(context['silnia'](10))
    print(context['passed']("test2"))
    context['message']("end!")
    print("tcc plugin - end testing2")
