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

import io

from schlib.schhtml.basehtmltags import BaseHtmlAtomParser, register_tag_map
from schlib.schhtml.atom import Atom, NullAtom, BrAtom


class AtomTag(BaseHtmlAtomParser):
    def __init__(self, parent, parser, tag, attrs):
        BaseHtmlAtomParser.__init__(self, parent, parser, tag, attrs)
        self.child_tags = parent.child_tags + ['a', 'p', 'calc', 'big', 'strong', 'span', 'font', 'div']
        self.gparent = parent.gparent

    def draw_atom(self, dc, style, x, y, dx, dy):
        parent = self.parent
        while parent:
            if type(parent)==Atag:
                return parent.draw_atom(dc, style, x, y, dx, dy)
            parent = parent.parent
        return False

    def close(self):
        if self.atom_list:
            self.parent.append_atom_list(self.atom_list)


class BrTag(AtomTag):

    def __init__(self, parent, parser, tag, attrs):
        AtomTag.__init__(self, parent, parser, tag, attrs)

    def close(self):
        self.make_atom_list()
        self.atom_list.append_atom(BrAtom())
        self.parent.append_atom_list(self.atom_list)


class Atag(AtomTag):

    def __init__(self, parent, parser, tag, attrs):
        AtomTag.__init__(self, parent, parser, tag, attrs)
        self.no_wrap = True

    def set_dc_info(self, dc_info):
        ret = AtomTag.set_dc_info(self, dc_info)
        self.make_atom_list()
        return ret

    def draw_atom(self, dc, style, x, y, dx, dy):
        self.reg_action('href', dc.subdc(x, y, dx, dy))
        return False

    def close(self):
        atom = NullAtom()
        self.atom_list.append_atom(atom)
        for atom in self.atom_list.atom_list:
            if not atom.parent:
                atom.set_parent(self)
        self.parent.append_atom_list(self.atom_list)

    def __repr__(self):
        return "ATag(" + self.tag +";" + str(self.attrs)+")"

class ImgDraw(object):

    def __init__(self, img_tag, image, width, height):
        self.img_tag = img_tag
        self.image = image
        self.width = width
        self.height = height

    def draw_atom(self, dc, style, x, y, dx, dy):
        http = self.img_tag.parser.http
        if self.image:
            dc.draw_image(x, y, self.width, self.height, 3, self.image,)
        else:
            print('null_img')


class ImgTag(AtomTag):

    def __init__(self, parent, parser, tag, attrs):
        AtomTag.__init__(self, parent, parser, tag, attrs)

        if 'src' in attrs:
            self.src = attrs['src']
        else:
            self.src = None
        self.img = None
        self.dx = 0
        self.dy = 0
        if self.src:
            http = self.parser.get_http_object()
            try:
                (status, ur) = http.get(self, self.src)
                if status == 404:
                    img = None
                else:
                    img = http.ptr()
                    http.clear_ptr()
            except:
                img = None
            if img:
                img_name = self.src.lower()
                if '.png' in img_name:
                    self.img = img
                else:
                    stream = io.BytesIO(img)
                    import PIL
                    image = PIL.Image.open(stream)
                    output = io.BytesIO()
                    image.save(output, "PNG")
                    self.img = output.getvalue()
            else:
                self.img = None

    def close(self):
        if self.img:
            if self.width > 0 and self.height > 0:
                self.dx = self.width
                self.dy = self.height
            else:
                (self.dx, self.dy) = self.dc_info.get_img_size(self.img)
            img_atom = Atom(ImgDraw(self, self.img, self.dx, self.dy), self.dx,
                            0, self.dy, 0)
            img_atom.set_parent(self)
            self.make_atom_list()
            self.atom_list.append_atom(img_atom)
            self.parent.append_atom_list(self.atom_list)

class ParCalc(AtomTag):
    def handle_data(self, data):
        parent=self.parent
        while parent:
            if parent.tag=='table':
                table=parent
            if parent.tag=='body':
                body=parent
            if parent.tag=='html':
                html=parent
            parent = parent.parent
        data2 = str(eval(data))
        return AtomTag.handle_data(self, data2)


register_tag_map('br', BrTag)
register_tag_map('a', Atag)
register_tag_map('i', AtomTag)
register_tag_map('b', AtomTag)
register_tag_map('em', AtomTag)
register_tag_map('strong', AtomTag)
register_tag_map('s', AtomTag)
register_tag_map('small', AtomTag)
register_tag_map('big', AtomTag)
register_tag_map('sub', AtomTag)
register_tag_map('sup', AtomTag)
register_tag_map('tt', AtomTag)
register_tag_map('span', AtomTag)
register_tag_map('font', AtomTag)
register_tag_map('img', ImgTag)
register_tag_map('image', ImgTag)
register_tag_map('calc', ParCalc)

