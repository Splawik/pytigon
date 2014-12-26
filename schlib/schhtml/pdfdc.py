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

import os
import fpdf
from .basedc import BaseDc, BaseDcInfo
import io
import PIL

from schlib.schfs.vfstools import get_temp_filename

fpdf.fpdf.FPDF_FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../static/fonts")

class PDFSurface:
    def __init__(self, output_name, width, height):
        self.output_name = output_name
        self.width = width
        self.height = height
        self.pdf = fpdf.FPDF(unit='pt', orientation='L' if width > height else 'P')


        self.pdf.add_font('sans-serif', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.pdf.add_font('sans-serif', 'B', 'DejaVuSansCondensed-Bold.ttf', uni=True)
        self.pdf.add_font('sans-serif', 'I', 'DejaVuSansCondensed-Oblique.ttf', uni=True)
        self.pdf.add_font('sans-serif', 'BI', 'DejaVuSansCondensed-BoldOblique.ttf', uni=True)

        self.pdf.add_font('serif', '',  'DejaVuSerifCondensed.ttf', uni=True)
        self.pdf.add_font('serif', 'B', 'DejaVuSerifCondensed-Bold.ttf', uni=True)
        self.pdf.add_font('serif', 'I', 'DejaVuSerifCondensed-Italic.ttf', uni=True)
        self.pdf.add_font('serif', 'BI','DejaVuSerifCondensed-BoldItalic.ttf', uni=True)

        self.pdf.add_font('monospace', '',  'DejaVuSansMono.ttf', uni=True)
        self.pdf.add_font('monospace', 'B', 'DejaVuSansMono-Bold.ttf', uni=True)
        self.pdf.add_font('monospace', 'I', 'DejaVuSansMono-Oblique.ttf', uni=True)
        self.pdf.add_font('monospace', 'BI','DejaVuSansMono-BoldOblique.ttf', uni=True)

        self.fonts_map = { 'sans-serif': 'sans-serif', 'serif': 'serif', 'monospace': 'monospace', 'cursive': 'sans-serif', 'fantasy': 'sans-serif'}

        self.pdf.set_font('sans-serif','', 11)


    def get_dc(self):
        return self.pdf

    def save(self):
        self.pdf.output(self.output_name, 'F')

class PdfDc(BaseDc):

    def __init__(
        self,
        dc=None,
        calc_only=False,
        width=-1,
        height=-1,
        output_name=None,
        scale=1.0,
        ):
        BaseDc.__init__(self, calc_only, width, height, output_name, scale)
        if self.width >= 0:
            width2 = self.width
        else:
            width2 = self.default_width
        if self.height >= 0:
            height2 = self.height
        else:
            height2 = self.default_height
        self.dc_info = PdfDcInfo(self)
        self.type = None
        if self.calc_only:
            self.surf = PDFSurface(None, 10, 10)
            if width < 0:
                self.width = -1
            if height < 0:
                self.height = 1000000000
            self.dc = self.surf.get_dc()
        else:
            if dc:
                self.surf = None
                self.dc = dc
            else:
                if output_name:
                    name = output_name.lower()
                    self.surf = PDFSurface(output_name, width2, height2)
                else:
                    self.surf = PDFSurface(None, width2, height2)

                self.dc = self.surf.get_dc()

        self.last_style_tab = None
        self._color = (0, 0, 0, 255)
        self._line_width = 0
        self._fun_stack = []
        self._fill = False
        self._draw = False
        self._preserve = False

        self._last_pen = None
        self._last_brush = None
        self._last_pen_color = (0, 0, 0, 255)
        self._last_line_width = -1
        self._last_brush_color = (255, 255, 255, 255)
        self.start_page()

    def close(self):
        if not self.calc_only:
            self.surf.save()

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
        self.dc.add_page()
        BaseDc.start_page(self)

    def end_page(self):
        BaseDc.end_page(self)

    def draw(self, preserve=False):
        self._draw = True
        self._fill = False

        if self._last_pen_color != self._color or self._last_line_width != self._line_width:
            self.dc.set_draw_color(self._color[0], self._color[1], self._color[2])
            self.dc.set_text_color(self._color[0], self._color[1], self._color[2])
            self.dc.set_line_width(self._line_width)
            self._last_pen_color = self._color
            self._last_line_width = self._line_width
        self._draw_and_fill()
        self._draw = False
        if not preserve:
            self._fun_stack = []
        return BaseDc.draw(self, preserve)

    def fill(self, preserve=False):
        self._draw = False
        self._fill = True
        if self._last_brush_color != self._color:
            self.dc.set_fill_color(self._color[0], self._color[1], self._color[2])
            self._last_brush_color = self._color
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

        style = ""

        if style_tab[3] == '1':
            style +="I"
        if style_tab[4] == '1':
            style +="B"

        if style_tab[1] in self.surf.fonts_map:
            font_name = self.surf.fonts_map[style_tab[1]]
        else:
            font_name = 'sans-serif'
        self.dc.set_font(font_name,style,int((self.scale*self.base_font_size * int(style_tab[2])) / 100))
        (r, g, b) = self.rgbfromhex(style_tab[0])
        self.dc.set_text_color(r, g, b)
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
        self._add(self.dc.line, (x*self.scale, y*self.scale, (x + dx)*self.scale, (y + dy)*self.scale))
        BaseDc.add_line(self, x, y, dx, dy)

    def add_rectangle(
        self,
        x,
        y,
        dx,
        dy,
        ):
        self._add(self._rect, (x*self.scale, y*self.scale, dx*self.scale, dy*self.scale))
        BaseDc.add_rectangle(self, x, y, dx, dy)

    def add_rounded_rectangle(
        self,
        x,
        y,
        dx,
        dy,
        radius,
        ):
        self._add(self._rect_rounded, (x*self.scale, y*self.scale, dx*self.scale, dy*self.scale))
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
        BaseDc.add_ellipse(self, x, y, dx, dy)

    def add_polygon(self, xytab):
        BaseDc.add_polygon(self, xytab)

    def add_spline(self, xytab, close):
        BaseDc.add_spline(self, xytab)

# ------ Base graphics methods 4

    def draw_text(
        self,
        x,
        y,
        txt,
        ):
        dx, dx_space, dy_up, dy_down = self.dc_info.get_extents(txt)
        self.dc.text(x*self.scale, y*self.scale - dy_down - 2, txt)
        BaseDc.draw_text(self, x, y, txt)

    def draw_rotated_text(
        self,
        x,
        y,
        txt,
        angle,
        ):
        (w, h, d, e) = self.dc_info.get_extents(txt)
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

        png_stream = io.BytesIO(png_data)
        image = PIL.Image.open(png_stream)
        w, h = image.size

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
            if scale!=0:
                image.thumbnail((w * x_scale, h * y_scale), Image.ANTIALIAS)
            file_name = get_temp_filename("temp.png")
            image.save(file_name, "PNG")
            self.dc.image(file_name, x, y)
            os.remove(file_name)
        else:
            pass
            #delta_x = 0
            #delta_y = 0
            #while delta_y < dy:
            #    if scale == 4 and delta_y > 0:
            #        break
            #    delta_x = 0
            #    bmp = image.ConvertToBitmap()
            #    while delta_x < dx:
            #        if scale == 5 and delta_x > 0:
            #            break
            #        self.dc.DrawBitmap(bmp, x + delta_x, y + delta_y)
            #        delta_x += w
            #    delta_y += h
        BaseDc.draw_image(
            self,
            x,
            y,
            dx,
            dy,
            scale,
            png_data,
            )


    def _polygon(self, points):
        old_point = None
        for point in points:
            if old_point:
                self.dc.line(int(old_point[0]), int(old_point[1]), int(point[0]), int(point[1]))
            old_point = point

    def _rect(self, x, y, dx, dy):
        if self._fill == True and self._draw == False:
            return self.dc.rect(x, y, dx, dy, 'F')
        elif self._fill == False and self._draw == True:
            return self.dc.rect(x, y, dx, dy, 'D')
        else:
            return self.dc.rect(x, y, dx, dy, 'DF')

    def _rect_rounded(self, x, y, dx, dy):
        if self._fill == True and self._draw == False:
            return self.dc.rect(x, y, dx, dy, 'F')
        elif self._fill == False and self._draw == True:
            delta = 12
            points = [
                (x+delta, y), (x+dx-delta, y), (x+dx-delta/2, y+delta/6), (x+dx-delta/6, y+delta/2),
                (x+dx, y+delta), (x+dx, y+dy-delta), (x+dx-delta/6, y+dy-delta/2), (x+dx-delta/2, y+dy-delta/6),
                (x+dx-delta, y+dy), (x+delta, y+dy), (x+delta/2, y+dy-delta/6),(x+delta/6, y+dy-delta/2),
                (x, y+dy-delta), (x, y+delta), (x+delta/6, y+delta/2), (x+delta/2, y+delta/6),
                (x+delta, y)
                ]
            self._polygon(points)
        else:
            return self.dc.rect(x, y, dx, dy, 'DF')



class PdfDcInfo(BaseDcInfo):

    def __init__(self, dc):
        BaseDcInfo.__init__(self, dc)

    def get_line_dy(self, height):
        return height

    def get_extents(self, word, style=None):
        if style != None:
            self.dc.set_style(style)

        w = self.dc.dc.get_string_width(word)
        dx = w
        dy_up = self.dc.dc.font_size_pt
        dy_down = 0
        dx_space = self.dc.dc.get_string_width(' ')
        if word[-1] != ' ':
            dx_space = 0
        return (dx, dx_space, dy_up, dy_down)

    def get_text_width(self, txt, style=None):
        if style != None:
            self.dc.set_style(style)
        return self.dc.dc.get_string_width(txt)

    def get_text_height(self, txt, style=None):
        if style:
            self.dc.set_style(style)
        return self.dc.dc.font_size_pt

    def get_img_size(self, png_data):
        try:
            png_stream = io.BytesIO(png_data)
            image = PIL.Image.open(png_stream)
        except:
            image = None
        if image:
            w, h = image.size
            return (w, h)
        else:
            return (0, 0)

