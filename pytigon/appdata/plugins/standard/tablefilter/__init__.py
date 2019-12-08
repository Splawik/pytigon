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

def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    import pytigon_gui.guictrl.grid.grid
    old_on_key_down = pytigon_gui.guictrl.grid.grid.SchTableGrid.on_key_down

    def on_key_down(self, event):
        if (event.KeyCode == ord('F') or event.KeyCode == ord('f')) and event.ControlDown():
            win = self.GetParent()
            while not hasattr(win, 'new_child_page'):
                win = win.GetParent()
            win.new_child_page('^standard/tablefilter/tablefilter.html', title='Filter')
        elif event.KeyCode == wx.WXK_NUMPAD_ADD or event.KeyCode == 61:
            win = self.GetParent()
            while not hasattr(win, 'new_child_page'):
                win = win.GetParent()
            win.new_child_page('^standard/tablefilter/addfilter.html', title='Add'
                             )
        elif event.KeyCode == wx.WXK_NUMPAD_SUBTRACT or event.KeyCode == ord('-'):
            win = self.GetParent()
            while not hasattr(win, 'new_child_page'):
                win = win.GetParent()
            p = win.new_child_page('^standard/tablefilter/addfilter.html', title='Add')
            p.body.StyleSubtract()
        else:
            if old_on_key_down:
                old_on_key_down(self, event)

    pytigon_gui.guictrl.grid.grid.SchTableGrid.on_key_down = on_key_down
