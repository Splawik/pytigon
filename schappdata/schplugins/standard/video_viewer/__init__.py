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
from io import StringIO
from PIL import Image
from schcli.guilib.schpil import piltoimage
# from  wx.lib import scrolledpanel


def init_plugin(
    app,
    mainframe,
    desktop,
    mgr,
    menubar,
    toolbar,
    accel,
    ):
    from schcli.guictrl.schctrl import SChBaseCtrl
    import schcli.guictrl.schctrl


    class Videoviewer(wx.ScrolledWindow):

        def __init__(self, *args, **kwds):
            self.obj = SChBaseCtrl(self, args, kwds)
# kwds['label']=wx.EmptyBitmap(2,2)

            wx.ScrolledWindow.__init__(self, *args, **kwds)
            self.static_bitmap = wx.StaticBitmap(self)
            if self.src:
                self.SetExt(self.src)
            self.last_clipboard_state = False
            mainframe.bind_to_toolbar(self.OnCopy, id=wx.ID_COPY)
            mainframe.bind_to_toolbar(self.OnCut, id=wx.ID_CUT)
            mainframe.bind_to_toolbar(self.OnPaste, id=wx.ID_PASTE)
            a_table = [(0, wx.WXK_F2, self.OnSave), (wx.ACCEL_CTRL, ord('S'),
                       self.OnSave)]
            self.SetAccKeyTab(a_table)
            self.resize_to_win = True
            self.Bind(wx.EVT_SIZE, self.OnSize)
            self.pil = None

        def on_size(self, event):
            if self.pil:
                size = self.GetParent().GetSize()
                resized = False
                if self.resize_to_win and (self.pil.size[0] > size[0]
                         or self.pil.size[1] > size[1]):
                    delta1 = (self.pil.size[0] * 1.0) / size[0]
                    delta2 = (self.pil.size[1] * 1.0) / size[1]
                    delta = delta1 if delta1 > delta2 else delta2
                    pos = (int(self.pil.size[0] / delta), int(self.pil.size[1]
                            / delta))
                    pil2 = self.pil.resize(pos, Image.BICUBIC)
                    resized = True
                else:
                    pil2 = self.pil
                img = piltoimage(pil2)
                self.static_bitmap.SetBitmap(img.ConvertToBitmap())
                if not resized:
                    self.SetVirtualSize(wx.Size(img.GetWidth(),
                                        img.GetHeight()))
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
            self.SetExt(ext)
            http = wx.GetApp().HTTP
            http.get(self, url)
            txt = http.ptr()
            io = StringIO(txt)
            self.pil = Image.open(io)
            size = self.GetParent().GetSize()
            resized = False
            if self.resize_to_win and (self.pil.size[0] > size[0]
                                        or self.pil.size[1] > size[1]):
                delta1 = (self.pil.size[0] * 1.0) / size[0]
                delta2 = (self.pil.size[1] * 1.0) / size[1]
                delta = delta1 if delta1 > delta2 else delta2
                pos = (int(self.pil.size[0] / delta), int(self.pil.size[1]
                        / delta))
# pos = (size[0]-5, size[1]-5) pil2 = self.pil.resize(pos, Image.ANTIALIAS) pil2
# = self.pil.resize(pos, Image.BILINEAR)
                pil2 = self.pil.resize(pos, Image.BICUBIC)
                resized = True
            else:
                pil2 = self.pil
            img = piltoimage(pil2)
            self.static_bitmap.SetBitmap(img.ConvertToBitmap())
            if not resized:
                self.SetVirtualSize(wx.Size(img.GetWidth(), img.GetHeight()))
                self.SetScrollRate(20, 20)

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

# def CanCopy(self): if self.GetSelectionEnd() - self.GetSelectionStart() != 0:
# return True else: return False
#
# def CanPaste(self): if self.last_clipboard_state or CodeEditor.CanPaste(self):
# self.last_clipboard_state = True return True else: return False

        def on_copy(self, event):
            self.Copy()

        def on_cut(self, event):
            self.Cut()

        def on_paste(self, event):
            self.Paste()


    schcli.guictrl.schctrl.VIDEOVIEWER = Videoviewer


