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

                (wx.ACCEL_ALT, ord('N'), self.on_home),
                (wx.ACCEL_ALT, ord(';'), self.on_end),

                (wx.ACCEL_ALT|wx.ACCEL_SHIFT, ord('L'), self.on_next_word),
                (wx.ACCEL_ALT|wx.ACCEL_SHIFT, ord('H'), self.on_prev_word),

                (wx.ACCEL_CTRL, ord('K'), self.on_top),
                (wx.ACCEL_CTRL, ord('J'), self.on_bottom),

                (wx.ACCEL_ALT, ord('I'), self.on_start_sel),
                (wx.ACCEL_ALT, ord('C'), self.on_copy),
                (wx.ACCEL_ALT, ord('P'), self.on_paste),
                (wx.ACCEL_ALT, ord('X'), self.on_delete),
                (wx.ACCEL_ALT, ord('Z'), self.on_undo),

                (wx.ACCEL_ALT|wx.ACCEL_SHIFT, ord('J'), self.on_page_down),
                (wx.ACCEL_ALT|wx.ACCEL_SHIFT, ord('K'), self.on_page_up),

                (wx.ACCEL_ALT, wx.WXK_RETURN, self.on_line_next),
            ]
            base.__init__(self, *args, **kwds)
            self.GetParent().set_acc_key_tab(self, aTable)
            self.start_sel = None

        def on_start_sel(self, event):
            if self.start_sel:
                self.start_sel = None
                pos =  self.GetCurrentPos()
                self.SetSelection(pos,pos)
            else:
                self.start_sel =  self.GetCurrentPos()

        def on_copy(self, event):
            if self.start_sel != None:
                pos = self.GetCurrentPos()
                self.Copy()
                self.SetSelection(pos, pos)
                self.start_sel = None
            else:
                self.Copy()

        def on_paste(self, event):
            self.Paste()
            self.start_sel = None

        def _cmd(self, cmd1, cmd2):
            if self.start_sel != None:
                cmd2()
            else:
                cmd1()
            self.EnsureCaretVisible()

        def on_down(self, event):
            self._cmd(self.LineDown, self.LineDownExtend)

        def on_up(self, event):
            self._cmd(self.LineUp, self.LineUpExtend)

        def on_page_down(self, event):
            self._cmd(self.PageDown, self.PageDownExtend)

        def on_page_up(self, event):
            self._cmd(self.PageUp, self.PageUpExtend)

        def on_home(self, event):
            self._cmd(self.VCHome, self.VCHomeExtend)

        def on_end(self, event):
            self._cmd(self.LineEnd, self.LineEndExtend)

        def on_left(self, event):
            self._cmd(self.CharLeft, self.CharLeftExtend)

        def on_right(self, event):
            self._cmd(self.CharRight, self.CharRightExtend)

        def on_next_word(self, event):
            self._cmd(self.WordRight, self.WordRightExtend)

        def on_prev_word(self, event):
            self._cmd(self.WordLeft, self.WordLeftExtend)

        def on_top(self, event):
            self._cmd(self.DocumentStart, self.DocumentStartExtend)

        def on_bottom(self, event):
            self._cmd(self.DocumentEnd, self.DocumentEndExtend)

        def on_delete(self, event):
            start,end = self.GetSelection()
            if start==end:
                pos = self.GetCurrentPos()+1
                self.SetCurrentPos(pos)
                self.SetSelection(pos, pos)
                self.DeleteBack()
                self.EnsureCaretVisible()
            else:
                self.DeleteBack()
            self.start_sel = None

        def on_undo(self, event):
            self.Redo()

        def on_line_next(self, event):
            self.LineEnd()
            self._enter_key()

    schcli.guictrl.schctrl.STYLEDTEXT = ViKeyMapEditor

