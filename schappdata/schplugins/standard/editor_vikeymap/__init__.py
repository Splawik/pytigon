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
    import schcli.guictrl.schctrl

    base = schcli.guictrl.schctrl.STYLEDTEXT

    class ViKeyMapEditor(base):
        def __init__(self, *args, **kwds):
            aTable = [
                    (wx.ACCEL_ALT, ord('J'), self.on_down),
                    (wx.ACCEL_ALT, ord('K'), self.on_up),
                    (wx.ACCEL_ALT, ord('H'), self.on_left),
                    (wx.ACCEL_ALT, ord('L'), self.on_right),
                    (wx.ACCEL_ALT, ord('B'), self.on_page_up),
                    (wx.ACCEL_ALT, ord('F'), self.on_page_down),

                    (wx.ACCEL_ALT, ord('I'), self.on_home),
                    (wx.ACCEL_ALT, ord('A'), self.on_end),
                    (wx.ACCEL_ALT, ord('O'), self.on_line_next),

                    (wx.ACCEL_ALT, ord('V'), self.on_start_sel),
                    (wx.ACCEL_ALT, ord('Y'), self.on_copy),
                    (wx.ACCEL_ALT, ord('P'), self.on_paste),

            ]
            base.__init__(self, *args, **kwds)
            self.GetParent().set_acc_key_tab(self, aTable)
            self.start_sel = None

        def on_start_sel(self, event):
            if self.start_sel:
                self.start_sel = None
            else:
                self.start_sel =  self.GetCurrentPos()

        def on_copy(self, event):
            if self.start_sel != None:
                pos = self.GetCurrentPos()
                self.SetSelection(self.start_sel, pos)
                self.Copy()
                self.SetSelection(pos, pos)
            self.start_sel = None


        def on_paste(self, event):
            self.Paste()

        def on_down(self, event):
            if self.start_sel != None:
                self.LineDownExtend()
            else:
                self.LineDown()

        def on_up(self, event):
            if self.start_sel != None:
                self.LineUpExtend()
            else:
                self.LineUp()

        def on_page_down(self, event):
            if self.start_sel != None:
                self.PageDownExtend()
            else:
                self.PageDown()

        def on_page_up(self, event):
            if self.start_sel != None:
                self.PageUpExtend()
            else:
                self.PageUp()

        def on_home(self, event):
            if self.start_sel != None:
                self.VCHomeExtend()
            else:
                self.VCHome()

        def on_end(self, event):
            if self.start_sel != None:
                self.LineEndExtend()
            else:
                self.LineEnd()

        def on_line_next(self, event):
            self.LineEnd()
            self._enter_key()

        def on_left(self, event):
            pos = self.GetCurrentPos()-1
            if pos>=0:
                self.SetCurrentPos(pos)
                if self.start_sel != None:
                    self.SetSelection(self.start_sel, pos)
                else:
                    self.SetSelection(pos, pos)
                self.EnsureCaretVisible()

        def on_right(self, event):
            pos = self.GetCurrentPos()+1
            if pos>=0:
                self.SetCurrentPos(pos)
                if self.start_sel != None:
                    self.SetSelection(self.start_sel, pos)
                else:
                    self.SetSelection(pos, pos)
                self.EnsureCaretVisible()


    schcli.guictrl.schctrl.STYLEDTEXT = ViKeyMapEditor

