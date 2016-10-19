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

from PIL import Image
import wx


def bitmap_to_pil(bitmap):
    return image_to_pil(bitmap_to_image(bitmap))


def bitmap_to_image(bitmap):
    return wx.ImageFromBitmap(bitmap)


def pil_to_bitmap(pil):
    return image_to_bitmap(pil_to_image(pil))


def pil_to_image(pil):
    image = wx.EmptyImage(pil.size[0], pil.size[1])
    image.SetData(pil.convert('RGB').tostring())
    return image


def piltoimage(pil, alpha=True):
    if alpha:
        image = wx.EmptyImage(*pil.size)
        image.SetData(pil.convert('RGB').tobytes())
        #image.SetAlphaData(pil.convert('RGBA').tostring()[3::4])
        image.SetAlphaBuffer(pil.convert('RGBA').tobytes()[3::4])
    else:
        image = wx.EmptyImage(pil.size[0], pil.size[1])
        new_image = pil.convert('RGB')
        data = new_image.tobytes()
        image.SetData(data)
    return image


def image_to_pil(image):
    pil = Image.new('RGB', (image.GetWidth(), image.GetHeight()))
    pil.fromstring(image.GetData())
    return pil


def image_to_bitmap(image):
    return image.ConvertToBitmap()


