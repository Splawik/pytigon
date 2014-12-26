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
from schcli.guilib.tools import bitmap_from_href


class ArtProviderFromIcon(wx.ArtProvider):

    def __init__(self):
        wx.ArtProvider.__init__(self)
        self.tab_16 = {}
        self.tab_22 = {}
        self.tab_32 = {}

        ids = open(wx.GetApp().scr_path + '/schappdata/media/ids.txt')
        for line in ids:
            l = line.replace('\n', '').split(',')
            if len(l) > 1:
                image_path = l[1]
                i = 'wx.ART_' + l[0]
                try:
                    wxid = eval(i)
                    self.tab_16[wxid] = [image_path, None]
                    self.tab_22[wxid] = [image_path, None]
                    self.tab_32[wxid] = [image_path, None]
                except:
                    pass
        ids.close()

    def CreateBitmap(
        self,
        artid2,
        client,
        size,
        ):
        artid = artid2.encode('utf-8')
        if size != 16 and size != 22 and size != 32:
            size = 32
        path = None
        if size == 16:
            if artid in self.tab_16:
                if self.tab_16[artid][1]:
                    return self.tab_16[artid][1]
                path = 'client://' + self.tab_16[artid][0] + '?size=0'
        elif size == 22:
            if artid in self.tab_22:
                if self.tab_22[artid][1]:
                    return self.tab_22[artid][1]
                path = 'client://' + self.tab_16[artid][0] + '?size=1'
        else:
            if artid in self.tab_32:
                if self.tab_32[artid][1]:
                    return self.tab_32[artid][1]
                path = 'client://' + self.tab_32[artid][0] + '?size=2'
        try:
            bitmap = bitmap_from_href(path)
        except:
            bitmap = None
        if bitmap:
            if size == 16:
                self.tab_16[artid][1] = bitmap
            elif size == 22:
                self.tab_22[artid][1] = bitmap
            else:
                self.tab_32[artid][1] = bitmap
            return bitmap
        else:
            return wx.NullBitmap
