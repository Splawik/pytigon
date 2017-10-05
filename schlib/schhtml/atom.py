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


from schlib.schhtml.htmltools import superstrip

decode_sym = (('&gt;','>'), ('&lt;','<'), ('&amp;', '&'), ('&quot;','\"'),)

def unescape(txt):
    ret = txt
    for pos in decode_sym:
        if pos[0] in txt:
            ret = ret.replace(pos[0],pos[1])
    return ret

class Atom(object):
    """Base rendered element"""
    def __init__(self,data,dx,dx_space,dy_up,dy_down,style=-1,is_txt=False):
        self.data = data
        self.dx = dx
        self.dx_space = dx_space
        self.dy_up = dy_up
        self.dy_down = dy_down
        self.style = style
        self.parent = None
        self.is_txt = is_txt

    def get_width(self):
        return self.dx

    def get_height(self):
        return self.dy_up + self.dy_down

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent


class NullAtom(Atom):
    def __init__(self):
        self.data = ''
        self.dx = 0
        self.dx_space = 0
        self.dy_up = 0
        self.dy_down = 0
        self.style = None
        self.parent = None
        self.is_txt = None

    def draw_atom(self,dc,style,x,y):
        return True


class BrAtom(NullAtom):
    def __init__(self, cr_count=1):
        NullAtom.__init__(self)
        self.cr_count = cr_count

class AtomLine(object):
    """Class represent full line in rendered html"""
    def __init__(self, maxwidth):
        self.maxwidth = maxwidth
        self.dx = 0
        self.space = 0
        self.dy_up = 0
        self.dy_down = 0
        self.objs = []

    def _append(self, atom):
        atom = atom
        if len(self.objs) > 0 and atom.is_txt:
            if False:
                self.objs[-1].data += atom.data
                self.objs[-1].dx_space = atom.dx_space
                self.objs[-1].dx += atom.get_width()
                self.dx = self.dx + atom.get_width()
            else:
                self.objs.append(atom)
                self.dx = self.dx + atom.get_width()
        else:
            self.objs.append(atom)
            self.dx = self.dx + atom.get_width()
        self.space = atom.dx_space
        if self.dy_up < atom.dy_up:
            self.dy_up = atom.dy_up
        if self.dy_down < atom.dy_down:
            self.dy_down = atom.dy_down

    def append(self, atom, force_append=False):
        if len(self.objs) > 0:
            if force_append or (self.dx + atom.get_width()) - atom.dx_space <= self.maxwidth:
                self._append(atom)
                return True
            return False
        else:
            if force_append or atom.get_width() - atom.dx_space <= self.maxwidth:
                self._append(atom)
                return True
            return False

    def get_height(self):
        return self.dy_up + self.dy_down


class AtomList(object):
    def __init__(self, dc_info, line_dy=0, pre=False):
        self.dc_info = dc_info
        self.atom_list = []
        self.line_dy = dc_info.get_line_dy(line_dy)
        self.list_for_draw = None
        self.first_line_height = -1
        self.width = -1
        self.pre = pre

    def set_line_dy(self, dy):
        self.line_dy = self.dc_info.get_line_dy(dy)

    def append_text(self,txt,style,parent=None):
        if txt and len(txt) > 0:
            if not self.pre:
                txt2 = unescape(txt.replace('\n', ' '))
            else:
                if '\n' in txt:
                    txt2 = unescape(txt)
                    x = txt2.split('\n')
                    self.append_text(x[0], style, parent)
                    last_br = None
                    for pos in x[1:]:
                        if pos!='':
                            if last_br:
                                last_br.cr_count += 1
                            else:
                                last_br = BrAtom()
                                self.append_atom(BrAtom())
                            self.append_text(pos, style, parent)
                            last_br = None
                        else:
                            if last_br:
                                last_br.cr_count += 1
                            else:
                                last_br = BrAtom()
                                self.append_atom(last_br)
                    return
                else:
                    txt2 = unescape(txt)
            words = superstrip(txt2).split(' ')
            if txt2[0] == ' ':
                words[0] = ' ' + words[0]
            for i in range(0, len(words) - 1):
                words[i] = words[i] + ' '
            if txt2[-1] == ' ':
                words[-1] = words[-1] + ' '
                if words[-1] == '  ':
                    words[-1] = ' '
            if self.pre or (parent and parent.no_wrap):
                if txt2 != '':
                    extents = self.dc_info.get_extents(txt2, style)
                    atom = Atom(superstrip(txt2),extents[0],extents[1],extents[2],extents[3],style,True)
                    atom.set_parent(parent)
                    self.atom_list.append(atom)
            else:
                for word in words:
                    if word == '':
                        continue
                    extents = self.dc_info.get_extents(word, style)
                    atom = Atom(word,extents[0],extents[1],extents[2],extents[3],style,True)
                    if parent:
                        atom.set_parent(parent)
                    self.atom_list.append(atom)

    def append_atom(self, atom):
        self.atom_list.append(atom)

    def get_width_tab(self):
        minwidth = 0
        maxwidth = 0
        maxmaxwidth = 0
        for atom in self.atom_list:
            if atom.get_width() > minwidth:
                minwidth = atom.get_width()
            maxwidth += atom.get_width() + atom.dx_space
            if type(atom) == BrAtom:
                if maxwidth > maxmaxwidth:
                    maxmaxwidth = maxwidth
                    maxwidth = 0

        if maxwidth < maxmaxwidth:
            maxwidth = maxmaxwidth

        if len(self.atom_list) > 8:
            optwidth = (maxwidth * 8) / len(self.atom_list)
        else:
            optwidth = maxwidth
        return (optwidth, minwidth, maxwidth)

    def gen_list_for_draw(self, width):
        l = []
        last_atom = None
        line = AtomLine(width)
        for atom in self.atom_list:
            if atom.__class__ == BrAtom:
                if atom.cr_count>1:
                    line.dy_down = line.dy_down + line.get_height()*(atom.cr_count-1)
                l.append(line)
                line = AtomLine(width)
                continue
            test_append = True
            if atom.is_txt and atom.data == ' ':
                if last_atom == None or last_atom and last_atom.is_txt\
                        and last_atom.data[-1] == ' ' or 'CtrlTag'\
                        in last_atom.data.__class__.__name__:
                    test_append = False
            if test_append:
                if not line.append(atom):
                    l.append(line)
                    line = AtomLine(width)
                    line.append(atom, force_append=True)
            last_atom = atom
        if len(line.objs) > 0:
            l.append(line)
            if self.first_line_height == -1:
                self.first_line_height = line.get_height()
        self.list_for_draw = l
        self.width = width

    def get_height(self):
        if self.list_for_draw:
            dy = 0
            for pos in self.list_for_draw:
                dy = dy + pos.get_height()
            dy += self.line_dy * (len(self.list_for_draw) - 1)
            return dy
        else:
            return -1

    def draw_atom_list(self,dc,align=0,valign=1):
        size = dc.get_size()
        if size[0] == -1:
            size[0] = self.width
        if valign > 0:
            y2 = self.get_height()
            if valign == 1:
                y = (size[1] - y2) / 2
            else:
                y = size[1] - y2
        else:
            y = 0
        for line in self.list_for_draw:
            if len(line.objs) > 0:
                if align == 0:
                    x = 0
                else:
                    if align == 1:
                        x = (size[0] - line.dx + line.space) / 2
                    else:
                        x = size[0] - line.dx + line.space
                subdc = dc.subdc(x, y, size[0] - x, line.get_height())
                subdc.draw_atom_line(0, 0, line)
                y += line.get_height() + self.line_dy
        return y - self.line_dy

    def to_txt(self):
        ret = ''
        for atom in self.atom_list:
            if type(atom.data)==str:
                ret += atom.data
        return ret

    def to_attrs(self):
        attrs = {}
        for atom in self.atom_list:
            if atom.parent:
                for attr in atom.parent.attrs:
                    if not attr in attrs:
                        attrs[attr] = atom.parent.attrs[attr]
                attrs['data'] = atom.data
        return attrs

    def to_obj_tab(self):
        objs = {}
        for atom in self.atom_list:
            if atom.parent and not atom.parent.sys_id in objs:
                objs[atom.parent.sys_id] = atom.parent
        return objs


