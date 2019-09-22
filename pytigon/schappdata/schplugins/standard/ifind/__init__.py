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
    import pytigon_gui.guictrl.ctrl
    old_on_key_pressed = pytigon_gui.guictrl.ctrl.STYLEDTEXT.on_key_pressed

    def on_key_pressed(self, event):
        key = event.GetKeyCode()
        if key == 70 and event.ControlDown():
            self.GetParent().new_child_page('^standard/ifind/ifindpanel.html', title='Find')
        if key == 71 and event.ControlDown():
            self.GetParent().new_child_page('^standard/ifind/gotopanel.html', title='Go')
        if key == 72 and event.ControlDown():
            self.GetParent().new_child_page('^standard/ifind/ireplacepanel.html', title='Replace')
        else:
            if old_on_key_pressed:
                old_on_key_pressed(self, event)

    pytigon_gui.guictrl.ctrl.STYLEDTEXT.on_key_pressed = on_key_pressed


