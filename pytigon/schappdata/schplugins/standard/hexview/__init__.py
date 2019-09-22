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
import binascii


def init_plugin(app, mainframe, desktop, mgr, menubar, toolbar, accel):
    import pytigon_gui
    import pytigon_gui.guictrl.ctrl

    class Hexviewer(pytigon_gui.guictrl.ctrl.STYLEDTEXT):

        def __init__(self, *args, **kwds):
            pytigon_gui.guictrl.ctrl.STYLEDTEXT.__init__(self, *args, **kwds)
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
            num_buf = len(hex) // 32
            for i in range(num_buf):
                h = hex[0 + i * 32:32 + i * 32]
                hh = " ".join([a+b for a,b in zip(h[::2],h[1::2])])
                b = binascii.unhexlify(h)
                p = b.decode('utf-8', 'replace').replace('\n','.').replace('\r','.').replace('\t','.').\
                    replace("'", '.').replace("\"","")
                pp = ''.join([x if x in string.printable else '.' for x in p])
                self.AddText(hh + ' | ' + pp + '\n')

        def load_from_url(self, url, ext):
            self.set_ext('txt')
            http = wx.GetApp().http
            response = http.get(self, url + '0/')
            txt = response.str()
            self.print_hex(txt)
            self.url = url

        def on_save(self, event):
            pass


    pytigon_gui.guictrl.ctrl.HEXVIEWER = Hexviewer


