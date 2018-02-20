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


import zipfile
import io
import json


class BaseDc(object):

    def __init__(self,calc_only=False,width=-1,height=-1,output_name=None,scale=1.0):
        self.x = 0
        self.y = 0
        self.gparent = None
        self.dc_info = None

        self.store = []
        self.rec = True
        self.calc_only = calc_only

        self.default_height = 595
        self.default_width = 842
        self.width = width
        self.height = height
        self.output_name = output_name
        self.base_font_size = 10
        self.paging = False
        self.pages = []
        self._maxwidth = 0
        self._maxheight = 0
        self.last_style = 'None'
        self.scale = scale

    def close(self):
        pass

    def state(self):
        rec = [len(self.pages),self.width,self.height,self.base_font_size,self.paging,self._maxwidth,self._maxheight]
        if self.dc_info:
            rec.append(self.dc_info.styles)
        else:
            rec.append([])
        rec.append(self.last_style)
        return rec

    def set_scale(self, scale):
        self.scale = scale

    def restore_state(self, state):
        self.width = state[1]
        self.height = state[2]
        self.base_font_size = state[3]
        self.paging = state[4]
        self._maxwidth = state[5]
        self._maxheight = state[6]
        if self.dc_info:
            self.dc_info.styles=state[7]
        self.last_style = state[8]

    def get_max_sizes(self):
        return (self._maxwidth, self._maxheight)

    def test_point(self, x, y):
        if x > self._maxwidth:
            self._maxwidth = x
        if y > self._maxheight:
            self._maxheight = y

    def set_paging(self, enable=True):
        self.paging = enable

    def get_page_count(self):
        return len(self.pages)

    def set_base_font_size(self, size):
        self.base_font_size = size

    def is_calc_only(self):
        return self.calc_only

    def get_size(self):
        return [self.width, self.height]

    def rgbfromhex(self, hex):
        if len(hex) == 4:  #  #000
            (r, g, b) = (hex[1], hex[2], hex[3])
            (r, g, b) = [int(n, 16) * 16 for n in (r, g, b)]
        elif len(hex) == 7:  # #00ff00
            (r, g, b) = (hex[1:3], hex[3:5], hex[5:])
            (r, g, b) = [int(n, 16) for n in (r, g, b)]
        else:
            r = 0
            g = 0
            b = 0
        return (r, g, b)

    def subdc(self,x,y,dx,dy,reg_max=True,):
        return SubDc(self,x,y,dx,dy,reg_max)

    def get_dc_info(self):
        return self.dc_info

    def record(self, name, args=None):
        if self.rec:
            self.store.append((name, args))

    def play(self, page=-1):
        rec = self.rec
        self.rec = False
        if page >= 0:
            self.store = self.pages[page]
        for pos in self.store:
            fun = getattr(self, pos[0])
            if pos[1]:
                fun(*pos[1])
            else:
                fun()
        self.rec = rec

    def play_str(self, str):
        for buf in str.split('\n'):
            buf = buf.strip()
            if buf != '':
                pos = json.loads(buf)
                fun = getattr(self, pos[0])
                if pos[1]:
                    fun(*pos[1])
                else:
                    fun()

    def save(self, zip_name):
        zf = zipfile.ZipFile(zip_name, mode='w',
                             compression=zipfile.ZIP_DEFLATED)
        zf.writestr('set.dat', json.dumps(self.state()))
        i = 1
        for page in self.pages:
            buf = io.BytesIO()
            for rec in page:
                try:
                    buf.write(json.dumps(rec))
                except:
                    print('basedc:', rec.__class__, rec)
                buf.write(b'\n')
            zf.writestr('page_%d' % i, buf.getvalue())
            i += 1
        zf.close()

    def load(self, zip_name):
        zf = zipfile.ZipFile(zip_name, mode='r')
        parm = json.loads(zf.read('set.dat').decode('utf-8'))
        count = parm[0]
        self.pages = []
        self.width = parm[1]
        self.height = parm[2]
        self.base_font_size = parm[3]
        self.paging = parm[4]
        self._maxwidth = parm[5]
        self._maxheight = parm[6]
        if self.dc_info:
            self.dc_info.styles = parm[7]
        for i in range(1, count + 1):
            rec = []
            data = zf.read('page_%d' % i).decode('utf-8')
            for line in data.split('\n'):
                if len(line) > 1:
                    buf = json.loads(line)
                    rec.append(buf)
            self.pages.append(rec)
            self.rec = rec
        zf.close()

    def _scale_image(self,x,y,dx,dy,scale,image_w,image_h):
        if scale < 4:
            x_scale = 1
            y_scale = 1
            if scale > 0:
                if dx > 0:
                    x_scale = dx / image_w
                    if dy > 0:
                        y_scale = dy / image_h
                    else:
                        y_scale = x_scale
                else:
                    if dy > 0:
                        y_scale = dy / image_h
                        x_scale = y_scale
                    else:
                        x_scale = 1
                        y_scale = 1
                if scale == 2:
                    if x_scale < y_scale:
                        x_scale = y_scale
                    else:
                        y_scale = x_scale
                if scale == 3:
                    if x_scale < y_scale:
                        y_scale = x_scale
                    else:
                        x_scale = y_scale
        else:
            x_scale = 1
            y_scale = 1
        return (x_scale, y_scale)

    def end_document(self):
        if len(self.store) > 0:
            self.pages.append(self.store)

    def start_page(self):
        if len(self.store) > 0:
            self.pages.append(self.store)
            self.store = []
        self.last_style = 'None'

    def end_page(self):
        if len(self.store) > 0:
            self.pages.append(self.store)
            self.store = []
        self.last_style = 'None'

    def fill(self, *args):
        self.record('fill', args)

    def draw(self, *args):
        self.record('draw', args)

    def set_color(self, *args):
        self.record('set_color', args)

    def set_line_width(self, *args):
        self.record('set_line_width', args)

    def set_style(self, *args):
        self.last_style = args[0]
        self.record('set_style', args)

    def add_line(self, *args):
        self.record('add_line', args)

    def add_rectangle(self, *args):
        self.record('add_rectangle', args)

    def add_rounded_rectangle(self, *args):
        self.record('add_rounded_rectangle', args)

    def add_arc(self, *args):
        self.record('add_arc', args)

    def add_ellipse(self, *args):
        self.record('add_ellipse', args)

    def add_polygon(self, *args):
        self.record('add_polygon', args)

    def add_spline(self, *args):
        self.record('add_spline', args)

    def draw_text(self, *args):
        self.record('draw_text', args)

    def draw_rotated_text(self, *args):
        self.record('draw_rotated_text', args)

    def draw_image(self, *args):
        self.record('draw_image', args)

    def draw_atom_line(self,x,y,line):
        self.last_style = 'None'
        dx = 0
        test = 0
        for obj in line.objs:
            if obj.style and obj.style >= 0:
                style = self.set_style(obj.style)
            else:
                style = self.set_style(0)
            if style[5] == '1':
                self.add_line((x + dx) - 1, y + line.dy_up + 2, obj.dx
                               - obj.dx_space + 1, 0)
                self.draw()
            if type(obj.data)==str:
                ret = False
                if obj.parent and hasattr(obj.parent, 'draw_atom'):
                    ret = obj.parent.draw_atom(
                        self,
                        obj.style,
                        x + dx,
                        (y + line.dy_up) - obj.dy_up,
                        obj.get_width(),
                        obj.get_height(),
                        )
                if not ret:
                    self.draw_text(x + dx, y + line.dy_up, obj.data.replace('»',' '))
            else:
                obj.data.draw_atom(
                    self,
                    obj.style,
                    x + dx,
                    (y + line.dy_up) - obj.dy_up,
                    obj.get_width(),
                    obj.get_height(),
                    )
            dx += obj.dx


class BaseDcInfo(object):
    def __init__(self, dc):
        self.dc = dc
        self.styles = []

    def get_text_width(self, txt, style):
        return 12 * len(txt)

    def get_text_height(self, txt, style):
        return 12

    def get_line_dy(self, height):
        return height * 12

    def get_multiline_text_width(self, txt, style='default'):
        txt_tab = txt.split(' ')
        minsize = 0
        for word in txt_tab:
            size = self.get_text_width(word, style)
            if size > minsize:
                minsize = size
        maxsize = self.get_text_width(txt, style)
        if len(txt_tab) > 16:
            optsize = (maxsize * 16) / len(txt_tab)
        else:
            optsize = maxsize
        return (optsize, minsize, maxsize)

    def get_multiline_text_height(self,txt,width,style='default'):
        lines = []
        line = ''
        line_ok = ''
        dy = 0
        txt_tab = txt.dc.split(' ')
        for pos in txt_tab:
            if line == '':
                line = pos
            else:
                line = line + ' ' + pos
            if self.get_text_width(line, style) > width:
                lines.append(line_ok)
                dy += self.get_text_height(line_ok, style)
                line = pos
                line_ok = pos
            else:
                line_ok = line
        if line_ok != '':
            lines.append(line_ok)
            dy += self.get_text_height(line_ok, style)
        return (dy, lines)

    def get_extents(self, word, style):
        dx = self.get_text_width(word, style)
        dx_space = self.get_text_width(' ', style)
        dy = self.get_test_height(word, style)
        dy_up = dy / 2
        dy_down = dy - dy_up
        return (dx, dx_space, dy_up, dy_down)

    def get_style_id(self, style):
        i = 0
        for pos in self.styles:
            if style == pos:
                return i
            i += 1
        self.styles.append(style)
        return i


def convert_fun_arg(fn):
    def fun(self, *args, **kwargs):
        dx = 0
        dy = 0
        test = 0
        if len(args) > 1:
            dx = args[0]
            dy = args[1]
            arg1 = dx + self.x
            arg2 = dy + self.y
            test = 1
        else:
            if 'x' in kwargs:
                dx = kwargs['x']
                kwargs['x'] = dx + self.x
            if 'y' in kwargs:
                dy = kwargs['y']
                kwargs['y'] = dy + self.y
        if len(args) > 3:
            if args[2] == -1:
                arg3 = self.dx - dx
            else:
                arg3 = args[2]
            if args[3] == -1:
                arg4 = self.dy - dy
            else:
                arg4 = args[3]
            test = 2
        else:
            if 'dx' in kwargs:
                if kwargs['dx'] == -1:
                    kwargs['dx'] = self.dx - dx
            if 'dy' in kwargs:
                if kwargs['dx'] == -1:
                    kwargs['dx'] = self.dy - dy
        if test == 0:
            return fn(self, *args, **kwargs)
        if test == 1:
            return fn(self, *(arg1, arg2) + args[2:], **kwargs)
        if test == 2:
            return fn(self, *(arg1, arg2, arg3, arg4) + args[4:], **kwargs)

    return fun


class SubDc(object):

    def __init__(self,parent,x,y,dx,dy,reg_max=True):
        self.x = parent.x + x
        self.y = parent.y + y
        self.dx = dx
        self.dy = dy
        if parent.__class__ == SubDc:
            self._parent = parent._parent
        else:
            self._parent = parent
        if reg_max:
            self._parent.test_point(self.x + self.dx, self.y + self.dy)

    def subdc(self,x,y,dx,dy,reg_max=True,):
        return SubDc(self,x,y,dx,dy,reg_max)

    def get_size(self):
        return [self.dx, self.dy]

    def __getattribute__(self, attr):
        try:
            ret = object.__getattribute__(self, attr)
        except:
            ret = getattr(self._parent, attr)
        return ret

    def play_str(self, str):
        for buf in str.split('\n'):
            buf = buf.strip()
            if buf != '':
                pos = buf.split('(')
                if len(pos) > 2:
                    pos2 = []
                    pos2.append(pos[0])
                    pos2.append(''.s.join(pos[1:]))
                    pos = pos2
                if len(pos) == 2:
                    name = pos[0]
                    attr = (pos[1])[:-1]
                    if attr == '':
                        attr = None
                    else:
                        attr = json.loads('[' + attr + ']')
                    fun = getattr(self, name)
                    if attr:
                        fun(*attr)
                    else:
                        fun()

    @convert_fun_arg
    def add_line(self,x,y,dx,dy):
        return self._parent.add_line(x, y, dx, dy)

    @convert_fun_arg
    def add_rectangle(self,x,y,dx,dy):
        return self._parent.add_rectangle(x, y, dx, dy)

    @convert_fun_arg
    def add_rounded_rectangle(self, x, y, dx, dy, radius):
        return self._parent.add_rounded_rectangle(x, y, dx, dy, radius)

    @convert_fun_arg
    def add_arc(self, x, y, radius, angle1, angle2):
        return self._parent.add_arc(x, y, radius, angle1, angle2)

    @convert_fun_arg
    def add_ellipse(self, x, y, dx, dy):
        return self._parent.add_ellipse(x, y, dx, dy)

    def add_polygon(self, xytab):
        xytab2 = []
        for pos in xytab:
            xytab2.append((self.x + pos[0], self.y + pos[1]))
        return self._parent.add_polygon(xytab2)

    def add_spline(self, xytab, close):
        xytab2 = []
        for pos in xytab:
            xytab2.append((self.x + pos[0], self.y + pos[1]))
        return self._parent.add_spline(xytab2, close)

    @convert_fun_arg
    def draw_text(self, x, y, txt):
        return self._parent.draw_text(x, y, txt)

    @convert_fun_arg
    def draw_rotated_text(self, x, y, txt, angle):
        return self._parent.draw_rotated_text(x, y, txt, angle)

    @convert_fun_arg
    def draw_image(self, x, y, dx, dy, scale, png_data):
        return self._parent.draw_text(x, y, dx, dy, scale, png_data)

    @convert_fun_arg
    def draw_atom_line(self, x, y, line):
        return self._parent.draw_atom_line(x, y, line)


class NullDc(object):
    def __init__(self, ref_dc):
        self._ref_dc = ref_dc
        self._maxwidth = 0
        self._maxheight = 0

    def __getattribute__(self, attr):
        if attr.startswith('_'):
            ret = object.__getattribute__(self, attr)
        else:
            try:
                ret = object.__getattribute__(self, attr)
            except:
                ret = getattr(self._ref_dc, attr)
        return ret

    def get_dc_info(self):
        return self._ref_dc.dc_info

    def get_max_sizes(self):
        return (self._maxwidth, self._maxheight)

    def test_point(self, x, y):
        if x > 10000000 or y > 1000000:
            return
        if x > self._maxwidth:
            self._maxwidth = x
        if y > self._maxheight:
            self._maxheight = y

    def subdc(self, x, y, dx, dy, reg_max=True):
        return SubDc(self, x, y, dx, dy, reg_max)

    def add_line(self, x, y, dx, dy):
        self.test_point(x + dx, y + dy)
        return None

    def add_rectangle(self, x, y, dx, dy):
        self.test_point(x + dx, y + dy)
        return None

    def add_rounded_rectangle(self, x, y, dx, dy, radius):
        self.test_point(x + dx, y + dy)
        return None

    def add_arc(self, x, y, radius, angle1, angle2):
        self.test_point(x + radius, y + radius)
        return None

    def add_ellipse(self, x, y, dx, dy):
        self.test_point(x + dx, y + dy)
        return None

    def add_polygon(self, xytab):
        for pos in xytab:
            self.test_point(pos[0], pos[1])
        return None

    def add_spline(self, xytab, close):
        for pos in xytab:
            self.test_point(pos[0], pos[1])
        return None

    def draw_text(self, x, y, txt):
        self.test_point(x, y)
        return None

    def draw_rotated_text(self, x, y, txt, angle):
        self.test_point(x, y)
        return None

    def draw_image(self, x, y, dx, dy, scale, png_data):
        self.test_point(x + dx, y + dy)
        return None


class NullDcinfo(object):
    def __init__(self, dc):
        pass

    def get_text_width(self, txt, style):
        return 12 * len(txt)

    def get_text_height(self, txt, style):
        return 12

    def get_line_dy(self, height):
        return height * 12

    def get_multiline_text_width(self, txt, style='default'):
        return 100

    def get_multiline_text_height(self, txt, width, style='default'):
        return (100, [])

    def get_extents(self, word, style):
        return (100, 0, 0, 20)

    def get_style_id(self, style):
        return 0


