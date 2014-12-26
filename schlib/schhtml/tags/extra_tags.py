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

from schlib.schhtml.basehtmltags import BaseHtmlAtomParser, register_tag_map
from schlib.schhtml.atom import AtomList, Atom
from schlib.schhtml.render_helpers import RenderBackground, RenderBorder, \
    RenderCellSpacing, RenderCellPadding, get_size
from collections import deque
import sys
import traceback


class VectorImg(BaseHtmlAtomParser):

    def __init__(
        self,
        parent,
        parser,
        tag,
        attrs,
        ):
        BaseHtmlAtomParser.__init__(self, parent, parser, tag, attrs)
        self.gparent = parent.gparent
        self.render_helpers = [RenderCellSpacing(self), RenderBorder(self),
                               RenderBackground(self), RenderCellPadding(self)]
        self.extra_space = get_size(self.render_helpers)
        self.draw_txt = ''

    def _get_pseudo_margins(self):
        return [self.extra_space[0], self.extra_space[1], self.extra_space[2],
                self.extra_space[3]]

    def close(self):
        if self.width > 0 and self.height > 0:
            self.dx = self.width
            self.dy = self.height
        else:
            self.dx = 100
            self.dy = 100
        img_atom = Atom(self, self.dx, 0, self.dy, 0)
        img_atom.set_parent(self)
        self.make_atom_list()
        self.atom_list.append_atom(img_atom)
        self.parent.append_atom_list(self.atom_list)

    def handle_data(self, data):
        self.draw_txt += data

# def render(self, dc):

    def draw_atom(
        self,
        dc,
        style,
        x,
        y,
        dx,
        dy,
        ):
        self.reg_id(dc)
        self.reg_end()
        dc2 = dc.subdc(x, y, self.width, self.height, True)
        for r in self.render_helpers:
            dc2 = r.render(dc2)
        dc2.play_str(self.draw_txt)
        return True


register_tag_map('vimg', VectorImg)
