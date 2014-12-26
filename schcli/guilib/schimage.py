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
import io
import imp
import sys


def get_mondrian_icon():
    icon = wx.EmptyIcon()
# icon.CopyFromBitmap(GetMondrianBitmap()) FRAME_ICON
    b = wx.ArtProvider.GetBitmap(wx.ART_FRAME_ICON, wx.ART_TOOLBAR, (32, 32))
    icon.CopyFromBitmap(b)
    return icon


class SchImage:

    def __init__(self, address, ilosc=0):
        try:
            http = wx.GetApp().HTTP
            (status, ur) = http.get(self, address)
            if status == 404:
                self.bmp = wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE,
                        wx.ART_TOOLBAR, (32, 32))
            else:
                str = http.ptr()
                stream = io.BytesIO(str)
                self.bmp = wx.BitmapFromImage(wx.ImageFromStream(stream))
            http.clear_ptr()
        except:
            self.bmp = wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE,
                    wx.ART_TOOLBAR, (32, 32))

    def __getitem__(self, key):
        rect = wx.Rect(21 * int(key), 0, 20, 20)
        try:
            ret = self.bmp.GetSubBitmap(rect)
        except:
            ret = wx.ArtProvider.GetBitmap(wx.ART_MISSING_IMAGE, wx.ART_TOOLBAR, (32, 32))

        #return self.bmp.GetSubBitmap(rect)
        return ret


