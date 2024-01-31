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

# Pytigon - wxpython and django application framework

# author: "Slawomir Cholaj (slawomir.cholaj@gmail.com)"
# copyright: "Copyright (C) ????/2012 Slawomir Cholaj"
# license: "LGPL 3.0"
# version: "0.1a"

import wx
from io import BytesIO
from PIL import Image
from pytigon_gui.guilib.image import pil_to_image
from pytigon_gui.guictrl.basectrl import SchBaseCtrl
from pytigon_lib.schtools.images import svg_to_png


def init_plugin(
    app,
    mainframe,
    desktop,
    mgr,
    menubar,
    toolbar,
    accel,
):
    import pytigon_gui.guictrl.ctrl

    class Imageviewer(wx.ScrolledWindow, SchBaseCtrl):
        def __init__(self, parent, **kwds):
            SchBaseCtrl.__init__(self, parent, kwds)
            wx.ScrolledWindow.__init__(self, parent, **kwds)
            self.static_bitmap = wx.StaticBitmap(self)
            if self.src:
                self.set_ext(self.src)
            self.last_clipboard_state = False
            mainframe.bind_to_toolbar(self.on_copy, id=wx.ID_COPY)
            mainframe.bind_to_toolbar(self.on_cut, id=wx.ID_CUT)
            mainframe.bind_to_toolbar(self.on_paste, id=wx.ID_PASTE)
            a_table = [
                (0, wx.WXK_F2, self.on_save),
                (wx.ACCEL_CTRL, ord("S"), self.on_save),
            ]
            self.set_acc_key_tab(a_table)
            self.resize_to_win = True
            self.Bind(wx.EVT_SIZE, self.on_size)
            self.pil = None

        def on_size(self, event):
            if self.pil:
                size = self.GetParent().GetSize()
                resized = False
                if self.resize_to_win and (
                    self.pil.size[0] > size[0] or self.pil.size[1] > size[1]
                ):
                    delta1 = (self.pil.size[0] * 1.0) / size[0]
                    delta2 = (self.pil.size[1] * 1.0) / size[1]
                    delta = delta1 if delta1 > delta2 else delta2
                    pos = (int(self.pil.size[0] / delta), int(self.pil.size[1] / delta))
                    pil2 = self.pil.resize(pos, Image.BICUBIC)
                    resized = True
                else:
                    pil2 = self.pil
                img = pil_to_image(pil2)
                self.static_bitmap.SetBitmap(img.ConvertToBitmap())
                if not resized:
                    self.SetVirtualSize(wx.Size(img.GetWidth(), img.GetHeight()))
                    self.SetScrollRate(20, 20)
            event.Skip()

        def set_ext(self, ext):
            self.ext = ext

        def goto_pos(self, pos):
            pass

        def set_save_path(self, href):
            self.href = href

        def SetValue(self, value):
            self.AddText(value)

        def load_from_url(self, url, ext):
            self.set_ext(ext)
            http = wx.GetApp().http
            response = http.get(self, url)
            txt = response.ptr()
            size = self.GetParent().GetSize()

            if ext == "svg":
                img2 = svg_to_png(txt, size[0], size[1], "simple_min")
                io = BytesIO(img2)
            else:
                io = BytesIO(txt)

            self.pil = Image.open(io)
            size = self.GetParent().GetSize()
            resized = False
            if self.resize_to_win and (
                self.pil.size[0] > size[0] or self.pil.size[1] > size[1]
            ):
                delta1 = (self.pil.size[0] * 1.0) / size[0]
                delta2 = (self.pil.size[1] * 1.0) / size[1]
                delta = delta1 if delta1 > delta2 else delta2
                pos = (int(self.pil.size[0] / delta), int(self.pil.size[1] / delta))
                pil2 = self.pil.resize(pos, Image.BICUBIC)
                resized = True
            else:
                pil2 = self.pil
            img = pil_to_image(pil2)
            self.static_bitmap.SetBitmap(img.ConvertToBitmap())
            if not resized:
                self.SetVirtualSize(wx.Size(img.GetWidth(), img.GetHeight()))
                self.SetScrollRate(20, 20)
            self.url = url

        def on_save(self, event):
            http = wx.GetApp().get_http(self)
            if self.href:
                http.post(self, self.href, {"data": self.GetText()})

        def on_copy(self, event):
            self.Copy()

        def on_cut(self, event):
            self.Cut()

        def on_paste(self, event):
            self.Paste()

    pytigon_gui.guictrl.ctrl.IMAGEVIEWER = Imageviewer
