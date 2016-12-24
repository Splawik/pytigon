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
from schlib.schhtml.basedc import BaseDc, BaseDcInfo
import io


class GraphicsContextDc(BaseDc):

    def __init__(self, ctx=None, calc_only=False, width=-1, height=-1, output_name=None):
        BaseDc.__init__(self, calc_only, width, height, output_name)
        self.dc_info = GraphicsContextDcinfo(self)
        self.type = None
        if self.calc_only:
            self.surf = wx.EmptyBitmap(10, 10, 32)
            dc = wx.MemoryDC(self.surf)
            dc.Clear()
            self.ctx = self._make_gc(dc)
            if width < 0:
                self.width = -1
            if height < 0:
                self.height = 1000000000
        else:
            if ctx:
                self.surf = None
                self.ctx = ctx
            else:
                if self.width >= 0:
                    width2 = self.width
                else:
                    width2 = self.default_width
                if self.height >= 0:
                    height2 = self.height
                else:
                    height2 = self.default_height
                self.surf = wx.EmptyBitmap(width2, height2, 32)
                if output_name:
                    self.type = 'png'
                dc = wx.MemoryDC(self.surf)
                dc.Clear()
                self.ctx = self._make_gc(dc)
        self.path = None
        self.colour = wx.Colour(0, 0, 0)
        self.line_width = 1
        self._move_x = 0
        self._move_y = 0
        self.last_style_tab = None

    def _make_gc(self, dc):
        try:
            gc = wx.GraphicsContext.Create(dc)
        except NotImplementedError:
            dc.DrawText('This build of wxPython does not support the wx.GraphicsContext family of classes.'
                        , 25, 25)
            return None
        return gc

    def close(self):
        if not self.calc_only:
            if self.type in ('png', ):
                image = self.surf.ConvertToImage()
                image.SaveFile(self.output_name, wx.BITMAP_TYPE_PNG)

    def new_page(self):
        BaseDc.new_page(self)

    def new_path(self):
        self.path = self.ctx.CreatePath()
        BaseDc.new_path(self)

    def stroke(self):
        if not self.calc_only:
            self.ctx.StrokePath(self.path)
        self.path = None
        BaseDc.stroke(self)

    def fill(self):
        if not self.calc_only:
            self.ctx.FillPath(self.path)
        self.path = None
        BaseDc.fill(self)

    def draw(self):
        if not self.calc_only:
            self.ctx.DrawPath(self.path)
        self.path = None
        BaseDc.draw(self)

    def move_to(self, x, y):
        self._move_x = x
        self._move_y = y
        if self.path:
            self.path.MoveToPoint(x, y)
        BaseDc.move_to(self, x, y)

    def line_to(self, x, y):
        self.path.AddLineToPoint(x, y)
        BaseDc.move_to(self, x, y)

    def show_text(self, txt):
        (w, h, d, e) = self.ctx.GetFullTextExtent(txt)
        dy_up = h - d
        self.ctx.DrawText(txt, self._move_x, self._move_y - dy_up)
        BaseDc.show_text(self, txt)

    def set_pen(self, r, g, b, a=255, width=1):
        pen = wx.Pen(wx.Colour(r, g, b, a))
        self.ctx.SetPen(pen)
        BaseDc.set_pen(self, r, g, b, a, width)

    def set_brush(self, r, g, b, a=255):
        brush = wx.Brush(wx.Colour(r, g, b, a))
        self.ctx.SetBrush(brush)
        BaseDc.set_brush(self, r, g, b, a)

    def set_style(self, style):
        if style == self.last_style:
            return self.last_style_tab
        style_tab = self.dc_info.styles[style].split(';')
        self.last_style_tab = style_tab
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        if style_tab[3] == '1':
            slant = wx.ITALIC
            font.SetStyle(wx.ITALIC)
        else:
            slant = wx.NORMAL
        if style_tab[4] == '1':
            weight = wx.BOLD
            font.SetWeight(wx.BOLD)
        else:
            weight = wx.FONTWEIGHT_NORMAL
        if style_tab[1] == 'serif':
            font_style = wx.ROMAN
            font.SetFamily(wx.ROMAN)
        elif style_tab[1] == 'sans-serif':
            font_style = wx.SWISS
            font.SetFamily(wx.SWISS)
        elif style_tab[1] == 'monospace':
            font_style = wx.MODERN
            font.SetFamily(wx.MODERN)
        elif style_tab[1] == 'cursive':
            font_style = wx.SCRIPT
            font.SetFamily(wx.SCRIPT)
        elif style_tab[1] == 'fantasy':
            font_style = wx.DECORATIVE
            font.SetFamily(wx.DECORATIVE)
        else:
            font_style = wx.DEFAULT
        font.SetPointSize((self.base_font_size * int(style_tab[2])) / 100.0)
        self.ctx.SetFont(font)
        (r, g, b) = self.rgbfromhex(style_tab[0])
        self.ctx.SetPen(wx.Pen(wx.Colour(r, g, b)))
        BaseDc.set_style(self, style)
        return style_tab

    def draw_atom_line(self, x, y, line):
        dx = 0
        test = 0
        for obj in line.objs:
            if obj.style >= 0:
                style = self.set_style(obj.style)
                if style[5] == '1':
                    self.new_path()
                    self.move_to(x + dx, y + line.dy_up + line.dy_down)
                    self.line_to(x + dx + obj.dx, y + line.dy_up + line.dy_down)
                    self.stroke()
            if type(obj.data)==str:
                ret = False
                if obj.parent and hasattr(obj.parent, 'draw_atom'):
                    ret = obj.parent.draw_atom(self, obj.style, x + dx, (y
                             + line.dy_up) - obj.dy_up)
                if not ret:
                    self.move_to(x + dx, y + line.dy_up)
                    self.show_text(obj.data)
            else:
                obj.data.draw_atom(self, obj.style, x + dx, (y + line.dy_up) - obj.dy_up)
            dx += obj.dx

    def rectangle(self, x, y, dx, dy):
        self.path.AddRectangle(x, y, dx, dy)
        BaseDc.rectangle(self, x, y, dx, dy)

    def draw_line(self, x, y, dx, dy):
        self.path.MoveToPoint(x, y)
        self.path.AddLineToPoint(x + dx, y + dy)
        BaseDc.draw_line(self, x, y, dx, dy)

#  scale: 0 - no scale, no repeat 1 - scale to dx, dy 2 - scale to dx or dy -
# preserve img scale 3 - scale to dx or dy - preserve img scale, fit fool image
# 4 - repeat x 5 - repeat y 6 - repeat x and y

    def draw_image(self, x, y, dx, dy, scale, png_data):
        png_stream = io.StringIO(png_data)
        image = wx.ImageFromStream(png_stream)
        w = image.GetWidth()
        h = image.GetHeight()
        (x_scale, y_scale) = self._scale_image(x, y, dx, dy, scale, w, h)
        if scale < 4:
            image.Rescale(w * x_scale, h * y_scale)
            bmp = image.ConvertToBitmap()
            w = image.GetWidth()
            h = image.GetHeight()
            self.ctx.DrawBitmap(bmp, x, y, w, h)
        else:
            delta_x = 0
            delta_y = 0
            while delta_y < dy:
                if scale == 4 and delta_y > 0:
                    break
                delta_x = 0
                bmp = image.ConvertToBitmap()
                while delta_x < dx:
                    if scale == 5 and delta_x > 0:
                        break
                    self.ctx.DrawBitmap(bmp, x + delta_x, y + delta_y, w, h)
                    delta_x += w
                delta_y += h
        BaseDc.draw_image(self, x, y, dx, dy, scale, png_data)


class GraphicsContextDcinfo(BaseDcInfo):

    def __init__(self, dc):
        BaseDcInfo.__init__(self, dc)

    def get_line_dy(self, height):
        return height * 3

    def get_extents(self, word, style):
        self.dc.set_style(style)
        (w, h, d, e) = self.dc.ctx.GetFullTextExtent('-' + word + '-')
        dx = w
        dy_up = h - d
        dy_down = h - dy_up
        (w2, h2) = self.dc.ctx.GetTextExtent('-')
        dx_space = w2
        dx -= 2 * dx_space
        if word[-1] != ' ':
            dx_space = 0
        return (dx, dx_space, dy_up, dy_down)

    def get_text_width(self, txt, style):
        self.dc.set_style(style)
        (tw, th) = self.dc.ctx.GetTextExtent(txt)
        return tw

    def get_text_height(self, txt, style):
        self.dc.set_style(style)
        (tw, th) = self.dc.ctx.GetTextExtent(txt)
        return th

    def get_img_size(self, png_data):
        try:
            png_stream = io.StringIO(png_data)
            image = wx.ImageFromStream(png_stream)
        except:
            image = None
        if image:
            w = image.GetWidth()
            h = image.GetHeight()
            return (w, h)
        else:
            return (0, 0)


