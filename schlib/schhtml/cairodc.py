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


try:
    import cairo
except:
    pass
import io
from math import pi

from schcli.schhtml.basedc import BaseDc, BaseDcInfo

# A4 mm width, height = 2100, 2970
#
# A4 cale width, height = 8.28, 11.69
#
# A4 - 300dpi width, height = 2480, 3508

class CairoDc(BaseDc):

    def __init__(self, ctx=None, calc_only=False, width=-1, height=-1, output_name=None, scale=1.0):
        BaseDc.__init__(self, calc_only, width, height, output_name, scale)
        if self.width >= 0:
            width2 = self.width
        else:
            width2 = self.default_width
        if self.height >= 0:
            height2 = self.height
        else:
            height2 = self.default_height
        self.dc_info = CairoDcInfo(self)
        self.type = None
        if self.calc_only:
            self.surf = cairo.ImageSurface(cairo.FORMAT_RGB24, 10, 10)
            if width < 0:
                self.width = -1
            if height < 0:
                self.height = 1000000000
            self.ctx = cairo.Context(self.surf)
        else:
            if ctx:
                self.surf = None
                self.ctx = ctx
            else:
                if output_name:
                    name = output_name.lower()
                    if '.pdf' in name:
                        self.surf = cairo.PDFSurface(output_name, width2,
                                height2)
                        self.type = 'pdf'
                    elif '.svg' in name:
                        self.surf = cairo.SVGSurface(output_name, width2,
                                height2)
                        self.type = 'svg'
                    elif '.png' in name:
                        self.surf = cairo.ImageSurface(cairo.FORMAT_RGB24,
                                width2, height2)
                        self.type = 'png'
                    else:
                        self.surf = cairo.ImageSurface(cairo.FORMAT_RGB24,
                                width2, height2)
                else:
                    self.surf = cairo.ImageSurface(cairo.FORMAT_RGB24, width2,
                            height2)
                self.ctx = cairo.Context(self.surf)
        self.last_style_tab = None
        self.last_move_to = None
        self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)

    def close(self):
        if not self.calc_only:
            if self.type in ('svg', 'pdf'):
                self.ctx.show_page()
                self.surf.finish()
            if self.type in ('png', ):
                self.surf.write_to_png(self.output_name)
                self.surf.finish()

    def _move_to(self, x, y):
        self.ctx.move_to(x*self.scale, y*self.scale)
        self.last_move_to = (x*self.scale, y*self.scale)

    def start_page(self):
        self.ctx.show_page()
        BaseDc.start_page(self)

    def draw(self, preserve=False):
        if preserve:
            self.ctx.stroke_preserve()
        else:
            self.ctx.stroke()
        BaseDc.draw(self, preserve)

    def fill(self, preserve=False):
        if preserve:
            self.ctx.fill()
        else:
            self.ctx.fill()
        BaseDc.fill(self)

    def set_color(
        self,
        r,
        g,
        b,
        a=255,
        ):
        self.ctx.set_source_rgb(r / 256.0, g / 256.0, b / 256.0)
        BaseDc.set_color(self, r, g, b, a)

    def set_line_width(self, width):
        self.ctx.set_line_width(width*self.scale)
        BaseDc.set_line_width(self, width)

    def set_style(self, style):
        if style == self.last_style:
            return self.last_style_tab
        style_tab = self.dc_info.styles[style].split(';')
        self.last_style_tab = style_tab
        if style_tab[3] == '1':
            slant = cairo.FONT_SLANT_ITALIC
        else:
            slant = cairo.FONT_SLANT_NORMAL
        if style_tab[4] == '1':
            weight = cairo.FONT_WEIGHT_BOLD
        else:
            weight = cairo.FONT_WEIGHT_NORMAL
        self.ctx.select_font_face(style_tab[1], slant, weight)
        (r, g, b) = self.rgbfromhex(style_tab[0])
        self.ctx.set_font_size((self.scale*self.base_font_size * int(style_tab[2])) / 100)
        self.ctx.set_source_rgb(r / 256.0, g / 256.0, b / 256.0)
        BaseDc.set_style(self, style)
        return style_tab

    def add_line(self, x, y, dx, dy):
        self._move_to(x, y)
        self.ctx.line_to((x + dx)*self.scale, (y + dy)*self.scale)
        self.last_move_to = ((x + dx)*self.scale, (y + dy)*self.scale)
        BaseDc.add_line(self, x, y, dx, dy)

    def add_rectangle(self, x, y, dx, dy):
        self.ctx.rectangle(x*self.scale, y*self.scale, dx*self.scale, dy*self.scale)
        BaseDc.add_rectangle(self, x, y, dx, dy)

    def add_rounded_rectangle(self, x, y, dx, dy, radius):
        degrees = pi / 180.0
        self.ctx.new_sub_path()
        self.ctx.arc(((x + dx) - radius)*self.scale, (y + radius)*self.scale, radius*self.scale, -90 * degrees, 0
                      * degrees)
        self.ctx.arc(((x + dx) - radius)*self.scale, ((y + dy) - radius)*self.scale, radius*self.scale, 0 * degrees,
                     90 * degrees)
        self.ctx.arc((x + radius)*self.scale, ((y + dy) - radius)*self.scale, radius*self.scale, 90 * degrees, 180
                      * degrees)
        self.ctx.arc((x + radius)*self.scale, (y + radius)*self.scale, radius*self.scale, 180 * degrees, 270
                      * degrees)
        self.ctx.close_path()
        BaseDc.add_rounded_rectangle(self, x, y, dx, dy, radius)

    def add_arc(self, x, y, radius, angle1, angle2):
        self.ctx.arc(x*self.scale, y*self.scale, radius*self.scale, ((2 * pi) * angle1) / 360, ((2 * pi)
                      * angle2) / 360)
        BaseDc.add_arc(self, x, y, radius, angle1, angle2)

    def add_ellipse(self, x, y, dx, dy):
        self.ctx.save()
        self.ctx.translate((x + dx / 2)*self.scale, (y + dy / 2)*self.scale)
        self.ctx.scale(self.scale*dx / 2.0, self.scale*dy / 2.0)
        self.ctx.arc(0.0, 0.0, 1.0, 0.0, 2.0 * pi)
        self.ctx.restore()
        BaseDc.add_ellipse(self, x, y, dx, dy)

    def add_polygon(self, xytab):
        pos0 = xytab[0]
        self.ctx.move_to(pos0[0]*self.scale, pos0[1]*self.scale)
        for pos in xytab[1:]:
            self.ctx.line_to(pos[0]*self.scale, pos[1]*self.scale)
        self.ctx.close_path()
        self.last_move_to = [pos[0]*self.scale, pos[1]*self.scale]
        BaseDc.add_polygon(self, xytab)

    def add_spline(self, xytab, close):
        pos0 = xytab[0]
        self.ctx._move_to(pos0[0], pos0[1])
        for pos in xytab[1:]:
            self.ctx.line_to(pos[0], pos[1])
            self.last_move_to = pos
        if close:
            self.ctx.close_path()
            self.last_move_to = pos0
        BaseDc.add_spline(self, xytab)

    def draw_text(self, x, y, txt):
        sizes = self.ctx.text_extents(txt)[:4]
        self.ctx.move_to((x - sizes[0] / 2)*self.scale, y*self.scale)
        self.ctx.show_text(txt)
        BaseDc.draw_text(self, x, y, txt)

    def draw_rotated_text(self, x, y, txt, angle):
        self.ctx.save()
        self.ctx.move_to(x*self.scale, y*self.scale)
        self.ctx.rotate(((2 * pi) * angle) / 360)
        self.ctx.show_text(txt)
        self.ctx.restore()
        BaseDc.draw_rotated_text(self, x, y, txt, angle)

# scale: 0 - no scale, no repeat 1 - scale to dx, dy 2 - scale to dx or dy -
# preserve img scale 3 - scale to dx or dy - preserve img scale, fit fool image
# 4 - repeat x 5 - repeat y 6 - repeat x and y

    def draw_image(self, x, y, dx, dy, scale, png_data):
        try:
            png_stream = io.StringIO(png_data)
            surface = cairo.ImageSurface.create_from_png(png_stream)
        except:
            surface = cairo.ImageSurface.create_from_png('sleeptimer.png')
        w = surface.get_width()
        h = surface.get_height()
        self.ctx.save()
        self.ctx.rectangle(x, y, dx, dy)
        self.ctx.clip()
        (x_scale, y_scale) = self._scale_image(x, y, dx, dy, scale, w, h)
        if scale < 4:
            self.ctx.scale(x_scale, y_scale)
            self.ctx.set_source_surface(surface, x / x_scale, y / y_scale)
            self.ctx.paint()
        else:
            delta_x = 0
            delta_y = 0
            while delta_y < dy:
                if scale == 4 and delta_y > 0:
                    break
                delta_x = 0
                while delta_x < dx:
                    if scale == 5 and delta_x > 0:
                        break
                    self.ctx.set_source_surface(surface, x + delta_x, y + delta_y)
                    self.ctx.paint()
                    delta_x += w
                delta_y += h
        self.ctx.restore()
        BaseDc.draw_image(self, x, y, dx, dy, scale, png_data)


class CairoDcInfo(BaseDcInfo):
    def __init__(self, dc):
        BaseDcInfo.__init__(self, dc)

    def get_line_dy(self, height):
        return height * 12

    def get_extents(self, word, style):
        self.dc.set_style(style)
        sizes = self.dc.ctx.text_extents(word + '.')[:4]
        dx = sizes[2]
        dy_up = -1 * sizes[1]
        dy_down = sizes[3] - dy_up
        sizes2 = self.dc.ctx.text_extents('.')[:4]
        dx_space = sizes2[2]
        dx -= dx_space
        if word[-1] != ' ':
            dx_space = 0
        return (dx, dx_space, dy_up, dy_down)

    def get_text_width(self, txt, style):
        self.dc.set_style(style)
        (x_off, y_off, tw, th) = self.dc.ctx.text_extents(txt)[:4]
        return tw

    def get_text_height(self, txt, style):
        self.dc.set_style(style)
        (x_off, y_off, tw, th) = self.dc.ctx.text_extents(txt)[:4]
        return th

    def get_img_size(self, png_data):
        try:
            png_stream = io.StringIO(png_data)
            surface = cairo.ImageSurface.create_from_png(png_stream)
        except:
            surface = None
        if surface:
            w = surface.get_width()
            h = surface.get_height()
            return (w, h)
        else:
            return (0, 0)


def get_PdfCairoDc(result, width, height):
    surf = cairo.PDFSurface(result, width, height)
    ctx = cairo.Context(surf)
    ret = CairoDc(ctx=ctx, calc_only=False, width=width, height=height)
    ret.surf = surf
    return ret
