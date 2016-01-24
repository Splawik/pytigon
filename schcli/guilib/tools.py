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
from io import StringIO, BytesIO
#from .art_provider import ArtProviderFromIcon

size_default = -1
size_small = 0
size_medium = 1
size_large = 2

def norm_colour2(c):
    x = int(c)
    if x > 255:
        return 255
    else:
        return x


def norm_colour(
    r,
    g,
    b,
    proc,
    ):
    if proc > 1:
        y = (255, 255, 255)
        dx = 2 - proc
    else:
        y = (0, 0, 0)
        dx = proc
    dy = 1 - dx
    ret = [int(r * dx + y[0] * dy), int(g * dx + y[1] * dy), int(b * dx + y[1]
            * dy)]
    for i in range(3):
        if ret[i] > 255:
            ret[i] = 255
    return ret


def get_colour(wx_id, proc=None):
    c1 = wx.SystemSettings.GetColour(wx_id)
    if not proc:
        return c1.GetAsString(wx.C2S_HTML_SYNTAX)
    else:
        x = norm_colour(c1.Red(), c1.Green(), c1.Blue(), proc)
        c2 = wx.Colour(x[0], x[1], x[2])
        return c2.GetAsString(wx.C2S_HTML_SYNTAX)


def standard_tab_colour():
    return (
        ('color_body_0_2', get_colour(wx.SYS_COLOUR_3DFACE, 0.2)),
        ('color_body_0_5', get_colour(wx.SYS_COLOUR_3DFACE, 0.5)),
        ('color_body_0_7', get_colour(wx.SYS_COLOUR_3DFACE, 0.7)),
        ('color_body_0_9', get_colour(wx.SYS_COLOUR_3DFACE, 0.9)),
        ('color_body', get_colour(wx.SYS_COLOUR_3DFACE)),
        ('color_body_1_1', get_colour(wx.SYS_COLOUR_3DFACE, 1.1)),
        ('color_body_1_3', get_colour(wx.SYS_COLOUR_3DFACE, 1.3)),
        #('color_body_1_5', get_colour(wx.SYS_COLOUR_3DFACE, 1.5)),
        ('color_body_1_5', get_colour(wx.SYS_COLOUR_3DFACE, 0)),
        ('color_body_1_8', get_colour(wx.SYS_COLOUR_3DFACE, 1.8)),
        ('color_higlight', get_colour(wx.SYS_COLOUR_3DHIGHLIGHT)),
        ('color_shadow', get_colour(wx.SYS_COLOUR_3DSHADOW)),
        ('color_background_0_5', get_colour(wx.SYS_COLOUR_3DFACE, 0.5)),
        ('color_background_0_8', get_colour(wx.SYS_COLOUR_3DFACE, 0.8)),
        ('color_background_0_9', get_colour(wx.SYS_COLOUR_3DFACE, 0.9)),
        ('color_background', get_colour(wx.SYS_COLOUR_3DFACE)),
        ('color_background_1_1', get_colour(wx.SYS_COLOUR_3DFACE, 1.1)),
        ('color_background_1_2', get_colour(wx.SYS_COLOUR_3DFACE, 1.2)),
        ('color_background_1_5', get_colour(wx.SYS_COLOUR_3DFACE, 1.5)),
        ('color_info', get_colour(wx.SYS_COLOUR_INFOBK, 1.5)),
        )


def bitmap_from_art_id(bmp, size):
    #return ArtProviderFromIcon.GetBitmap(bmp, wx.ART_OTHER, size)
    return wx.ArtProvider.GetBitmap(bmp, wx.ART_OTHER)


def bitmaps_from_art_id(bmp, size):
    #bitmap = ArtProviderFromIcon.GetBitmap(bmp, wx.ART_OTHER, size)
    bitmap = wx.ArtProvider.GetBitmap(bmp, wx.ART_OTHER, size)
    img = bitmap.ConvertToImage()
    bitmap_disabled = \
        wx.BitmapFromImage(img.ConvertToGreyscale().AdjustChannels(1, 1, 1,
                           0.3))
    return (bitmap, bitmap_disabled)


def bitmap_from_href(href, size_type=size_default):
    size_type2 = size_type
    if '?' in href:
        x = href.split('?')
        href2 = x[0]
        if '=' in x[1]:
            try:
                size_type2 = int(x[1].split('=')[1])
            except:
                size_type2 = 1
    else:
        href2 = href
    if size_type2 == size_small:
        icon_size = 16
    elif size_type2 == size_medium:
        icon_size = 22
    else:
        icon_size = 32
    if href2[:3] == 'wx.':
        #bmp = ArtProviderFromIcon.GetBitmap(eval(href2), wx.ART_TOOLBAR, (icon_size,
        #                               icon_size))
        bmp = wx.ArtProvider.GetBitmap(eval(href2), wx.ART_TOOLBAR, (icon_size,
                                       icon_size))
    elif href.startswith('client://'):
        image = wx.Image(wx.GetApp().scr_path + '/schappdata/media/%dx%d/' % (icon_size,
                         icon_size) + href2[9:])
        bmp = wx.BitmapFromImage(image)
    elif href.startswith('fa://'):
        image = wx.Image(wx.GetApp().scr_path + '/static/fonts/font-awesome/fonts/%dx%d/' % (icon_size,icon_size) + href2[5:].replace('fa-','')+".png")
        image = image.AdjustChannels(1, 1, 1, 0.55)
        bmp = wx.BitmapFromImage(image)
    else:
        http = wx.GetApp().get_http(None)
        if http.get(None, str(href))[0]!=404:
            s = http.ptr()
            http.clear_ptr()
            stream = BytesIO(s)
            bmp = wx.BitmapFromImage(wx.ImageFromStream(stream))
        else:
            bmp = wx.Bitmap()
            print("bitmap_from_href: can't read from href:", href)
    return bmp


