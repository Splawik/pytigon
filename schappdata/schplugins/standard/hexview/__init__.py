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
import string


def init_plugin(
    app,
    mainframe,
    desktop,
    mgr,
    menubar,
    toolbar,
    accel,
    ):
    from .editor import CodeEditor
    from schcli.guictrl.schctrl import SchBaseCtrl
    import schcli.guictrl.schctrl


    class Hexviewer(CodeEditor, SchBaseCtrl):

        def __init__(self, *args, **kwds):
            SchBaseCtrl.__init__(self, args, kwds)
            CodeEditor.__init__(self, *args, **kwds)
            if self.src:
                self.SetExt(self.src)
            self.last_clipboard_state = False

        def set_save_path(self, href):
            self.href = href

        def SetValue(self, value):
            self.AddText(value)

        def GetValue(self):
            return self.GetText()

        def print_hex(self, hex):
            num_buf = len(hex) / 64
            for i in range(num_buf):
                h = hex[0 + i * 32:32 + i * 32]
                hh = ''
                s = ''
                for j in range(16):
# print "A1:", h[2*j: 2*j+2], string.atoi(h[2*j: 2*j+2], 16)
                    f = h[2 * j:2 * j + 2]
                    hh += f + ' '
                    c = string.atoi(f, 16)
# if ( ord('a') <= c <= ord('z') ) or ( ord('A') <= c <= ord('Z') ) or (
# ord('0') <= c <= ord('9') ):
                    if chr(c) in string.ascii_letters or chr(c) in string.digits\
                         or chr(c) in '()[]=*/+-{}:;':
                        s += chr(c)
                    else:
                        s += '.'
                self.AddText(s + ' | ' + hh + '\n')

        def load_from_url(self, url, ext):
# self.SetExt(ext)
            self.SetExt('txt')
            http = wx.GetApp().HTTP
            http.get(self, url + '0/')
            txt = http.ptr()
            self.PrintHex(txt)
# self.AddText(txt)
            http.clear_ptr()
            self.url = url

        def on_save(self, event):
# print "OnSave" http = wx.GetApp().HTTP
            http = wx.GetApp().get_http(self)
            if self.href:
                http.post(self, self.href, {'data': self.GetText()})
# txt = http.Ptr() print "Save result:", txt
            http.clear_ptr()

        def can_copy(self):
            if self.GetSelectionEnd() - self.GetSelectionStart() != 0:
                return True
            else:
                return False

        def can_cut(self):
            return self.CanCopy()

# if self.GetSelectionEnd() - self.GetSelectionStart() != 0: return True else:
# return False

        def can_paste(self):
            if self.last_clipboard_state or CodeEditor.CanPaste(self):
                self.last_clipboard_state = True
                return True
            else:
                return False

        def on_copy(self, event):
            self.Copy()

        def on_cut(self, event):
            self.Cut()

        def on_paste(self, event):
            self.Paste()


    schcli.guictrl.schctrl.HEXVIEWER = Hexviewer


