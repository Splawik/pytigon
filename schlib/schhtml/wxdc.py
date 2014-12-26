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
from .basedc import BaseDc, BaseDcInfo
import io
from base64 import b32decode
# import cairo as C import cairo
#
# A4 mm width, height = 2100, 2970
#
# A4 cale width, height = 8.28, 11.69
#
# A4 - 300dpi width, height = 2480, 3508


class DcDc(BaseDc):

    def __init__(
        self,
        dc=None,
        calc_only=False,
        width=-1,
        height=-1,
        output_name=None,
        scale = 1.0,
        ):
        BaseDc.__init__(self, calc_only, width, height, output_name, scale)
        self.dc_info = DcDcinfo(self)
        if self.width >= 0:
            width2 = self.width
        else:
            width2 = self.default_width
        if self.height >= 0:
            height2 = self.height
        else:
            height2 = self.default_height
        self.type = None
        if self.calc_only:
            self.surf = wx.EmptyBitmap(10, 10, 32)
            self.dc = wx.MemoryDC(self.surf)
            self.dc.Clear()
            if width < 0:
                self.width = -1
            if height < 0:
                self.height = 1000000000
        else:
            if dc:
                self.surf = None
                self.dc = dc
            else:
                if output_name:
                    name = output_name.lower()
                    self.surf = wx.EmptyBitmap(width2, height2, 32)
                    self.dc = wx.MemoryDC(self.surf)
                    self.dc.Clear()
                    if '.jpg' in name or '.jpeg' in name:
                        self.type = 'jpg'
                    else:
                        self.type = 'png'
                else:
                    self.surf = wx.EmptyBitmap(10, 10, 32)
                    self.dc = wx.MemoryDC(self.surf)
        self.last_style_tab = None
        self._color = (0, 0, 0, 255)
        self._line_width = 0
        self._fun_stack = []
        self._fill = False
        self._draw = False
        self._preserve = False
        self.transparent_brush = wx.Brush(wx.Colour(255, 255, 255),
                style=wx.TRANSPARENT)
        self.transparent_pen = wx.Pen(wx.Colour(255, 255, 255), width=0,
                                      style=wx.TRANSPARENT)
        #self._last_pen = wx.Pen(wx.Colour(0, 0, 0), 1.0*self.scale, style=wx.SOLID)
        self._last_pen = None
        self._last_brush = wx.Brush(wx.Colour(255, 255, 255), style=wx.SOLID)
        self._last_pen_color = (0, 0, 0, 255)
        #self._last_line_width = 1.0*scale
        self._last_line_width = -1
        self._last_brush_color = (255, 255, 255, 255)

    def close(self):
        if not self.calc_only:
            if self.type:
                img = self.surf.ConvertToImage()
                ext = wx.BITMAP_TYPE_PNG
                if self.type == 'jpg':
                    ext = wx.BITMAP_TYPE_JPEG
                img.SaveFile(self.output_name, ext)

    def set_scale(self, scale):
        self.scale = scale
        self._last_line_width = -1
        self._last_pen = None
        return BaseDc.set_scale(self, scale)

    def _add(self, fun, args):
        self._fun_stack.append((fun, args))

    def _spline(self, points):
        if self.fill:
            self.dc.DrawSpline(points)
        else:
            self.dc.DrawSpline(points)

    def _draw_and_fill(self):
        for fun_arg in self._fun_stack:
            fun_arg[0](*fun_arg[1])

# ------ Base graphics methods

    def start_page(self):
        self.dc.StartPage()
        BaseDc.start_page(self)

    def end_page(self):
        self.dc.EndPage()
        BaseDc.end_page(self)

    def draw(self, preserve=False):
        self._draw = True
        self._fill = False
        self.dc.SetBrush(self.transparent_brush)
        if self._last_pen_color != self._color or self._last_line_width\
             != self._line_width:
            self._last_pen = wx.Pen(wx.Colour(self._color[0], self._color[1],
                                    self._color[2]), (self._line_width+0.49)*self.scale,
                                    style=wx.SOLID)
            self._last_pen_color = self._color
            self._last_line_width = self._line_width
        self.dc.SetPen(self._last_pen)
        self._draw_and_fill()
        self._draw = False
        if not preserve:
            self._fun_stack = []
        return BaseDc.draw(self, preserve)

    def fill(self, preserve=False):
        self._draw = False
        self._fill = True
        self.dc.SetPen(self.transparent_pen)
        if self._last_brush_color != self._color:
            self._last_brush = wx.Brush(wx.Colour(self._color[0],
                                        self._color[1], self._color[2]),
                                        style=wx.SOLID)
            self._last_brush_color = self._color
        self.dc.SetBrush(self._last_brush)
        self._draw_and_fill()
        self._fill = False
        if not preserve:
            self._fun_stack = []
        return BaseDc.fill(self, preserve)

# ------ Base graphics methods 2

    def set_color(
        self,
        r,
        g,
        b,
        a=255,
        ):
        self._color = (r, g, b, a)
        BaseDc.set_color(self, r, g, b, a)

    def set_line_width(self, width):
        self._line_width = width
        BaseDc.set_line_width(self, width)

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
        font.SetPointSize((self.scale * (self.base_font_size * 72) * int(style_tab[2])) / (96
                           * 100.0))
        self.dc.SetFont(font)
        (r, g, b) = self.rgbfromhex(style_tab[0])
        self.dc.SetTextForeground(wx.Colour(r, g, b))
        self.set_color(r, g, b)
# self.dc.SetPen(wx.Pen(wx.Colour(r, g, b)))
        BaseDc.set_style(self, style)
        return style_tab

# ------ Base graphics methods 3

    def add_line(
        self,
        x,
        y,
        dx,
        dy,
        ):
        self._add(self.dc.DrawLine, (x*self.scale, y*self.scale, (x + dx)*self.scale, (y + dy)*self.scale))
        BaseDc.add_line(self, x, y, dx, dy)

    def add_rectangle(
        self,
        x,
        y,
        dx,
        dy,
        ):
        self._add(self.dc.DrawRectangle, (x*self.scale, y*self.scale, dx*self.scale, dy*self.scale))
        BaseDc.add_rectangle(self, x, y, dx, dy)

    def add_rounded_rectangle(
        self,
        x,
        y,
        dx,
        dy,
        radius,
        ):
        self._add(self.dc.DrawRoundedRectangle, (x*self.scale, y*self.scale, dx*self.scale, dy*self.scale, radius*self.scale))
        BaseDc.add_rounded_rectangle(
            self,
            x,
            y,
            dx,
            dy,
            radius,
            )

    def add_arc(
        self,
        x,
        y,
        radius,
        angle1,
        angle2,
        ):
        self._add(self.dc.DrawEllipticArc, (
            (x + radius)*self.scale,
            (y + radius)*self.scale,
            radius*2*self.scale,
            radius*2*self.scale,
            (360 - angle1)*self.scale,
            (360 - angle2)*self.scale,
            ))
        BaseDc.add_arc(
            self,
            x,
            y,
            radius,
            angle1,
            angle2,
            )

    def add_ellipse(
        self,
        x,
        y,
        dx,
        dy,
        ):
        self._add(self.dc.DrawEllipse, (x*self.scale, y*self.scale, dx*self.scale, dy*self.scale))
        BaseDc.add_ellipse(self, x, y, dx, dy)

    def add_polygon(self, xytab):
        tabpoints = []
        for pos in xytab:
            tabpoints.append(wx.Point(pos[0]*self.scale, pos[1]*self.scale))
        self._add(self.dc.DrawPolygon, (tabpoints, ))
        BaseDc.add_polygon(self, xytab)

    def add_spline(self, xytab, close):
        tabpoints = []
        for pos in xytab:
            tabpoints.append(wx.Point(pos[0]*self.scale, pos[1]*self.scale))
        self._add(self._spline, (self, tabpoints))
        BaseDc.add_spline(self, xytab)

# ------ Base graphics methods 4

    def draw_text(
        self,
        x,
        y,
        txt,
        ):
        (w, h, d, e) = self.dc.GetFullTextExtent(txt)
        dy_up = h - d
        self.dc.DrawText(txt, x*self.scale, y*self.scale - dy_up)
        BaseDc.draw_text(self, x, y, txt)

    def draw_rotated_text(
        self,
        x,
        y,
        txt,
        angle,
        ):
        (w, h, d, e) = self.dc.GetFullTextExtent(txt)
        dy_up = h - d
        self.dc.DrawRotatedText(txt, x*self.scale + dy_up, y*self.scale, 360 - angle)
        BaseDc.draw_rotated_text(self, x, y, txt)

# scale: 0 - no scale, no repeat 1 - scale to dx, dy 2 - scale to dx or dy -
# preserve img scale 3 - scale to dx or dy - preserve img scale, fit fool image
# 4 - repeat x 5 - repeat y 6 - repeat x and y

    def draw_image(
        self,
        x,
        y,
        dx,
        dy,
        scale,
        png_data,
        ):

# image = wx.Image(png_name) try: image = wx.Image(png_name) except: image =
# wx.Image("sleeptimer.png") print "No:", png_name
#
# png_stream = cStringIO.StringIO(b32decode(png_data))
        png_stream = io.BytesIO(png_data)
        image = wx.ImageFromStream(png_stream)
        w = image.GetWidth()
        h = image.GetHeight()
        (x_scale, y_scale) = self._scale_image(
            x,
            y,
            dx,
            dy,
            scale,
            w,
            h,
            )
        if scale < 4:
            image.Rescale(w * x_scale, h * y_scale)
            bmp = image.ConvertToBitmap()
            w = image.GetWidth()
            h = image.GetHeight()
            self.dc.DrawBitmap(bmp, x, y)
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
                    self.dc.DrawBitmap(bmp, x + delta_x, y + delta_y)
                    delta_x += w
                delta_y += h
        BaseDc.draw_image(
            self,
            x,
            y,
            dx,
            dy,
            scale,
            png_data,
            )


class DcDcinfo(BaseDcInfo):

    def __init__(self, dc):
        BaseDcInfo.__init__(self, dc)

    def get_line_dy(self, height):
        return height * 3

    def get_extents(self, word, style):
        self.dc.set_style(style)
        (w, h, d, e) = self.dc.dc.GetFullTextExtent('-' + word + '-')
        dx = w
        dy_up = h - d
        dy_down = h - dy_up
        (w2, h2) = self.dc.dc.GetTextExtent('-')
        dx_space = w2
        dx -= 2 * dx_space
        if word[-1] != ' ':
            dx_space = 0
        return (dx, dx_space, dy_up, dy_down)

    def get_text_width(self, txt, style):
        self.dc.set_style(style)
        (tw, th) = self.dc.dc.GetTextExtent(txt)
        return tw

    def get_text_height(self, txt, style):
        self.dc.set_style(style)
        (tw, th) = self.dc.dc.GetTextExtent(txt)
        return th

    def get_img_size(self, png_data):
        try:
# png_stream = cStringIO.StringIO(b32decode(png_data))
            png_stream = io.BytesIO(png_data)
            image = wx.Image(png_stream)
            #image = wx.ImageFromStream(png_stream)
            
        except:
            image = None
        if image:
            w = image.GetWidth()
            h = image.GetHeight()
            return (w, h)
        else:
            return (0, 0)


